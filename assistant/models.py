from django.db import models

class IdealCustomerProfile(models.Model):
    name = models.CharField(max_length=200, help_text="e.g. Mid-Market B2B SaaS or High-Growth FinTech")
    target_industries = models.TextField(help_text="Comma-separated or bullet points of target industries (e.g. B2B SaaS, Cybersecurity, E-Commerce, Healthcare Tech)")
    target_company_sizes = models.CharField(max_length=200, blank=True, default="50-500 employees")
    key_pain_points = models.TextField(help_text="Pain points your solution solves (e.g. slow content turnaround, high customer churn, API security)")
    value_proposition = models.TextField(help_text="What your offering provides to this ICP")
    disqualifying_signals = models.TextField(blank=True, default="", help_text="Negative signals that lower ICP fit (e.g. B2C only, legacy on-prem, no digital presence)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Lead(models.Model):
    FIT_CHOICES = [
        ('STRONG', 'Strong Fit'),
        ('MODERATE', 'Moderate Fit'),
        ('LOW', 'Low Fit'),
        ('DISQUALIFIED', 'Disqualified'),
        ('PENDING', 'Pending Research'),
    ]

    company_name = models.CharField(max_length=255)
    website_url = models.URLField(max_length=500)
    supplied_contact_name = models.CharField(max_length=255, blank=True, default="")
    supplied_contact_role = models.CharField(max_length=255, blank=True, default="")
    supplied_contact_email = models.CharField(max_length=255, blank=True, default="")
    supplied_notes = models.TextField(blank=True, default="", help_text="Publicly supplied lead information or notes")

    icp = models.ForeignKey(IdealCustomerProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='leads')

    # Research findings
    business_summary = models.TextField(blank=True, default="", help_text="Summarized value proposition and what the company does")
    detected_industry = models.CharField(max_length=255, blank=True, default="")
    target_market = models.CharField(max_length=255, blank=True, default="") # B2B, B2C, Enterprise, etc.
    core_products_services = models.TextField(blank=True, default="")
    
    # Qualification
    icp_fit_level = models.CharField(max_length=20, choices=FIT_CHOICES, default='PENDING')
    icp_fit_score = models.IntegerField(default=0, help_text="Score out of 100")
    icp_qualification_reasons = models.TextField(blank=True, default="", help_text="Key reasons for ICP fit or mismatch")

    # Outreach
    personalized_outreach_subject = models.CharField(max_length=300, blank=True, default="")
    personalized_outreach_angle = models.TextField(blank=True, default="", help_text="Evidence-backed personalized pitch")

    # Evidence audit trail (stored as JSON)
    evidence_links = models.JSONField(default=list, blank=True, help_text="List of quotes, claims, and exact source URLs found on the website")

    # Metadata
    scraped_page_title = models.CharField(max_length=500, blank=True, default="")
    scraped_raw_text = models.TextField(blank=True, default="")
    last_researched_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.company_name} ({self.get_icp_fit_level_display()})"
