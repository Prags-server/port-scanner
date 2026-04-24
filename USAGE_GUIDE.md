# Port Scanner - Quick Usage Guide

## 🚀 Getting Started in 30 Seconds

### Installation

```bash
# No dependencies needed - just Python 3.8+
python port_scanner.py --help
```

### First Scan

```bash
python port_scanner.py 192.168.1.1
```

---

## 📚 Common Scenarios

### Scenario 1: Quick Security Audit

You need to quickly check what's exposed on your server:

```bash
python port_scanner.py 10.0.0.5
```

This scans 25 common ports. Takes ~30 seconds.

**Output:** Terminal display + automatically saved report

---

### Scenario 2: Deep Security Assessment

You're conducting a comprehensive security assessment:

```bash
python port_scanner.py 172.16.0.1 --all-ports -o comprehensive_audit.txt
```

Scans all 65535 ports. Takes 5-10 minutes depending on network.

---

### Scenario 3: Verify Specific Services

You only care about certain services:

```bash
python port_scanner.py 192.168.1.50 -p 22,3306,5432,27017
```

Checks SSH, MySQL, PostgreSQL, MongoDB. Takes ~10 seconds.

---

### Scenario 4: Fast Network Reconnaissance

You need results quickly (accept some unreliability):

```bash
python port_scanner.py 10.0.0.0 -t 150
```

Uses 150 threads instead of default 50. Much faster.

---

### Scenario 5: Slow Reliable Scan

You want the most accurate results (slower but thorough):

```bash
python port_scanner.py 192.168.1.1 -t 10
```

Uses only 10 threads. Better for unreliable networks.

---

### Scenario 6: Generate Report Only

You just want the report, no terminal spam:

```bash
python port_scanner.py 192.168.1.1 --quiet -o report.txt
```

---

## 🎯 Real-World Use Cases (SOC Context)

### SOC Incident: "We think our database server is compromised"

```bash
# Check what's listening
python port_scanner.py 10.20.30.40 -p 3306,5432,27017,6379
# Generate report for incident log
python port_scanner.py 10.20.30.40 -o incident_20260424.txt
```

### Infrastructure Team: "Verify our new firewall rules"

```bash
# Before: Scan to see what was exposed
python port_scanner.py 192.168.1.100
# After: Scan again to verify rules are enforced
python port_scanner.py 192.168.1.100
# Compare reports
```

### Compliance: "Need documentation of all listening services"

```bash
# Generate professional report
python port_scanner.py 10.0.0.1 --all-ports -o compliance_audit_2026_Q2.txt
```

---

## ⚡ Tips & Tricks

### Tip 1: Batch Scanning Multiple Servers

```bash
for ip in 10.0.0.1 10.0.0.2 10.0.0.3; do
  python port_scanner.py $ip -p 22,80,443 -q -o report_$ip.txt
done
```

### Tip 2: Monitor Same Server Over Time

```bash
# Week 1
python port_scanner.py 192.168.1.50 -o week1_scan.txt

# Week 2 - Compare results
python port_scanner.py 192.168.1.50 -o week2_scan.txt
# diff week1_scan.txt week2_scan.txt
```

### Tip 3: Focus on High-Risk Ports Only

```bash
# Redis, MongoDB, RDP, MySQL, PostgreSQL
python port_scanner.py 192.168.1.1 -p 6379,27017,3389,3306,5432
```

### Tip 4: Parse Output Programmatically

```bash
# Run with --quiet to just get the report
python port_scanner.py 192.168.1.1 --quiet -o output.txt

# Then parse the report file with grep/awk/Python
grep "CRITICAL" output.txt
```

---

## 🔧 Troubleshooting

### Q: "No module named socket" - How to fix?

**A:** Socket is built-in. Make sure you're using Python 3.8+

```bash
python --version  # Should be 3.8+
python3 port_scanner.py 192.168.1.1  # Try python3 instead
```

### Q: Scan is very slow - How to speed up?

**A:** Increase thread count and limit ports

```bash
python port_scanner.py 192.168.1.1 -p 22,80,443,3306,5432 -t 100
```

### Q: Getting timeout errors - How to fix?

**A:** Reduce thread count (less concurrent connections)

```bash
python port_scanner.py 192.168.1.1 -t 20
```

### Q: How do I know if the IP is valid?

**A:** Script validates IP format automatically. Use standard notation:

```bash
✓ python port_scanner.py 192.168.1.1
✓ python port_scanner.py 10.0.0.1
✗ python port_scanner.py 256.1.1.1      # Invalid
✗ python port_scanner.py 192.168        # Invalid (needs 4 octets)
```

---

## 📊 Output Interpretation

### Understanding Risk Levels

🟢 **GREEN (LOW)**: Safe to leave open (SSH, HTTP/HTTPS if properly secured)

- Standard services with good security controls available

🟡 **YELLOW (HIGH)**: Should be restricted (Databases, RDP, VNC)

- These shouldn't be accessible from untrusted networks

🔴 **RED (CRITICAL)**: Immediate action required (Redis, MongoDB exposed)

- Default ports with no authentication = severe vulnerability

### Example Risk Summary

```
● CRITICAL: 2    → Shut these down NOW (6379, 27017)
● HIGH: 3        → Restrict access (3306, 5432, 5900)
● MEDIUM: 0
● LOW: 3         → Acceptable if hardened (22, 80, 443)
```

---

## 📝 Report File Format

Reports are saved to `reports/` folder with format:

```
scan_report_[IP]_[TIMESTAMP].txt
```

Example:

```
scan_report_192_168_1_100_20260424_143215.txt
```

Reports include:

- Scan metadata (target, date, time)
- Risk summary (counts by severity)
- Detailed port information
- Security recommendations
- Compliance-ready formatting

---

## 🎓 Learning Path

**Beginner:**

1. Scan a few machines with default settings
2. Look at the terminal output
3. Read the generated reports
4. Understand risk classification

**Intermediate:**

1. Customize port lists
2. Adjust thread counts for different scenarios
3. Generate reports for compliance documentation
4. Parse reports programmatically

**Advanced:**

1. Integrate into monitoring pipelines
2. Batch scan entire subnets
3. Track changes over time
4. Correlate with other security tools

---

## ✅ Checklist Before Running

- [ ] I have permission to scan this IP
- [ ] Target IP is correctly formatted
- [ ] I understand the purpose of this scan
- [ ] I have administrative/sudo access if needed on Linux
- [ ] Network connectivity is stable
- [ ] I'm not going to scan a production system without approval

---

**Happy scanning! Remember: Only use on networks you own or have explicit permission to test.**
