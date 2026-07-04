# Security Policy

## Reporting a Vulnerability

### DO NOT Disclose Publicly

If you discover a security vulnerability in QR-SHIELD, please **DO NOT** open a public GitHub issue.

Instead, report it confidentially using **one of these methods:**

### Method 1: GitHub Security Advisory (Recommended)

Use GitHub's private vulnerability reporting feature:

1. Go to [Security Advisories](https://github.com/dreamed000/QR-SHIELD/security/advisories)

1. Click "Report a vulnerability"

1. Provide detailed information

1. Submit

This creates a private communication channel with maintainers.

### Method 2: Email (For Severe Issues)

Email the maintainer directly:

- **To:** dreamdrafted000@gmail.com

- **Subject:** [SECURITY] Vulnerability Report - QR-SHIELD

- **PGP Key:** [To be provided]

### Method 3: GitHub Issue (If private reporting unavailable)

If private channels are unavailable:

1. Open a private security issue (if available)

1. Title it `[SECURITY] Vulnerability Description`

1. Include reproduction steps

1. Do NOT disclose exploit details beyond the minimum required for reproduction

---

## Vulnerability Disclosure Timeline

### Our Commitment

We follow responsible disclosure principles:

| Timeline | Action |
| --- | --- |
| Day 1 | Vulnerability report received and acknowledged |
| Day 3 | Triage and severity assessment |
| Day 7 | Fix development begins |
| Day 30 | Security patch released (target) |
| Day 90 | Public disclosure if patch not ready |

### Your Responsibility

- Do not disclose vulnerability publicly before:

  - We release a patch, OR

  - 90 days have passed (whichever comes first)

- Do not test vulnerability on live systems

- Do not access data beyond scope of testing

---

## Vulnerability Severity Levels

| Severity | Description | Action |
| --- | --- | --- |
| Critical | Immediate risk, high impact | Emergency patch within 24-48 hours |
| High | Likely risk, significant impact | Patch within 1-2 weeks |
| Medium | Possible risk, moderate impact | Patch within 1 month |
| Low | Limited impact, unlikely risk | Included in next release |

---

## What Makes a Valid Report

### Valid Reports Include

- Clear description of vulnerability

- Steps to reproduce

- Potential impact

- Your contact information

- Suggested fix (optional but appreciated)

### Invalid Reports

- Theoretical vulnerabilities without PoC

- Dependent on user error or misconfiguration

- Social engineering attacks

- Social-engineering attempts

- Physical attacks

---

## What Happens Next

### After You Report

1. **Acknowledgment** - We confirm receipt within 1 business day

1. **Investigation** - We evaluate and verify the vulnerability

1. **Development** - We create a security patch

1. **Testing** - We test the patch thoroughly

1. **Release** - We publish a security advisory and patch

1. **Credit** - We acknowledge your discovery (optional)

### Communication

- We will keep you updated on progress

- We will discuss disclosure timeline with you

- We will notify you when patch is released

---

## Security Update Policy

### When We Release Security Updates

- Critical vulnerabilities: Within 48 hours

- High vulnerabilities: Within 2 weeks

- Medium vulnerabilities: Within 1 month

- Low vulnerabilities: In next regular release

### Supported Versions

| Version | Status | Support Until |
| --- | --- | --- |
| 1.x | Active | Current + 6 months |
| 0.x | Security fixes only | 12 months from 1.0 release |
| Legacy | End of life | No support |

---

## General Security Practices

### Using QR-SHIELD Safely

- Run only on authorized systems

- Use isolated environments for testing

- Keep Python and dependencies updated

- Use strong file permissions on sessions/

- Delete sessions after testing

- Monitor for unauthorized access

- Log all activities

### For Administrators

- Keep QR-SHIELD and dependencies current

- Monitor for security advisories

- Apply security patches promptly

- Restrict access to sessions/ directory

- Use version pinning in production

- Test updates before deployment

---

## Security Best Practices

### Secure Development

- Use branch protection rules

- Require code review before merge

- Run security tests in CI/CD

- Scan dependencies for vulnerabilities

- Update dependencies regularly

- Use cryptographic libraries properly

### Secure Deployment

- Use environment variables for secrets

- Encrypt sensitive data at rest

- Use HTTPS for all communications

- Implement access controls

- Log security events

- Monitor for suspicious activity

---

## Known Vulnerabilities

Current known security considerations:

| Issue | Status | Mitigation |
| --- | --- | --- |
| QR code interception | Inherent | Operate in isolated environment |
| Browser fingerprinting | Inherent | Accept as research limitation |
| Session data privacy | Mitigated | Encrypt sessions/ directory |
| Dependency vulnerabilities | Managed | Regular updates and scanning |

See [THREAT_MODEL.md](../../THREAT_MODEL.md) for threat analysis.

---

## Security Advisories

### GitHub Advisories

Subscribe to security advisories:

1. Watch repository

1. Enable notifications

1. Check GitHub Advisories regularly

### Mailing List

To be announced - Sign up for security bulletins

---

## FAQ

### Q: How long will you keep my report confidential?

A: Until we publish a security patch or 90 days, whichever comes first.

### Q: Can I publicly disclose after 90 days?

A: Yes, but please notify us first. We prefer coordinated disclosure.

### Q: Will I be credited for the report?

A: Yes, if you want to be (publicly or anonymously).

### Q: What if I don't agree with your severity assessment?

A: We're happy to discuss. Email the maintainer to appeal.

### Q: Do you have a bug bounty program?

A: Not currently, but we deeply appreciate responsible researchers.

---

## Security-Related Resources

### Further Reading

- [OWASP Security Guidelines](https://owasp.org/)

- [SANS Security Resources](https://www.sans.org/)

- [CWE/CAPEC](https://cwe.mitre.org/)

### Responsible Disclosure

- [Coordinated Vulnerability Disclosure](https://cheatsheetseries.owasp.org/cheatsheets/Vulnerability_Disclosure_Cheat_Sheet.html)

- [HackerOne Guidelines](https://www.hackerone.com/vulnerability-disclosure)

---

## Contact

**Primary Contact:** Puneet Chandra Chaudhary (@dreamed000)

- Email: dreamdrafted000@gmail.com

- GitHub: [@dreamed000](https://github.com/dreamed000)

- ORCID: [0009-0005-7220-2327](https://orcid.org/0009-0005-7220-2327)

---

**Thank you for helping keep QR-SHIELD secure!**

Last Updated: July 2026
