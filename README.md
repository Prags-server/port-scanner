# 🔐 Network Port Scanner & Security Reporter

**A production-grade Python tool that mimics SOC (Security Operations Center) engineer workflows**

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Security](https://img.shields.io/badge/Security-Port%20Scanning-red.svg)](https://owasp.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📋 Overview

This tool automates what SOC engineers do daily: scanning networks for open ports, identifying running services, classifying security risks, and generating professional reports. It combines socket-based port scanning with intelligent service identification and risk assessment.

### Key Features

✅ **Socket-Based Port Scanning** - Direct TCP connections to identify open ports  
✅ **Service Identification** - Automatically identifies 25+ common services  
✅ **Risk Classification** - Intelligent risk levels (CRITICAL, HIGH, MEDIUM, LOW)  
✅ **Colour-Coded Output** - Terminal output with visual risk indicators  
✅ **Structured Reports** - Professional .txt reports for compliance/documentation  
✅ **Multi-Threaded Scanning** - Fast concurrent scanning with configurable threads  
✅ **Flexible Port Selection** - Scan common ports, custom ports, or all 65535  
✅ **Production-Ready** - Robust error handling and argument validation

---

## 🛠️ Installation

### Requirements

- Python 3.8 or higher
- Linux, macOS, or Windows
- No external dependencies (uses only Python standard library)

### Setup

```bash
# Clone or download the repository
git clone https://github.com/yourusername/port-scanner.git
cd port-scanner

# Make the script executable (Linux/macOS)
chmod +x port_scanner.py

# Run directly (Python will find the script)
python port_scanner.py --help
```

---

## 🚀 Usage

### Basic Scan (Common Ports)

Scan the 25 most commonly attacked ports on a target:

```bash
python port_scanner.py 192.168.1.1
```

**Output:**

- Colour-coded terminal display
- Saved report in `reports/` directory

---

### Custom Port Scanning

Scan specific ports:

```bash
python port_scanner.py 10.0.0.5 -p 22,80,443,3306,5432
```

---

### Aggressive Scanning

Scan all 65535 ports (⚠️ slow, use cautiously):

```bash
python port_scanner.py 172.16.0.1 --all-ports
```

---

### Performance Tuning

Adjust thread count for faster/slower scanning:

```bash
# Faster (100 concurrent threads)
python port_scanner.py 192.168.1.1 -t 100

# Slower, more reliable (20 threads)
python port_scanner.py 192.168.1.1 -t 20
```

---

### Advanced Options

```bash
# Custom output filename
python port_scanner.py 192.168.1.1 -o custom_report.txt

# Report only (suppress terminal output)
python port_scanner.py 192.168.1.1 --quiet

# Combine options
python port_scanner.py 10.0.0.5 -p 22,80,443,8080,8443 -t 50 -o security_audit.txt
```

---

## 📊 Output Example

### Terminal Output

```
╔════════════════════════════════════════════════════════════════╗
║       NETWORK PORT SCANNER & SECURITY REPORTER v1.0           ║
╚════════════════════════════════════════════════════════════════╝

Target: 192.168.1.100
Scan Date: 2026-04-24 14:32:15
Total Ports Scanned: 25
Open Ports Found: 8

═══════════════════════════════════════════════════════════════
PORT     SERVICE         DESCRIPTION                   RISK
═══════════════════════════════════════════════════════════════
6379     Redis           Redis Cache                    CRITICAL
27017    MongoDB         MongoDB Database               CRITICAL
22       SSH             Secure Shell                   LOW
80       HTTP            HyperText Transfer Protocol    LOW
443      HTTPS           Secure HyperText...            LOW
3306     MySQL           MySQL Database                 HIGH
5432     PostgreSQL      PostgreSQL Database            HIGH
5900     VNC             Virtual Network Computing      HIGH
═══════════════════════════════════════════════════════════════

RISK SUMMARY:
  ● CRITICAL: 2
  ● HIGH: 3
  ● LOW: 3

⚠️  RECOMMENDATION: Review and close unnecessary open ports!
```

### Report File

A detailed .txt report is automatically saved to `reports/` with:

- Scan metadata
- Risk assessment summary
- Detailed port information
- Security recommendations
- Compliance-ready formatting

---

## 🔍 Supported Services (25+ Common Ports)

| Port             | Service    | Risk        | Category      |
| ---------------- | ---------- | ----------- | ------------- |
| 21               | FTP        | 🔴 CRITICAL | File Transfer |
| 22               | SSH        | 🟢 LOW      | Remote Access |
| 23               | Telnet     | 🔴 CRITICAL | Remote Access |
| 80               | HTTP       | 🟢 LOW      | Web           |
| 443              | HTTPS      | 🟢 LOW      | Web           |
| 445              | SMB        | 🟡 HIGH     | File Sharing  |
| 3306             | MySQL      | 🟡 HIGH     | Database      |
| 3389             | RDP        | 🟡 HIGH     | Remote Access |
| 5432             | PostgreSQL | 🟡 HIGH     | Database      |
| 6379             | Redis      | 🔴 CRITICAL | Cache         |
| 27017            | MongoDB    | 🔴 CRITICAL | Database      |
| ... and 15+ more |            |             |               |

See `port_scanner.py` for complete port database.

---

## 🎯 Use Cases

### 1. **Security Auditing**

Identify exposed services that should be restricted or patched.

```bash
python port_scanner.py 10.0.0.0 -p 22,3306,5432,27017
```

### 2. **Compliance Verification**

Generate reports for security assessments and compliance checks.

```bash
python port_scanner.py 192.168.1.50 --all-ports -o compliance_report.txt
```

### 3. **Internal Network Hardening**

Scan internal systems to find unnecessary open ports.

```bash
python port_scanner.py 172.16.0.0 -t 100  # Fast scan with many threads
```

### 4. **Incident Response**

Quickly assess what services are running when investigating a compromised system.

```bash
python port_scanner.py 192.168.1.1 --quiet  # Get report without noise
```

---

## 📈 SOC Workflow Integration

This tool replicates real SOC workflows:

```
1. Asset Discovery → 2. Port Enumeration → 3. Service Identification →
4. Risk Classification → 5. Report Generation → 6. Remediation Tasks
```

Professional SOC teams use similar tools daily to:

- Monitor network attack surface
- Validate security policies
- Investigate suspicious connections
- Document infrastructure inventory
- Track compliance requirements

---

## ⚙️ Technical Details

### Architecture

```
port_scanner.py
├── Colour Class           → ANSI terminal formatting
├── PORT_DATABASE          → Service metadata & risk classification
├── Scanning Functions     → Socket operations & threading
├── Output Formatters      → Terminal & report generation
└── Main Entry Point       → CLI argument parsing
```

### Threading Model

- Configurable worker threads (default: 50)
- Concurrent socket connections
- Thread-safe result collection
- Automatic timeout handling

### Risk Classification Logic

- **CRITICAL**: Services with known default vulnerabilities (Redis, MongoDB)
- **HIGH**: Databases and remote access that shouldn't be exposed
- **MEDIUM**: Email and less-critical services
- **LOW**: Standard web services and secure protocols

---

## 🔒 Security Considerations

### ⚠️ Legal & Ethical Use

- **Only scan networks you own or have permission to test**
- Unauthorized port scanning may be illegal in your jurisdiction
- Use for authorized security assessments only
- Always document permission for compliance

### Operational Security

- Scans may be detected by IDS/IPS systems
- High thread counts may create network noise
- Always inform network administrators before scanning
- Test on internal/lab networks first

---

## 🐛 Troubleshooting

### Issue: "Invalid IP address"

```bash
# ✓ Correct format
python port_scanner.py 192.168.1.1

# ✗ Incorrect
python port_scanner.py 192.168.1
python port_scanner.py example.com  # Use IP, not hostname
```

### Issue: "Permission Denied" on Linux

```bash
sudo python port_scanner.py 192.168.1.1
# OR
chmod +x port_scanner.py
./port_scanner.py 192.168.1.1
```

### Issue: Slow Scanning

```bash
# Increase threads and use custom port list
python port_scanner.py 192.168.1.1 -p 22,80,443,3306 -t 100
```

### Issue: Too Many False Positives

```bash
# Reduce thread count to avoid timeouts
python port_scanner.py 192.168.1.1 -t 20
```

---

## 📝 How It Works

### 1. Port Scanning

```python
# Creates TCP socket and attempts connection
socket.connect_ex((host, port))  # Returns 0 if open
```

### 2. Service Identification

```python
# Looks up port in PORT_DATABASE
port_info = PORT_DATABASE.get(port)
```

### 3. Risk Classification

```python
# Risk levels based on service exposure risk
"CRITICAL" → Redis/MongoDB exposed
"HIGH" → Databases/RDP exposed
```

### 4. Report Generation

```python
# Formats results and saves to file
# Includes metadata, recommendations, compliance info
```

---

## 🤝 Contributing

Contributions welcome! Areas for enhancement:

- Service version detection via banner grabbing
- IPv6 support
- CIDR range scanning
- Additional service database entries
- Firewall detection
- XML/JSON report formats

---

## 📜 License

MIT License - See LICENSE file for details

---

## 🎓 Learning Resources

**Understanding Port Scanning:**

- [OWASP: Port Scanning](https://owasp.org/)
- [RFC 3629: TCP/IP Illustrated](https://tools.ietf.org/html/rfc793)
- [Nmap Port Scanner Guide](https://nmap.org/)

**SOC Engineering Concepts:**

- Security Onion Documentation
- NIST Cybersecurity Framework
- CIS Controls for Network Security

---

## 💬 Questions & Support

For questions about this project:

1. Check the troubleshooting section above
2. Review the code comments
3. Test with sample IPs first
4. Check README examples

---

**Made with 🔒 for aspiring SOC engineers and security professionals**
