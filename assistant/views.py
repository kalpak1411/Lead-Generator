from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.db.models import Count, Q
import csv
import json

from .models import IdealCustomerProfile, Lead
from .services.scraper import WebsiteScraper
from .services.qualifier import QualificationEngine

def dashboard_view(request):
    leads = Lead.objects.all().order_by('-created_at')
    icps = IdealCustomerProfile.objects.all()

    total_leads = leads.count()
    strong_fits = leads.filter(icp_fit_level='STRONG').count()
    moderate_fits = leads.filter(icp_fit_level='MODERATE').count()
    low_fits = leads.filter(icp_fit_level='LOW').count()
    disqualified = leads.filter(icp_fit_level='DISQUALIFIED').count()

    recent_leads = leads[:8]

    context = {
        'total_leads': total_leads,
        'strong_fits': strong_fits,
        'moderate_fits': moderate_fits,
        'low_fits': low_fits,
        'disqualified': disqualified,
        'recent_leads': recent_leads,
        'icps': icps,
    }
    return render(request, 'assistant/dashboard.html', context)

def lead_list_view(request):
    query = request.GET.get('q', '').strip()
    fit_filter = request.GET.get('fit', '')
    icp_filter = request.GET.get('icp', '')

    leads = Lead.objects.all()

    if query:
        leads = leads.filter(
            Q(company_name__icontains=query) |
            Q(website_url__icontains=query) |
            Q(detected_industry__icontains=query) |
            Q(business_summary__icontains=query) |
            Q(supplied_contact_name__icontains=query)
        )

    if fit_filter:
        leads = leads.filter(icp_fit_level=fit_filter)

    if icp_filter:
        leads = leads.filter(icp_id=icp_filter)

    icps = IdealCustomerProfile.objects.all()

    return render(request, 'assistant/lead_list.html', {
        'leads': leads,
        'query': query,
        'fit_filter': fit_filter,
        'icp_filter': icp_filter,
        'icps': icps,
    })

def lead_create_view(request):
    icps = IdealCustomerProfile.objects.all()

    if request.method == 'POST':
        company_name = request.POST.get('company_name', '').strip()
        website_url = request.POST.get('website_url', '').strip()
        supplied_contact_name = request.POST.get('supplied_contact_name', '').strip()
        supplied_contact_role = request.POST.get('supplied_contact_role', '').strip()
        supplied_contact_email = request.POST.get('supplied_contact_email', '').strip()
        supplied_notes = request.POST.get('supplied_notes', '').strip()
        icp_id = request.POST.get('icp')
        auto_research = request.POST.get('auto_research') == 'on'

        if not company_name or not website_url:
            messages.error(request, 'Company name and website URL are required.')
            return render(request, 'assistant/lead_create.html', {'icps': icps})

        icp = None
        if icp_id:
            icp = IdealCustomerProfile.objects.filter(id=icp_id).first()

        lead = Lead.objects.create(
            company_name=company_name,
            website_url=website_url,
            supplied_contact_name=supplied_contact_name,
            supplied_contact_role=supplied_contact_role,
            supplied_contact_email=supplied_contact_email,
            supplied_notes=supplied_notes,
            icp=icp,
        )

        if auto_research:
            _run_lead_research(lead)
            messages.success(request, f'Lead "{lead.company_name}" created & researched successfully!')
            return redirect('lead_detail', pk=lead.pk)

        messages.success(request, f'Lead "{lead.company_name}" added.')
        return redirect('lead_detail', pk=lead.pk)

    return render(request, 'assistant/lead_create.html', {'icps': icps})

def lead_detail_view(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    icps = IdealCustomerProfile.objects.all()

    if request.method == 'POST':
        # Update outreach angle or reassign ICP
        action = request.POST.get('action')
        if action == 'update_notes':
            lead.supplied_notes = request.POST.get('supplied_notes', '')
            lead.personalized_outreach_subject = request.POST.get('personalized_outreach_subject', '')
            lead.personalized_outreach_angle = request.POST.get('personalized_outreach_angle', '')
            lead.save()
            messages.success(request, 'Outreach copy and notes saved.')
        elif action == 'change_icp':
            new_icp_id = request.POST.get('icp_id')
            if new_icp_id:
                lead.icp = IdealCustomerProfile.objects.filter(id=new_icp_id).first()
                lead.save()
                messages.success(request, 'Assigned ICP updated.')

        return redirect('lead_detail', pk=lead.pk)

    return render(request, 'assistant/lead_detail.html', {'lead': lead, 'icps': icps})

def lead_research_view(request, pk):
    """
    Triggers live scraping & qualification pipeline for a given lead.
    """
    lead = get_object_or_404(Lead, pk=pk)
    _run_lead_research(lead)
    messages.success(request, f'Completed live research and qualification analysis for {lead.company_name}!')
    return redirect('lead_detail', pk=lead.pk)

def _run_lead_research(lead):
    # 1. Scrape Website
    scraped = WebsiteScraper.fetch_company_info(lead.website_url)

    # 2. Run Qualification Engine
    analysis = QualificationEngine.analyze_company(scraped, lead, lead.icp)

    # 3. Update Model
    lead.scraped_page_title = scraped.get('title', '')
    lead.scraped_raw_text = scraped.get('raw_text', '')[:3000]
    lead.business_summary = analysis['business_summary']
    lead.detected_industry = analysis['detected_industry']
    lead.target_market = analysis['target_market']
    lead.core_products_services = analysis['core_products_services']
    lead.icp_fit_level = analysis['icp_fit_level']
    lead.icp_fit_score = analysis['icp_fit_score']
    lead.icp_qualification_reasons = analysis['icp_qualification_reasons']
    lead.evidence_links = analysis['evidence_links']
    lead.personalized_outreach_subject = analysis['personalized_outreach_subject']
    lead.personalized_outreach_angle = analysis['personalized_outreach_angle']
    lead.last_researched_at = timezone.now()
    lead.save()

def icp_list_view(request):
    icps = IdealCustomerProfile.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        target_industries = request.POST.get('target_industries', '').strip()
        target_company_sizes = request.POST.get('target_company_sizes', '').strip()
        key_pain_points = request.POST.get('key_pain_points', '').strip()
        value_proposition = request.POST.get('value_proposition', '').strip()
        disqualifying_signals = request.POST.get('disqualifying_signals', '').strip()

        if not name or not target_industries or not key_pain_points:
            messages.error(request, 'Profile Name, Target Industries, and Key Pain Points are required.')
        else:
            IdealCustomerProfile.objects.create(
                name=name,
                target_industries=target_industries,
                target_company_sizes=target_company_sizes,
                key_pain_points=key_pain_points,
                value_proposition=value_proposition,
                disqualifying_signals=disqualifying_signals,
            )
            messages.success(request, f'Ideal Customer Profile "{name}" created!')
            return redirect('icp_list')

    return render(request, 'assistant/icp_list.html', {'icps': icps})

def export_leads_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="qualified_leads_export.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Company Name', 'Website URL', 'Contact Name', 'Contact Role',
        'Contact Email', 'ICP Fit Level', 'Fit Score', 'Detected Industry',
        'Target Market', 'Business Summary', 'Personalized Angle', 'Evidence Excerpts'
    ])

    for lead in Lead.objects.all():
        evidence_text = " | ".join([e.get('quote', '') for e in (lead.evidence_links or [])])
        writer.writerow([
            lead.company_name,
            lead.website_url,
            lead.supplied_contact_name,
            lead.supplied_contact_role,
            lead.supplied_contact_email,
            lead.get_icp_fit_level_display(),
            lead.icp_fit_score,
            lead.detected_industry,
            lead.target_market,
            lead.business_summary,
            lead.personalized_outreach_angle,
            evidence_text
        ])

    return response

