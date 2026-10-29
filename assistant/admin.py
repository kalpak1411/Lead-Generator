from django.contrib import admin
from .models import IdealCustomerProfile, Lead

@admin.register(IdealCustomerProfile)
class IdealCustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'target_company_sizes', 'created_at')
    search_fields = ('name', 'target_industries', 'key_pain_points')

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'website_url', 'icp_fit_level', 'icp_fit_score', 'detected_industry', 'last_researched_at')
    list_filter = ('icp_fit_level', 'detected_industry', 'icp')
    search_fields = ('company_name', 'website_url', 'business_summary', 'supplied_contact_name')

