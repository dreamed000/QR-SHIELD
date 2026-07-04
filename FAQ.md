# Frequently Asked Questions

## Installation & Setup

### Q: What Python version do I need?

**A:** Python 3.10 or later. QR-SHIELD requires modern Python features. Check your version:

```bash
python --version
```

### Q: Do I need to use a virtual environment?

**A:** It's strongly recommended to isolate dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Q: Firefox isn't detected. What do I do?

**A:** Set the Firefox path explicitly:

```bash
export QRSHIELD_FIREFOX_BINARY="/path/to/firefox"
python qrshield.py
```

On Windows use:

```powershell
$env:QRSHIELD_FIREFOX_BINARY="C:\Program Files\Mozilla Firefox\firefox.exe"
```

### Q: Can I use Chrome or Edge instead of Firefox?

**A:** Currently only Firefox is supported. Chrome/Edge support is planned for a future release. See [ROADMAP.md](ROADMAP.md).

---

## Usage Questions

### Q: How do I capture a Discord session?

**A:**

```text
qrshield> use grabber/discord
qrshield> run
# A browser opens showing Discord login with QR code
# Scan the QR with your phone's Discord app to capture the session
```

### Q: Where are captured sessions stored?

**A:** In the `sessions/` directory organized by platform:

```text
sessions/
├── discord/[session_id]/localstorage.json
├── whatsapp/[session_id]/firefox_profile/
├── signal/[session_id]/localstorage.json
└── telegram/[session_id]/localstorage.json
```

### Q: How do I use a captured session?

**A:**

```text
qrshield> sessions -l                    # Find your session ID
qrshield> use post/discord
qrshield> set session_id [your_id]
qrshield> run
# Browser opens with logged-in session
```

### Q: Can I use the same session multiple times?

**A:** Yes, sessions persist until you delete them. List sessions:

```text
qrshield> sessions -l
```

### Q: How do I delete a session?

**A:**

```text
qrshield> sessions -d [session_id]
```

### Q: What's the difference between grabber and post modules?

**A:**

- **Grabber:** Captures new sessions by capturing QR codes

- **Post:** Uses already-captured sessions to interact with accounts

---

## Technical Questions

### Q: What's a QR code session hijacking?

**A:** It's capturing authentication tokens during QR-based login to impersonate users. See [THREAT_MODEL.md](THREAT_MODEL.md).

### Q: How does QR-SHIELD extract QR codes?

**A:** Using XPath selectors to locate canvas/img elements in the browser DOM, then extracting and decoding the image data.

### Q: Why use Selenium instead of direct HTTP requests?

**A:** Many login flows require JavaScript execution and interactive elements that pure HTTP can't handle. Selenium automates a real browser.

### Q: Can QR-SHIELD be detected?

**A:** It can be detected like any browser automation. It uses standard Firefox and doesn't hide all fingerprints. This is research tool, not an evasion tool.

### Q: What if a platform updates their DOM?

**A:** XPath selectors break. Report the issue on GitHub. Contributors can update selectors. You can modify selectors locally in module files.

---

## Ethical & Legal Questions

### Q: Is using QR-SHIELD legal?

**A:** It depends on how you use it:

- ✅ Legal: Testing systems you own with authorization

- ❌ Illegal: Unauthorized access, phishing, fraud

See [ETHICS.md](ETHICS.md) and [DISCLAIMER.md](DISCLAIMER.md).

### Q: Can I use QR-SHIELD for educational purposes?

**A:** Yes, for learning about security threats and defenses in academic settings with proper ethics board approval.

### Q: What's the author's responsibility if misused?

**A:** None. See [DISCLAIMER.md](DISCLAIMER.md). Users are solely responsible for legal compliance.

### Q: Should I report findings?

**A:** Yes, use responsible disclosure. See [RESPONSIBLE_DISCLOSURE.md](RESPONSIBLE_DISCLOSURE.md).

### Q: Can I use QR-SHIELD commercially?

**A:** Commercial use requires a separate Commercial License. See [COMMERCIAL-LICENSE.md](COMMERCIAL-LICENSE.md) for the conditions that apply to commercial integration, SaaS, consulting, managed services, OEM licensing, enterprise deployment, and redistribution.

---

## Troubleshooting

### Q: QR code detection fails. Why?

**A:** Possible causes:

1. Platform updated DOM - XPath selectors don't match

1. QR code isn't rendering (script error)

1. Page taking too long to load (increase timeout)

1. Browser automation detected and blocked

**Solution:**

```bash
python qrshield.py --verbose --debug
```

Check the output for specific errors.

### Q: Firefox crashes when running modules

**A:** Try:

```bash
# Update Firefox
firefox --version

# Update Selenium
pip install --upgrade selenium

# Increase timeout
qrshield> set timeout 60

# Run in debug mode
python qrshield.py --debug
```

### Q: Module is stuck/hangs

**A:** Modules hang waiting for user input:

1. Complete the action (scan QR with phone)

1. Or press Ctrl+C to cancel

If genuinely stuck:

```text
qrshield> jobs
qrshield> jobs -k [job_id]
```

### Q: I got a "port already in use" error

**A:** Another process is using that port:

```text
qrshield> set port 8001
qrshield> run
```

Or find and stop the other process.

### Q: Sessions not restoring properly

**A:** Check:

1. Session ID is correct: `sessions -l`

1. Session file exists: `ls sessions/platform/[id]/`

1. Try with `--debug` mode

1. Session may be corrupted - try another

---

## Contributing & Development

### Q: How do I contribute?

**A:** See [CONTRIBUTING.md](CONTRIBUTING.md). Start with:

1. Understanding the codebase

1. Check [ARCHITECTURE.md](ARCHITECTURE.md)

1. Fork on GitHub

1. Make improvements

1. Submit pull request

### Q: How do I add a new platform module?

**A:** Create a module following the pattern in existing modules:

```python
# core/modules/grabber/yourplatform.py
class info:
    author = "Your Name"
    short_description = "Description"

class execution:
    module_type = types.grabber
    name = "yourplatform"
    url = "https://platform.url"
    image_xpath = '//your/xpath'
    change_identifier = '//post-login/element'
    
    @staticmethod
    def run(global_options, visible_browser):
        # Implementation
        pass
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Q: How do I report bugs?

**A:**

1. Check [existing issues](https://github.com/dreamed000/QR-SHIELD/issues)

1. Provide clear reproduction steps

1. Include error messages and logs

1. Specify your environment (OS, Python, Firefox version)

### Q: Can I fork QR-SHIELD?

**A:** Yes, under the Community Research License for permitted research and defensive use. Commercial use requires a separate Commercial License.

---

## Performance & Optimization

### Q: How do I make modules run faster?

**A:**

- Use headless mode: `set headless true`

- Lower timeout: `set timeout 20` (if connection is fast)

- Use development mode: `python qrshield.py --dev`

### Q: Can I run multiple modules in parallel?

**A:** Not currently. QR-SHIELD is single-threaded by design. Parallel execution is planned for Phase 3.

### Q: How much disk space do sessions use?

**A:** Typically 100KB - 5MB per session depending on storage type and account size.

---

## Security & Privacy

### Q: How are sessions stored?

**A:** In the local `sessions/` directory with file permissions. On Unix systems:

- Owner can read/write

- Others cannot access

On Windows, NTFS permissions apply.

### Q: Are sessions encrypted?

**A:** No, by default. For sensitive research, encrypt the `sessions/` directory using OS-level encryption (BitLocker, FileVault, etc.).

### Q: Can I securely delete sessions?

**A:**

```bash
shred -vfz sessions/platform/[session_id]  # Linux
srm sessions/platform/[session_id]          # macOS
cipher /w:[drive]                           # Windows (full drive)
```

### Q: What data does QR-SHIELD collect about me?

**A:** Nothing. QR-SHIELD runs locally. It doesn't phone home or collect telemetry.

---

## Documentation & Help

### Q: Where do I find documentation?

**A:**

| Document | Purpose |
| --- | --- |
| [README.md](README.md) | Overview |
| [INSTALL.md](INSTALL.md) | Installation |
| [USAGE.md](USAGE.md) | How to use |
| [ARCHITECTURE.md](ARCHITECTURE.md) | How it works |
| [THREAT_MODEL.md](THREAT_MODEL.md) | Threat analysis |
| [SECURITY.md](SECURITY.md) | Security info |
| [ETHICS.md](ETHICS.md) | Ethical use |

### Q: How do I ask questions?

**A:**

1. Check this FAQ

1. Read relevant documentation

1. Open a GitHub Discussion

1. Check GitHub Issues

1. Email support (see [SUPPORT.md](SUPPORT.md))

### Q: How long does it take to get a response?

**A:** See [SUPPORT.md](SUPPORT.md) for response time expectations.

---

## Platform-Specific

### Q: Can I run QR-SHIELD on Windows?

**A:** Yes, fully supported. Use PowerShell or CMD.

### Q: Can I run on macOS?

**A:** Yes. Note M1/M2 Macs need native Python 3.10+.

### Q: Can I run on Linux?

**A:** Yes, all major distributions supported.

### Q: Does it work on Raspberry Pi?

**A:** Not officially tested. Low RAM and ARM architecture may cause issues. Try at your own risk.

---

## Version & Updates

### Q: What version am I running?

**A:**

```bash
cat core/Data/version.txt
# or
python qrshield.py -x "help"  # Version shown in banner
```

### Q: How do I update to the latest version?

**A:**

```bash
cd /path/to/qr-shield
git pull origin main
pip install -r requirements.txt
```

### Q: What's the difference between versions?

**A:** See [CHANGELOG.md](CHANGELOG.md) for release notes.

### Q: When will Version 4.0 be released?

**A:** See [ROADMAP.md](ROADMAP.md) for planned releases.

---

## Advanced Questions

### Q: Can I use QR-SHIELD as a library in my code?

**A:** Experimental. QR-SHIELD is primarily a CLI tool. Programmatic API is planned for Phase 3 (see [ROADMAP.md](ROADMAP.md)).

### Q: Can I deploy QR-SHIELD on a server?

**A:** Not recommended. QR-SHIELD requires user interaction (scanning QR codes). Desktop use is intended.

### Q: Can I run QR-SHIELD headless on a server?

**A:** Technically yes, but user still needs to scan QR codes. Remote automation is beyond current scope.

### Q: How do I extend QR-SHIELD?

**A:** Create modules. See [CONTRIBUTING.md](CONTRIBUTING.md) and [ARCHITECTURE.md](ARCHITECTURE.md).

---

## Still Have Questions?

- Check [SUPPORT.md](SUPPORT.md)

- Open a [GitHub Discussion](https://github.com/dreamed000/QR-SHIELD/discussions)

- Report an [Issue](https://github.com/dreamed000/QR-SHIELD/issues)

- Email support (see SUPPORT.md)

---

**Last Updated:** July 2026

**Didn't find your question? Ask in GitHub Discussions!**
