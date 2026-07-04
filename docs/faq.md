# Frequently Asked Questions

Quick answers to common questions about QR-SHIELD.

For detailed FAQ, see [FAQ.md](../FAQ.md).

## Installation

**Q: What Python version do I need?**

A: Python 3.10, 3.11, or 3.12. Check with `python --version`

**Q: How do I install?**

A: Clone, create virtual env, install requirements:

```bash
git clone https://github.com/dreamed000/QR-SHIELD.git
cd QR-SHIELD
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Q: Firefox isn't found**

A: Set Firefox path:

```bash
export QRSHIELD_FIREFOX_BINARY="/path/to/firefox"
python qrshield.py
```

## Usage

**Q: How do I capture a session?**

A:

```text
qrshield> use grabber/discord
qrshield> run
# Scan QR with phone
```

**Q: How do I use a captured session?**

A:

```text
qrshield> sessions -l
qrshield> use post/discord
qrshield> set session_id [ID]
qrshield> run
```

**Q: Where are sessions stored?**

A: In `sessions/[platform]/[id]/` directory

**Q: Can I use the same session multiple times?**

A: Yes, until you delete it

## Technical

**Q: Why Firefox only?**

A: Selenium integration is most reliable with Firefox. Chrome support is planned.

**Q: Can I detect QR-SHIELD?**

A: Yes, like any browser automation. It's a research tool, not evasion tool.

**Q: What if a platform updates their DOM?**

A: QR detection breaks. Report it on GitHub for updates.

## Security & Ethics

**Q: Is QR-SHIELD legal?**

A: Legal use: Authorized testing on systems you own or manage
Illegal use: Unauthorized access, deceptive credential collection, fraud

**Q: What if I misuse it?**

A: You're responsible. See [DISCLAIMER.md](../DISCLAIMER.md)

**Q: Should I report findings?**

A: Yes, use responsible disclosure: [RESPONSIBLE_DISCLOSURE.md](../RESPONSIBLE_DISCLOSURE.md)

## Troubleshooting

**Q: Module is stuck/hangs**

A: Complete the action (scan QR) or press Ctrl+C

**Q: "Port already in use" error**

A: Change port: `set port 8001`

**Q: Sessions not restoring**

A: Verify session exists: `sessions -l`
Check with `--debug`: `python qrshield.py --debug`

## Contributing

**Q: How do I contribute?**

A: See [CONTRIBUTING.md](../CONTRIBUTING.md)

- Fork repository

- Make improvements

- Submit pull request

**Q: How do I add a new platform?**

A: Create grabber and post modules following existing patterns
See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guide

**Q: Can I fork QR-SHIELD?**

A: Yes, you may fork QR-SHIELD for Community Research Use. Commercial use of forks requires a separate Commercial License.

---

**Need more help? See:**

- [USAGE.md](../USAGE.md) - Complete usage guide

- [FAQ.md](../FAQ.md) - Detailed FAQ

- [SUPPORT.md](../SUPPORT.md) - Support options

- [GitHub Issues](https://github.com/dreamed000/QR-SHIELD/issues)

---

**Last Updated:** July 2026
