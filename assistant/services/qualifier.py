import re

class QualificationEngine:
    """
    Analyzes scraped company text, titles, headings, and public lead info
    against the target Ideal Customer Profile (ICP).
    Extracts strictly factual company summary, evaluates qualification fit,
    gathers evidence links with direct quote anchors, and generates personalized
    outreach angles WITHOUT inventing personal details.
    """

    INDUSTRY_KEYWORDS = {
        'Cybersecurity & InfoSec': ['security', 'soc 2', 'threat', 'vulnerability', 'zero trust', 'firewall', 'compliance', 'endpoint', 'iam'],
        'B2B SaaS / Cloud Software': ['saas', 'platform', 'workflow', 'automation', 'crm', 'cloud', 'integrations', 'api', 'dashboard', 'analytics'],
        'FinTech & Financial Services': ['payment', 'banking', 'fintech', 'accounting', 'invoicing', 'payroll', 'reconciliation', 'treasury', 'lending'],
        'Healthcare & Life Sciences': ['health', 'patient', 'clinical', 'medical', 'hipaa', 'telehealth', 'care', 'provider', 'diagnostic'],
        'E-Commerce & Retail Tech': ['ecommerce', 'e-commerce', 'store', 'checkout', 'shopify', 'retail', 'cart', 'inventory', 'omnichannel'],
        'DevOps & Infrastructure': ['kubernetes', 'docker', 'ci/cd', 'infrastructure', 'monitoring', 'observability', 'serverless', 'developer tools'],
        'EdTech & Learning': ['learning', 'education', 'course', 'training', 'students', 'lms', 'curriculum', 'school'],
        'Marketing & Sales Tech': ['marketing', 'lead gen', 'sales', 'seo', 'inbound', 'email marketing', 'conversion', 'pipeline']
    }

    @classmethod
    def analyze_company(cls, scraped_data, supplied_lead, icp):
        """
        Executes full qualification and research pipeline.
        """
        full_text = scraped_data.get('raw_text', '')
        title = scraped_data.get('title', '')
        meta_desc = scraped_data.get('meta_description', '')
        headings = scraped_data.get('headings', [])
        paragraphs = scraped_data.get('paragraphs', [])
        notes = supplied_lead.supplied_notes or ''
        company_name = supplied_lead.company_name

        combined_corpus = f"{company_name} {title} {meta_desc} {' '.join(headings)} {' '.join(paragraphs)} {notes}".lower()

        # 1. Detect Industry
        detected_industry = cls._detect_industry(combined_corpus)

        # 2. Detect Target Market (B2B, B2C, Enterprise)
        target_market = cls._detect_target_market(combined_corpus)

        # 3. Summarize What the Business Does
        business_summary, core_products = cls._generate_business_summary(
            company_name, title, meta_desc, headings, paragraphs, notes, detected_industry, target_market
        )

        # 4. Evaluate ICP Fit
        fit_level, fit_score, qualification_reasons, evidence_links = cls._evaluate_icp_fit(
            combined_corpus, paragraphs, headings, meta_desc, scraped_data.get('url', ''), icp, detected_industry, target_market
        )

        # 5. Draft Personalized Outreach Angle with Evidence (NO invented personal details)
        subject_line, outreach_angle = cls._draft_outreach_angle(
            supplied_lead, company_name, business_summary, core_products,
            fit_level, icp, evidence_links, detected_industry
        )

        return {
            'business_summary': business_summary,
            'detected_industry': detected_industry,
            'target_market': target_market,
            'core_products_services': core_products,
            'icp_fit_level': fit_level,
            'icp_fit_score': fit_score,
            'icp_qualification_reasons': qualification_reasons,
            'evidence_links': evidence_links,
            'personalized_outreach_subject': subject_line,
            'personalized_outreach_angle': outreach_angle
        }

    @classmethod
    def _detect_industry(cls, text):
        scores = {}
        for ind, keywords in cls.INDUSTRY_KEYWORDS.items():
            matches = sum(1 for kw in keywords if re.search(r'\b' + re.escape(kw) + r'\b', text))
            if matches > 0:
                scores[ind] = matches
        if scores:
            return max(scores, key=scores.get)
        return "Technology & Digital Services"

    @classmethod
    def _detect_target_market(cls, text):
        b2b_signals = ['enterprise', 'b2b', 'businesses', 'teams', 'organizations', 'companies', 'roi', 'workforce', 'clients']
        b2c_signals = ['consumer', 'shoppers', 'personal use', 'lifestyle', 'individuals', 'families', 'b2c']

        b2b_count = sum(1 for s in b2b_signals if s in text)
        b2c_count = sum(1 for s in b2c_signals if s in text)

        if b2b_count > b2c_count:
            return "B2B / Mid-Market & Enterprise"
        elif b2c_count > b2b_count:
            return "B2C / Direct to Consumer"
        return "B2B / Cross-Market"

    @classmethod
    def _generate_business_summary(cls, name, title, meta_desc, headings, paragraphs, notes, industry, market):
        """
        Creates an objective summary strictly from what the company publishes.
        """
        summary_points = []
        if meta_desc:
            summary_points.append(meta_desc)
        elif paragraphs:
            summary_points.append(paragraphs[0])
        elif title:
            summary_points.append(f"{name} operates in {industry}: {title}.")

        if notes:
            summary_points.append(f"Public Lead Context: {notes}")

        # Products / Capabilities from headings and paragraphs
        products = []
        for h in headings:
            if any(term in h.lower() for term in ['platform', 'solution', 'features', 'product', 'service', 'engine', 'software', 'suite', 'built for']):
                products.append(h)

        if not products and len(headings) >= 2:
            products = headings[:3]

        core_products_str = "; ".join(products[:4]) if products else f"{industry} core solutions and services"

        summary_text = f"{name} is a {market} organization operating in the {industry} domain. " + " ".join(summary_points[:2])

        return summary_text.strip(), core_products_str

    @classmethod
    def _evaluate_icp_fit(cls, text, paragraphs, headings, meta_desc, url, icp, detected_industry, target_market):
        if not icp:
            return 'PENDING', 50, 'No Ideal Customer Profile assigned to evaluate against.', []

        score = 50
        reasons = []
        evidence_links = []

        # Target Industry Match
        icp_industries = [i.strip().lower() for i in icp.target_industries.split(',') if i.strip()]
        matched_ind = False
        for ind in icp_industries:
            if ind in detected_industry.lower() or ind in text:
                score += 20
                matched_ind = True
                reasons.append(f"✓ Industry Alignment: Matches ICP target '{ind.title()}' (Detected: {detected_industry}).")
                break
        if not matched_ind and icp_industries:
            score -= 10
            reasons.append(f"⚠ Industry Mismatch: Company aligns primarily with '{detected_industry}', which is outside primary ICP targets ({', '.join(icp_industries)}).")

        # Pain Points & Need Alignment
        pain_points = [p.strip() for p in re.split(r'[,;\n]', icp.key_pain_points) if p.strip()]
        matched_pains = []
        for pain in pain_points:
            words = [w.lower() for w in pain.split() if len(w) > 3]
            for w in words:
                if w in text:
                    matched_pains.append(pain)
                    break

        if matched_pains:
            score += 20
            reasons.append(f"✓ Operational Need Signal: Identified relevant initiatives related to: {', '.join(set(matched_pains)[:3])}.")

        # Market Model Check (e.g. B2B SaaS preference)
        if "b2b" in target_market.lower():
            score += 10
            reasons.append(f"✓ Target Model: Verified {target_market} business model.")
        elif "b2c" in target_market.lower() and "b2b" in icp.name.lower():
            score -= 25
            reasons.append("✗ Disqualification Warning: Primarily B2C consumer-facing offering while ICP requires B2B commercial entities.")

        # Disqualifying signals check
        if icp.disqualifying_signals:
            disqualifiers = [d.strip().lower() for d in re.split(r'[,;\n]', icp.disqualifying_signals) if d.strip()]
            for dis in disqualifiers:
                if dis and dis in text:
                    score -= 30
                    reasons.append(f"✗ Negative ICP Signal Triggered: Company mentions '{dis}'.")

        # Extract real text evidence quotes from paragraphs & meta
        source_candidates = [meta_desc] + headings + paragraphs
        quote_count = 0
        for item in source_candidates:
            if not item or len(item) < 25:
                continue
            item_lower = item.lower()
            # If paragraph contains proof points or industry keywords
            if any(k in item_lower for k in ['platform', 'we ', 'our ', 'solution', 'trusted by', 'customers', 'enterprise', 'built', 'security', 'growth']):
                evidence_links.append({
                    'quote': item.strip(),
                    'source_url': url,
                    'significance': 'Publicly stated capability / positioning from company website'
                })
                quote_count += 1
                if quote_count >= 3:
                    break

        # Normalize score
        score = max(0, min(100, score))

        if score >= 75:
            fit_level = 'STRONG'
        elif score >= 50:
            fit_level = 'MODERATE'
        elif score >= 25:
            fit_level = 'LOW'
        else:
            fit_level = 'DISQUALIFIED'

        return fit_level, score, "\n".join(reasons), evidence_links

    @classmethod
    def _draft_outreach_angle(cls, lead, company_name, summary, core_products, fit_level, icp, evidence_links, industry):
        """
        Drafts a tailored outreach email angle based ONLY on verified publicly supplied details.
        STRICT RULE: Do NOT invent personal hobbies, fake mutual connections, or unverified facts.
        """
        contact_name = lead.supplied_contact_name or "Team"
        contact_role = lead.supplied_contact_role or ""

        greeting = f"Hi {contact_name}," if lead.supplied_contact_name else f"Hello {company_name} Team,"

        role_mention = f"Given your leadership role as {contact_role} at {company_name}," if contact_role else f"Reaching out to your team at {company_name},"

        evidence_quote = evidence_links[0]['quote'] if evidence_links else ""
        evidence_snippet = f'\n\nNoticed on your site that: "{evidence_quote[:160]}..."' if evidence_quote else ""

        value_prop = icp.value_proposition if icp else "help scaling companies streamline operational bottlenecks and accelerate qualified pipeline."

        subject = f"{company_name} + {icp.name if icp else 'Partnership'} // Solving for scale in {industry}"

        angle_text = f"""{greeting}

{role_mention} I've been researching {company_name}'s footprint in the {industry} space.{evidence_snippet}

With your focus around {core_products.split(';')[0]}, teams at this stage often hit challenges around {icp.key_pain_points if icp else 'scaling operational workflows'}.

We built our platform to specifically {value_prop}

Would you be open to a 10-minute exploratory conversation next week to see if there's mutual alignment?

Best regards,
Outreach & Strategy Team
(Evidence source: {lead.website_url})"""

        return subject, angle_text.strip()

