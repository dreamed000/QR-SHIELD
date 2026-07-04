# Threat Model

Comprehensive threat analysis for QR-SHIELD and QR code-related security scenarios.

## Executive Summary

QR-SHIELD is designed to help security researchers and defenders understand threats from QR code-based login scenarios. This document analyzes the threats QR-SHIELD addresses and the risks associated with QR-SHIELD itself.

## Threats Addressed by QR-SHIELD

### 1. QR Code Session Hijacking

**Description:** An unauthorized actor captures authentication tokens during a QR-based login flow to impersonate users.

**Attack Flow:**

1. Attacker sets up environment with QR-SHIELD

1. Attacker triggers QR code display (phishing, interception)

1. Attacker scans QR with phone instead of legitimate user

1. QR-SHIELD captures session tokens

1. Attacker authenticates as victim user

**Impact:** Complete account compromise

**Mitigation:**

- Use 2FA with second factor on original device

- Rate limit QR code attempts

- Alert users of unusual access patterns

- Monitor QR code scans

### 2. Phishing via QR Code

**Description:** An unauthorized actor uses deceptive QR-based prompts to influence users into scanning misleading codes.

**Attack Vector:**

- Email phishing links to fake login pages

- SMS links with QR codes

- Physical QR codes in public places

- In-app notifications with malicious codes

**Impact:** Credential theft, session hijacking, malware distribution

**Defense:**

- Train users to verify QR sources

- Implement QR code validation

- Use secure QR generation

- Monitor anomalous QR activity

### 3. Interception Attacks

**Description:** Attacker intercepts and replays QR authentication flows.

**Attack Vectors:**

- Network interception (man-in-the-middle)

- Browser history capture

- Cache exploitation

- Session token extraction

**Impact:** Session hijacking, replay attacks

**Defenses:**

- Use HTTPS only

- Implement CSRF protection

- Use one-time tokens

- Implement rate limiting

### 4. Browser-Based Attacks

**Description:** Attacker uses browser automation (like QR-SHIELD) to automate QR capture.

**Attack Methods:**

- Automated QR detection and capture

- Batch session hijacking

- Coordinated credential stuffing

- Large-scale account takeover

**Impact:** Widespread account compromise

**Defense:**

- Detect browser automation

- Limit QR display frequency

- Implement CAPTCHAs

- Monitor automated access patterns

### 5. Reverse Engineering

**Description:** Attacker studies QR authentication to find vulnerabilities.

**Attack Process:**

- Analyze QR code encoding

- Study token structure

- Find predictable tokens

- Exploit weak cryptography

**Impact:** Session prediction, token forgery

**Defense:**

- Use strong cryptography

- Generate unpredictable tokens

- Use short token expiration

- Implement token binding

## Threats to QR-SHIELD

### 1. Misuse for Unauthorized Access

**Threat:** QR-SHIELD is used to access accounts without authorization.

**Likelihood:** High

**Impact:** Critical

**Mitigation:**

- Clear terms of service and disclaimer

- User agreement requiring authorized testing

- Documentation of ethical guidelines

- Legal compliance documentation

### 2. Malware Distribution

**Threat:** QR-SHIELD modified to distribute malware.

**Likelihood:** Low-Medium

**Impact:** Critical

**Mitigation:**

- Code signing (future)

- Repository verification

- Build verification

- Dependency monitoring

### 3. Supply Chain Attack

**Threat:** Compromised dependency introduces vulnerability.

**Likelihood:** Low

**Impact:** High

**Mitigation:**

- Dependency pinning

- Dependency scanning (Dependabot)

- Security advisories

- Regular updates

### 4. Code Injection

**Threat:** Vulnerability in QR-SHIELD code allows injection attacks.

**Likelihood:** Low

**Impact:** High

**Mitigation:**

- Code review process

- Security scanning (CodeQL)

- Input validation

- Output encoding

### 5. Data Leakage

**Threat:** Session data leaked from `sessions/` directory.

**Likelihood:** Medium

**Impact:** High

**Mitigation:**

- File permissions enforcement

- Encryption recommendations

- Secure deletion guidance

- User documentation

### 6. Session File Corruption

**Threat:** Sessions corrupted due to bugs or edge cases.

**Likelihood:** Low

**Impact:** Low-Medium

**Mitigation:**

- Input validation

- Error handling

- Session backup capability

- User warnings

## Threat Matrix

| Threat | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| QR hijacking | High | Critical | 2FA, monitoring, detection |
| Phishing via QR | High | High | Training, validation, alerts |
| Interception | Medium | High | HTTPS, CSRF protection, rate limiting |
| Browser automation attacks | Medium | High | Bot detection, rate limiting, CAPTCHAs |
| Reverse engineering | Medium | Medium | Strong crypto, token binding, expiration |
| Misuse for unauthorized access | High | Critical | Disclaimer, legal agreement, ethics docs |
| Malware distribution | Low | Critical | Code signing, verification, scanning |
| Supply chain attack | Low | High | Dependency scanning, pinning, updates |
| Code injection | Low | High | Code review, security scanning, validation |
| Data leakage | Medium | High | File permissions, encryption, user docs |
| Session corruption | Low | Medium | Validation, error handling, backups |

## Attacker Profiles

### Profile 1: Opportunistic Attacker

**Motive:** Quick credential theft

**Capabilities:** Basic technical skills

**Methods:**

- Simple phishing

- Uses QR-SHIELD as-is

**Defense:** User training, 2FA

### Profile 2: Targeted Attacker

**Motive:** Compromise specific account

**Capabilities:** Moderate technical skills

**Methods:**

- Sophisticated phishing

- Custom attack workflow

- Persistence techniques

**Defense:** Advanced 2FA, anomaly detection

### Profile 3: Advanced Threat

**Motive:** Large-scale compromise or espionage

**Capabilities:** High technical skills

**Methods:**

- Custom QR-SHIELD modifications

- Infrastructure setup

- Large-scale automation

**Defense:** Detection engineering, incident response

## Attack Scenarios

### Scenario 1: Discord Account Compromise

**Attacker Steps:**

1. Sends phishing email with QR code link

1. Victim clicks link, scans QR with Discord app

1. Attacker captures session with QR-SHIELD

1. Attacker logs in as victim

1. Attacker sends messages or accesses private channels

**Defensive Measures:**

- User training (recognize phishing)

- Rate limiting (detect QR overuse)

- 2FA (prevent login without second factor)

- Anomaly detection (flag unusual access)

### Scenario 2: Batch Account Takeover

**Attacker Steps:**

1. Sends mass phishing with QR codes

1. Collects QR scans from victims

1. Automates session capture with QR-SHIELD

1. Performs reconnaissance on compromised accounts

1. Exports or monetizes data

**Defensive Measures:**

- Bot detection (block QR-SHIELD-like automation)

- Rate limiting (per-user and per-IP)

- CAPTCHAs (add friction)

- Compromised credential detection

- Detection rules for mass login patterns

### Scenario 3: Insider Threat

**Attacker Steps:**

1. Insider with access to systems

1. Uses QR-SHIELD to compromise test accounts

1. Escalates privileges

1. Steals data

1. Covers tracks

**Defensive Measures:**

- Access logging and monitoring

- Privileged access management (PAM)

- Endpoint detection and response (EDR)

- Behavioral analytics

## Detection Strategies

### Behavioral Detection

**Indicators:**

- Rapid QR code displays to same user

- QR scans from unusual locations

- Multiple QR scans in short timeframe

- Automated QR interaction patterns

**Implementation:**

- Monitor QR display frequency

- Geolocate scans

- Implement rate limiting

- Detect browser automation

### Technical Detection

**Indicators:**

- Selenium user agent

- Common browser automation patterns

- Modified Firefox profiles

- Unusual HTTP patterns

**Implementation:**

- User agent blocking

- Browser fingerprinting

- Session analysis

- Network monitoring

### Behavioral Analysis

**Indicators:**

- Login from unusual locations

- Unusual activity timing

- Atypical API usage

- Message/data access patterns

**Implementation:**

- User behavior analytics (UBA)

- Machine learning models

- Baseline establishment

- Anomaly detection

## Risk Assessment

### High-Risk Scenarios

1. **OAuth Integration with QR** - QR codes used for OAuth login

1. **Enterprise VPN QR** - QR codes for VPN access

1. **Crypto Wallet QR** - QR codes for crypto operations

1. **Financial Transaction QR** - QR codes authorizing payments

### Remediation

For high-risk scenarios:

- Implement multi-factor authentication

- Use additional verification

- Implement transaction limits

- Enable detailed logging

## Recommendations

### For Developers

1. Never use QR codes as sole authentication factor

1. Implement additional verification steps

1. Use short-lived tokens

1. Implement rate limiting

1. Log all QR interactions

1. Detect browser automation

### For Defenders

1. Monitor QR code usage

1. Implement detection rules

1. Train users on phishing

1. Implement 2FA for all users

1. Monitor access patterns

1. Regular security assessments

### For Researchers

1. Study QR authentication mechanisms

1. Develop detection capabilities

1. Share findings responsibly

1. Contribute to threat intelligence

1. Build defensive tools

---

For more information see:

- [SECURITY.md](../SECURITY.md)

- [ETHICS.md](../ETHICS.md)

- [ARCHITECTURE.md](architecture.md)

---

**Last Updated:** July 2026
