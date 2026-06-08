---
name: threat-intel-email-orchestrator
description: Coordinate DNS, URL, and email checks for an email address.
---

# Threat Intel Email Orchestrator

Use this skill when the user gives an email address and wants a combined report.

## Deterministic Workflow

1. Extract the domain from the email address.
2. Run the DNS skill on the domain.
3. Build the canonical URL `https://<domain>/` and run the URL skill on it.
4. Run the email skill on the full email address.
5. Merge the three outputs into one report.

## Execution Pattern

Run the leaf scripts in order from `10_ThreatIntel_SocialEng/01_Intelligence/` and reuse their JSON output:

```bash
python skills/dns-intelligence/scripts/dns_intelligence.py <domain>
python skills/url-intelligence/scripts/url_intelligence.py https://<domain>/
python skills/email-intelligence/scripts/email_intelligence.py <email-address>
```

Use the DNS output to confirm the domain, the URL output to check the website, and the email output to check the mailbox address.

## Report Back

- Start with the email address and extracted domain.
- Then provide DNS findings, URL findings, and email findings in that order.
- End with a short overall risk assessment.
- Call out any conflicts between the three skills.
