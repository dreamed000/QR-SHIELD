# Roadmap

## Project Vision

QR-SHIELD aims to be a leading open-source framework for understanding and defending against QR code-based security threats. Our roadmap reflects a commitment to advancing research capability and defensive security.

## Current Status: Version 1.0.0

**Release Date:** July 2026

**Stability:** Stable for Research Use

### Version 1.0.0 Features

- ✅ Selenium 4 browser automation

- ✅ Python 3.10+ support

- ✅ Multi-platform module system (Discord, WhatsApp, Signal, Telegram)

- ✅ Session capture and replay

- ✅ Interactive CLI framework

- ✅ Development and debug modes

---

## Planned Development

### Phase 1: Core Enhancement (Q3-Q4 2026)

#### 1.1: Additional Platform Support

**Goal:** Expand to more messaging platforms

**Target Platforms:**

- Instagram Direct Messages

- LinkedIn Messaging

- Telegram Web (additional methods)

- Slack Web Integration

- Microsoft Teams

**Effort:** High priority

**Impact:** Broader threat research coverage

#### 1.2: XPath Selector Maintenance

**Goal:** Automated selector validation and updates

**Features:**

- Selector validation script

- Automated testing against live platforms

- GitHub Actions for CI validation

- Fallback selector suggestions

**Effort:** Medium priority

**Impact:** Improved maintainability

#### 1.3: Enhanced Session Management

**Goal:** Better session handling and organization

**Features:**

- Session metadata and tagging

- Session expiration tracking

- Session comparison tools

- Batch session operations

**Effort:** Medium priority

**Impact:** Improved usability

### Phase 2: Detection and Defense (Q1-Q2 2027)

#### 2.1: Defensive Detection Patterns

**Goal:** Provide detection engineering resources

**Deliverables:**

- Detection signature examples

- Behavioral anomaly detection documentation

- Alert configuration templates

- Integration guides for SIEM

**Effort:** High priority

**Impact:** Enable defender implementations

#### 2.2: Threat Intelligence Integration

**Goal:** Integrate with threat intelligence platforms

**Integrations:**

- MISP (Malware Information Sharing Platform)

- ATT&CK Framework mapping

- CVE tracking

- Threat actor attribution

**Effort:** Medium priority

**Impact:** Contextualize threats

#### 2.3: User Awareness Materials

**Goal:** Defensive security awareness training

**Materials:**

- Phishing simulation guides

- User training modules

- Awareness campaign templates

- Security education resources

**Effort:** Medium priority

**Impact:** Improve broader security awareness

### Phase 3: Research Infrastructure (Q3-Q4 2027)

#### 1.1: API Server

**Goal:** RESTful API for programmatic access

**Features:**

- Module execution via API

- Session management API

- Authentication tokens

- Rate limiting

- OpenAPI documentation

**Effort:** High effort

**Impact:** Enable integration with other tools

#### 1.2: Database Backend

**Goal:** Centralized session and result storage

**Capabilities:**

- PostgreSQL support

- Query interface

- Historical tracking

- Reporting capabilities

**Effort:** High effort

**Impact:** Improve scalability

#### 1.3: Web Dashboard

**Goal:** Visual interface for research management

**Features:**

- Session browser

- Module management UI

- Result visualization

- Campaign tracking

**Effort:** High effort

**Impact:** Improve usability

### Phase 4: Advanced Capabilities (2027+)

#### 4.1: Machine Learning Integration

**Goal:** AI-assisted detection and defense

**Applications:**

- Anomaly detection training

- Detection and response optimization

- Pattern recognition

- Threat classification

**Status:** To be evaluated

#### 4.2: Containerization

**Goal:** Docker and Kubernetes support

**Features:**

- Docker image

- Kubernetes manifests

- Distributed operation

- Cloud deployment

**Status:** Under consideration

#### 4.3: Mobile Platform Support

**Goal:** Mobile app research capabilities

**Platforms:**

- WhatsApp mobile

- Signal mobile

- Telegram mobile

- Discord mobile

**Status:** Requires significant research

---

## Community Contributions

### Welcome Contributions In

- ✅ Additional platform modules

- ✅ Bug fixes and improvements

- ✅ Documentation enhancements

- ✅ Test coverage expansion

- ✅ Security hardening

- ✅ Performance optimization

- ✅ Translation and localization

### How to Propose Features

1. **Open a GitHub Issue** - Describe your feature idea

1. **Link to Roadmap** - Reference this document

1. **Provide Context** - Explain use cases and benefits

1. **Discuss Impact** - Share defensive security implications

1. **Volunteer** - Offer to help implement

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## Dependencies and Upstream

### Selenium Updates

QR-SHIELD depends on Selenium for browser automation.

- **Current Version:** 4.20+

- **Support Policy:** Update within 6 months of Selenium release

- **Compatibility:** Maintain Python 3.10+ support

### Firefox Updates

Firefox is the target browser for QR-SHIELD.

- **Support Policy:** Compatible with Firefox ESR and latest

- **Feature Requirements:** Must support WebDriver protocol

- **Maintenance:** Test quarterly with latest Firefox

### Python Support

- **Current:** Python 3.10, 3.11, 3.12

- **Support Policy:** Drop support 6 months after EOL

- **Testing:** CI/CD tests against all supported versions

---

## Maintenance Commitments

### Bug Fix SLA

| Severity | Target | Timeframe |
| --- | --- | --- |
| Critical | Fix & Release | 24-48 hours |
| High | Fix & Release | 7 days |
| Medium | Fix & Release | 30 days |
| Low | Fix in next | 90 days |

### Security Updates

- **Critical:** 24-48 hours to patch

- **High:** 7 days to patch

- **Review:** Coordinate with responsible disclosure

### Documentation

- **Update Frequency:** With each release

- **Maintenance:** Quarterly review

- **Accuracy:** Community feedback welcome

---

## Release Schedule

### Version Planning

- **Major Version (X.0.0):** Annual or as-needed

- **Minor Version (1.X.0):** Quarterly or feature-driven

- **Patch Version (1.0.X):** As-needed for fixes

- **Security Releases:** ASAP

### Supported Versions

```text
Version   Status        EOL Date
1.0.x     Active        TBD
0.x       Maintenance   TBD
```

### Release Process

1. **Planning** - Feature/fix collection

1. **Development** - Implementation and testing

1. **RC Release** - Release candidate for testing

1. **Final Release** - Full version release

1. **Documentation** - Update all references

---

## Known Limitations

### Current Limitations

1. **Single-threaded CLI** - Sequential command execution

1. **Local Storage Only** - No cloud storage support

1. **Firefox Only** - Chrome/Edge not supported

1. **Limited Platforms** - Only Discord, WhatsApp, Signal, Telegram

1. **Manual Updates** - XPath selectors require manual maintenance

### Planned Solutions

- ✓ Multi-threaded operation (Phase 3)

- ✓ Database backend (Phase 3)

- ✓ Additional platforms (Phase 1)

- ✓ Automated selector validation (Phase 1)

---

## Breaking Changes

### Version 1.x to 2.x (Planned for 2027)

Potential breaking changes under discussion:

- Module system redesign

- Configuration format changes

- API changes

- Deprecation of legacy patterns

**Notice:** 12 months advance warning will be provided.

---

## Experimental Features

### Currently Experimental

- Development mode (`--dev` flag)

- Verbose logging (`--verbose` flag)

- Debug mode (`--debug` flag)

These may change significantly in future versions.

### Future Experimental Features

- API server (tentative Phase 3)

- Web dashboard (tentative Phase 3)

- ML integration (tentative Phase 4)

---

## Research Priorities

### Active Research Areas

1. **QR Code Detection** - Improve selector reliability

1. **Session Hijacking** - Understand post-exploit behavior

1. **Evasion Techniques** - Study detection circumvention

1. **Defense Mechanisms** - Develop detection patterns

1. **Awareness** - Build security education materials

### Community Research Opportunities

- Module development for new platforms

- Detection mechanism research

- Threat intelligence analysis

- Security awareness content creation

- Academic publication support

---

## Success Metrics

### Project Success Indicators

- **Adoption:** Growing research community usage

- **Contributions:** Community-submitted modules and features

- **Citations:** Academic and industry references

- **Defenses:** Tools developed using QR-SHIELD insights

- **Awareness:** Improved security consciousness

### Quality Metrics

- **Test Coverage:** 80%+ code coverage goal

- **Documentation:** 100% API documentation

- **Responsiveness:** <48 hour issue response

- **Uptime:** Zero security incidents

- **Community:** Positive feedback and engagement

---

## Getting Involved

### How You Can Help

1. **Test:** Use QR-SHIELD and report issues

1. **Contribute:** Submit code and modules

1. **Document:** Improve documentation

1. **Research:** Publish findings

1. **Teach:** Share knowledge with others

1. **Feedback:** Tell us what you need

### Contribution Areas by Difficulty

| Difficulty | Tasks |
| --- | --- |
| Easy | Documentation, typos, small fixes |
| Medium | Bug fixes, module updates, tests |
| Hard | New modules, core features, architecture |
| Very Hard | API server, database, web dashboard |

---

## Long-Term Vision

### 5-Year Goals (2029)

- Widely-adopted research framework

- Standard tool in security research organizations

- Integration with major security platforms

- Academic publication of findings

- Measurable improvement in QR security

- Large, active research community

### 10-Year Goals (2034)

- QR code security significantly improved industry-wide

- Detection mechanisms widely deployed

- Research findings integrated into standards

- Educational adoption in universities

- Continued evolution as threats change

---

## Feedback on Roadmap

### Share Your Input

We welcome feedback on this roadmap:

- Open a GitHub Issue with your ideas

- Participate in GitHub Discussions

- Email feedback to maintainers

- Contribute to roadmap priorities

Your voice shapes the project's future.

---

---

**Last Updated:** July 2026

**Next Review:** Q4 2026

For current status and issues, see [GitHub Issues](https://github.com/dreamed000/QR-SHIELD/issues).
