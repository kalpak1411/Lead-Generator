import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from assistant.models import IdealCustomerProfile, Lead

def seed():
    # 1. Ideal Customer Profiles
    icp1, _ = IdealCustomerProfile.objects.get_or_create(
        name="Mid-Market B2B SaaS & DevOps",
        defaults={
            "target_industries": "B2B SaaS, DevOps & Infrastructure, Cloud Software, Developer Tools",
            "target_company_sizes": "50-500 employees, Series A to C",
            "key_pain_points": "Manual pipeline qualification, slow content velocity, high churn, API scalability bottlenecks",
            "value_proposition": "streamline qualification velocity and automate verifiable outbound pipeline with 3x higher response rates",
            "disqualifying_signals": "B2C only, physical brick-and-mortar retail, inactive website"
        }
    )

    icp2, _ = IdealCustomerProfile.objects.get_or_create(
        name="Enterprise Cybersecurity & InfoSec",
        defaults={
            "target_industries": "Cybersecurity & InfoSec, Identity Management, Cloud Security, Compliance",
            "target_company_sizes": "100-2,000 employees",
            "key_pain_points": "SOC 2 audit compliance, lateral breach movement, zero trust migration complexity",
            "value_proposition": "eliminate compliance friction and enforce zero trust verification across all cloud endpoints",
            "disqualifying_signals": "Consumer antivirus, personal lifestyle, non-technical legacy retail"
        }
    )

    # 2. Sample Leads
    leads_data = [
        {
            "company_name": "Datadog",
            "website_url": "https://www.datadoghq.com",
            "supplied_contact_name": "Alex Vance",
            "supplied_contact_role": "VP of Product Marketing",
            "supplied_contact_email": "alex.vance@datadoghq.com",
            "supplied_notes": "Leading cloud monitoring and observability platform. Recently expanded security monitoring features.",
            "icp": icp1,
            "detected_industry": "DevOps & Infrastructure",
            "target_market": "B2B / Mid-Market & Enterprise",
            "business_summary": "Datadog is a B2B monitoring and analytics platform for cloud-scale applications, infrastructure, network, and application security.",
            "core_products_services": "Cloud Infrastructure Monitoring; Application Performance Monitoring (APM); Log Management; Cloud Security Management",
            "icp_fit_level": "STRONG",
            "icp_fit_score": 92,
            "icp_qualification_reasons": "✓ Industry Alignment: Matches ICP target 'Devops & Infrastructure'.\n✓ Operational Need Signal: Identified relevant initiatives related to observability and cloud performance.\n✓ Target Model: Verified B2B / Mid-Market & Enterprise business model.",
            "evidence_links": [
                {
                    "quote": "See metrics, traces, and logs from all your services, apps, and platforms in one single pane of glass.",
                    "source_url": "https://www.datadoghq.com",
                    "significance": "Core value proposition extracted from homepage"
                },
                {
                    "quote": "Turn observability into continuous business impact across your entire technology stack.",
                    "source_url": "https://www.datadoghq.com",
                    "significance": "Stated enterprise positioning"
                }
            ],
            "personalized_outreach_subject": "Datadog + Mid-Market B2B SaaS & DevOps // Solving for scale in DevOps & Infrastructure",
            "personalized_outreach_angle": """Hi Alex Vance,

Given your leadership role as VP of Product Marketing at Datadog, I've been researching Datadog's footprint in the DevOps & Infrastructure space.

Noticed on your site that: "See metrics, traces, and logs from all your services, apps, and platforms in one single pane of glass..."

With your focus around Cloud Infrastructure Monitoring, teams at this stage often hit challenges around manual pipeline qualification, slow content velocity, high churn.

We built our platform to specifically streamline qualification velocity and automate verifiable outbound pipeline with 3x higher response rates.

Would you be open to a 10-minute exploratory conversation next week to see if there's mutual alignment?

Best regards,
Outreach & Strategy Team
(Evidence source: https://www.datadoghq.com)""",
            "last_researched_at": timezone.now()
        },
        {
            "company_name": "Snyk",
            "website_url": "https://snyk.io",
            "supplied_contact_name": "Marcus Kane",
            "supplied_contact_role": "Director of Growth",
            "supplied_contact_email": "marcus@snyk.io",
            "supplied_notes": "Developer security platform helping developers find and fix vulnerabilities in code, dependencies, containers, and IaC.",
            "icp": icp2,
            "detected_industry": "Cybersecurity & InfoSec",
            "target_market": "B2B / Mid-Market & Enterprise",
            "business_summary": "Snyk is a developer security platform that integrates directly into development tools, workflows, and automation pipelines to secure custom code, open source dependencies, and cloud containers.",
            "core_products_services": "Snyk Code (SAST); Snyk Open Source (SCA); Snyk Container; Snyk IaC",
            "icp_fit_level": "STRONG",
            "icp_fit_score": 90,
            "icp_qualification_reasons": "✓ Industry Alignment: Matches ICP target 'Cybersecurity & Infosec'.\n✓ Operational Need Signal: Direct alignment on vulnerability remediation and developer workflows.\n✓ Target Model: Verified B2B enterprise offering.",
            "evidence_links": [
                {
                    "quote": "Develop fast. Stay secure. Automatically find and fix vulnerabilities in your code, dependencies, containers, and infrastructure.",
                    "source_url": "https://snyk.io",
                    "significance": "Primary homepage headline"
                }
            ],
            "personalized_outreach_subject": "Snyk + Enterprise Cybersecurity // Scaling secure developer pipeline",
            "personalized_outreach_angle": """Hi Marcus Kane,

Given your leadership role as Director of Growth at Snyk, I've been tracking Snyk's developer security footprint.

Noticed on your site that: "Automatically find and fix vulnerabilities in your code, dependencies, containers, and infrastructure..."

With your focus around Snyk Code (SAST), security leaders frequently grapple with SOC 2 audit compliance and zero trust migration complexity.

We built our platform to eliminate compliance friction and enforce zero trust verification across all cloud endpoints.

Open to a brief 10-minute conversation next week to see how this aligns with your Q4 expansion?

Best regards,
Outreach & Strategy Team
(Evidence source: https://snyk.io)""",
            "last_researched_at": timezone.now()
        },
        {
            "company_name": "Chewy",
            "website_url": "https://www.chewy.com",
            "supplied_contact_name": "",
            "supplied_contact_role": "",
            "supplied_contact_email": "",
            "supplied_notes": "Online retailer of pet food and pet-related products.",
            "icp": icp1,
            "detected_industry": "E-Commerce & Retail Tech",
            "target_market": "B2C / Direct to Consumer",
            "business_summary": "Chewy is a pure-play consumer e-commerce retailer offering pet food, pet supplies, pharmacy prescriptions, and pet care products directly to households.",
            "core_products_services": "Consumer Pet Food; Toys & Accessories; Pet Pharmacy",
            "icp_fit_level": "DISQUALIFIED",
            "icp_fit_score": 15,
            "icp_qualification_reasons": "⚠ Industry Mismatch: Company aligns primarily with 'E-Commerce & Retail Tech' (Consumer Goods).\n✗ Disqualification Warning: Primarily B2C consumer-facing offering while ICP requires B2B commercial entities.",
            "evidence_links": [
                {
                    "quote": "Shop Chewy for the best pet supplies ranging from pet food, toys and treats to litter, aquariums, and pet supplements.",
                    "source_url": "https://www.chewy.com",
                    "significance": "Consumer store description"
                }
            ],
            "personalized_outreach_subject": "Chewy + Partnership Exploration",
            "personalized_outreach_angle": """Hello Chewy Team,

Reaching out to your team at Chewy, I've been researching Chewy's presence in consumer retail.

Noticed on your site that: "Shop Chewy for the best pet supplies ranging from pet food, toys and treats..."

Note: Lead is currently flagged as DISQUALIFIED against B2B SaaS ICP criteria due to direct-to-consumer business model.

Best regards,
Outreach & Strategy Team
(Evidence source: https://www.chewy.com)""",
            "last_researched_at": timezone.now()
        }
    ]

    for data in leads_data:
        Lead.objects.get_or_create(company_name=data["company_name"], defaults=data)

    print("Database successfully seeded with realistic ICP profiles and qualified leads!")

if __name__ == '__main__':
    seed()

