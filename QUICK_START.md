# 🚀 QUICK START CARD - Project 1 Port Scanner

## ⚡ Get Running in 30 Seconds

```bash
cd c:\Users\prags\OneDrive\Desktop\Cyber Projects\01_Port_Scanner

# Test: Scan common ports on Google DNS
python port_scanner.py 8.8.8.8

# Output:
# 1. Colour-coded terminal display
# 2. Report saved to reports/ folder
```

---

## 📋 Most Common Commands

```bash
# 1. Quick scan (25 common ports)
python port_scanner.py 192.168.1.1

# 2. Scan specific ports (fast)
python port_scanner.py 192.168.1.1 -p 22,80,443,3306,5432

# 3. Dangerous ports check
python port_scanner.py 192.168.1.1 -p 6379,27017,3389

# 4. Full scan (all 65535 ports)
python port_scanner.py 192.168.1.1 --all-ports

# 5. Fast scan with more threads
python port_scanner.py 192.168.1.1 -t 100

# 6. Report only (no terminal spam)
python port_scanner.py 192.168.1.1 --quiet -o report.txt

# 7. Custom output filename
python port_scanner.py 192.168.1.1 -o my_report.txt

# 8. Help menu
python port_scanner.py --help
```

---

## 📂 What's in This Project

```
port_scanner.py          ← The main tool (750 lines, production-ready)
README.md                ← Professional documentation
USAGE_GUIDE.md           ← Real-world examples
LINKEDIN_PORTFOLIO.md    ← Ready-to-post copy
sample_outputs/          ← Example outputs for portfolio
reports/                 ← Where scan results are saved
LICENSE                  ← MIT License
```

---

## 🎯 What Makes This Special

✅ **Security-First Design**: Risk classification (CRITICAL/HIGH/MEDIUM/LOW)
✅ **Professional Output**: Colour-coded terminal + compliance reports
✅ **Real SOC Work**: Mirrors what security engineers do daily
✅ **Production-Ready**: Threading, error handling, validation
✅ **No Dependencies**: Uses only Python standard library
✅ **Well-Documented**: 1500+ lines of docs + code

---

## 📊 Risk Classification Quick Reference

🔴 **CRITICAL** (Act NOW):

- Redis (6379), MongoDB (27017) exposed
- Publicly accessible cache/database

🟡 **HIGH** (Restrict Access):

- MySQL (3306), PostgreSQL (5432), RDP (3389)
- Shouldn't be internet-facing

🟡 **MEDIUM** (Secure It):

- Email services, DNS
- Should have strong auth

🟢 **LOW** (OK if Hardened):

- SSH (22), HTTP (80), HTTPS (443)
- Standard services with proper controls

---

## 💼 For LinkedIn & GitHub

**GitHub Link:** [Create repo and update this]

**LinkedIn Copy:** See `LINKEDIN_PORTFOLIO.md` (ready to post)

**Key Talking Points:**

- "I built what SOC engineers do daily"
- "Production-grade with 750+ lines of clean Python"
- "Demonstrates security thinking + technical execution"
- "Multi-threaded, concurrent, professional reporting"

---

## 🧪 Test Cases (Safe IPs to Test)

```bash
# Public IP (if you have internet)
python port_scanner.py 8.8.8.8

# Local IP (if you're on a network)
python port_scanner.py 192.168.1.1

# Localhost (your own machine)
python port_scanner.py 127.0.0.1
```

---

## ⚠️ Remember

✅ Only scan IPs you own or have permission to test
✅ Unauthorized scanning may be illegal
✅ Get network admin approval before scanning production
✅ Use in authorized testing only

---

## 🎓 Next: Project 2

**Linux Server Hardening Audit Script** (Bash-based)

- Same folder: `02_Linux_Hardening`
- Checks: SSH config, firewall, logins, cron jobs
- Output: PASS/FAIL/WARN report
- Duration: ~35 minutes

Then connect both projects narratively:

1. **Port Scanner** → Discover vulnerabilities
2. **Hardening Script** → Fix them
3. **IR Playbook** → Respond to incidents

---

**You've built production-grade security software. Great work! 🔐**
