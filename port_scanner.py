#!/usr/bin/env python3
"""
Network Port Scanner & Security Reporter
A professional security tool that scans open ports, identifies services, and generates reports.
Mimics SOC engineer workflows with colour-coded output and structured reporting.
"""

import socket
import sys
from datetime import datetime
from typing import Dict, List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
from collections import defaultdict


# ANSI colour codes for terminal output
class Colours:
    """ANSI colour codes for terminal styling"""
    GREEN = '\033[92m'      # Safe ports
    YELLOW = '\033[93m'     # Warning ports
    RED = '\033[91m'        # Critical/Risky ports
    BLUE = '\033[94m'       # Information
    BOLD = '\033[1m'        # Bold text
    RESET = '\033[0m'       # Reset formatting


# Port metadata and risk classification
PORT_DATABASE = {
    20: {"service": "FTP-DATA", "description": "File Transfer Protocol Data", "risk": "HIGH", "category": "File Transfer"},
    21: {"service": "FTP", "description": "File Transfer Protocol", "risk": "CRITICAL", "category": "File Transfer"},
    22: {"service": "SSH", "description": "Secure Shell", "risk": "LOW", "category": "Remote Access"},
    23: {"service": "Telnet", "description": "Telnet Protocol", "risk": "CRITICAL", "category": "Remote Access"},
    25: {"service": "SMTP", "description": "Simple Mail Transfer Protocol", "risk": "MEDIUM", "category": "Email"},
    53: {"service": "DNS", "description": "Domain Name System", "risk": "LOW", "category": "DNS"},
    80: {"service": "HTTP", "description": "HyperText Transfer Protocol", "risk": "LOW", "category": "Web"},
    110: {"service": "POP3", "description": "Post Office Protocol", "risk": "MEDIUM", "category": "Email"},
    143: {"service": "IMAP", "description": "Internet Message Access Protocol", "risk": "MEDIUM", "category": "Email"},
    443: {"service": "HTTPS", "description": "Secure HyperText Transfer Protocol", "risk": "LOW", "category": "Web"},
    445: {"service": "SMB", "description": "Server Message Block", "risk": "HIGH", "category": "File Sharing"},
    465: {"service": "SMTPS", "description": "SMTP Secure", "risk": "LOW", "category": "Email"},
    587: {"service": "SMTP", "description": "SMTP Submission", "risk": "LOW", "category": "Email"},
    993: {"service": "IMAPS", "description": "IMAP Secure", "risk": "LOW", "category": "Email"},
    995: {"service": "POP3S", "description": "POP3 Secure", "risk": "LOW", "category": "Email"},
    1433: {"service": "MSSQL", "description": "Microsoft SQL Server", "risk": "HIGH", "category": "Database"},
    3306: {"service": "MySQL", "description": "MySQL Database", "risk": "HIGH", "category": "Database"},
    3389: {"service": "RDP", "description": "Remote Desktop Protocol", "risk": "HIGH", "category": "Remote Access"},
    5432: {"service": "PostgreSQL", "description": "PostgreSQL Database", "risk": "HIGH", "category": "Database"},
    5900: {"service": "VNC", "description": "Virtual Network Computing", "risk": "HIGH", "category": "Remote Access"},
    6379: {"service": "Redis", "description": "Redis Cache", "risk": "CRITICAL", "category": "Cache"},
    8080: {"service": "HTTP-ALT", "description": "Alternate HTTP", "risk": "LOW", "category": "Web"},
    8443: {"service": "HTTPS-ALT", "description": "Alternate HTTPS", "risk": "LOW", "category": "Web"},
    27017: {"service": "MongoDB", "description": "MongoDB Database", "risk": "CRITICAL", "category": "Database"},
    50000: {"service": "SAP", "description": "SAP Gateway", "risk": "MEDIUM", "category": "Enterprise"},
}

# Common ports to scan if not specified
COMMON_PORTS = [20, 21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 465, 587, 993, 995, 
                1433, 3306, 3389, 5432, 5900, 6379, 8080, 8443, 27017, 50000]


def is_valid_ip(ip: str) -> bool:
    """Validate IP address format"""
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(part) <= 255 for part in parts)
    except ValueError:
        return False


def scan_port(host: str, port: int, timeout: float = 2.0) -> Tuple[int, bool]:
    """
    Scan a single port on the target host
    Returns: (port_number, is_open)
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            return port, result == 0
    except Exception:
        return port, False


def get_port_info(port: int) -> Dict:
    """Get port information from database"""
    return PORT_DATABASE.get(port, {
        "service": "UNKNOWN",
        "description": "Unknown Service",
        "risk": "MEDIUM",
        "category": "Unclassified"
    })


def get_risk_colour(risk_level: str) -> str:
    """Return colour code based on risk level"""
    risk_colours = {
        "LOW": Colours.GREEN,
        "MEDIUM": Colours.YELLOW,
        "HIGH": Colours.YELLOW,
        "CRITICAL": Colours.RED
    }
    return risk_colours.get(risk_level, Colours.BLUE)


def format_terminal_output(results: Dict[str, List]) -> str:
    """Format scan results for colour-coded terminal output"""
    output = []
    output.append(f"\n{Colours.BOLD}{Colours.BLUE}╔════════════════════════════════════════════════════════════════╗{Colours.RESET}")
    output.append(f"{Colours.BOLD}{Colours.BLUE}║       NETWORK PORT SCANNER & SECURITY REPORTER v1.0           ║{Colours.RESET}")
    output.append(f"{Colours.BOLD}{Colours.BLUE}╚════════════════════════════════════════════════════════════════╝{Colours.RESET}\n")
    
    output.append(f"{Colours.BOLD}Target:{Colours.RESET} {results['target']}")
    output.append(f"{Colours.BOLD}Scan Date:{Colours.RESET} {results['timestamp']}")
    output.append(f"{Colours.BOLD}Total Ports Scanned:{Colours.RESET} {results['ports_scanned']}")
    output.append(f"{Colours.RED}{Colours.BOLD}Open Ports Found: {len(results['open_ports'])}{Colours.RESET}\n")
    
    if results['open_ports']:
        output.append(f"{Colours.BOLD}{Colours.BLUE}═══════════════════════════════════════════════════════════════{Colours.RESET}")
        output.append(f"{Colours.BOLD}PORT{Colours.RESET:<8} {Colours.BOLD}SERVICE{Colours.RESET:<15} {Colours.BOLD}DESCRIPTION{Colours.RESET:<30} {Colours.BOLD}RISK{Colours.RESET}")
        output.append(f"{Colours.BOLD}{Colours.BLUE}═══════════════════════════════════════════════════════════════{Colours.RESET}")
        
        # Sort by risk level (CRITICAL first, then HIGH, MEDIUM, LOW)
        risk_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        sorted_ports = sorted(results['open_ports'], 
                            key=lambda x: risk_order.get(x['risk'], 4))
        
        for port_info in sorted_ports:
            port = port_info['port']
            service = port_info['service']
            description = port_info['description'][:28]
            risk = port_info['risk']
            
            risk_colour = get_risk_colour(risk)
            output.append(f"{Colours.BOLD}{port:<8}{Colours.RESET} {service:<15} {description:<30} {risk_colour}{risk}{Colours.RESET}")
        
        output.append(f"{Colours.BOLD}{Colours.BLUE}═══════════════════════════════════════════════════════════════{Colours.RESET}\n")
        
        # Risk summary
        critical = sum(1 for p in results['open_ports'] if p['risk'] == 'CRITICAL')
        high = sum(1 for p in results['open_ports'] if p['risk'] == 'HIGH')
        medium = sum(1 for p in results['open_ports'] if p['risk'] == 'MEDIUM')
        low = sum(1 for p in results['open_ports'] if p['risk'] == 'LOW')
        
        output.append(f"{Colours.BOLD}RISK SUMMARY:{Colours.RESET}")
        if critical > 0:
            output.append(f"  {Colours.RED}● CRITICAL: {critical}{Colours.RESET}")
        if high > 0:
            output.append(f"  {Colours.YELLOW}● HIGH: {high}{Colours.RESET}")
        if medium > 0:
            output.append(f"  {Colours.YELLOW}● MEDIUM: {medium}{Colours.RESET}")
        if low > 0:
            output.append(f"  {Colours.GREEN}● LOW: {low}{Colours.RESET}")
        
        output.append(f"\n{Colours.RED}{Colours.BOLD}⚠️  RECOMMENDATION: Review and close unnecessary open ports!{Colours.RESET}\n")
    else:
        output.append(f"{Colours.GREEN}{Colours.BOLD}✓ No open ports detected on scanned range.{Colours.RESET}\n")
    
    return "\n".join(output)


def save_report(results: Dict[str, List], filename: str = None) -> str:
    """Save scan results to a structured text report file"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/scan_report_{results['target'].replace('.', '_')}_{timestamp}.txt"
    
    report = []
    report.append("=" * 70)
    report.append("NETWORK SECURITY SCAN REPORT")
    report.append("Port Scanner & Vulnerability Assessment")
    report.append("=" * 70)
    report.append("")
    
    report.append(f"Target Host: {results['target']}")
    report.append(f"Scan Date & Time: {results['timestamp']}")
    report.append(f"Total Ports Scanned: {results['ports_scanned']}")
    report.append(f"Open Ports Discovered: {len(results['open_ports'])}")
    report.append("")
    
    # Risk summary
    critical = sum(1 for p in results['open_ports'] if p['risk'] == 'CRITICAL')
    high = sum(1 for p in results['open_ports'] if p['risk'] == 'HIGH')
    medium = sum(1 for p in results['open_ports'] if p['risk'] == 'MEDIUM')
    low = sum(1 for p in results['open_ports'] if p['risk'] == 'LOW')
    
    report.append("RISK ASSESSMENT SUMMARY:")
    report.append(f"  Critical Vulnerabilities: {critical}")
    report.append(f"  High Risk Ports: {high}")
    report.append(f"  Medium Risk Ports: {medium}")
    report.append(f"  Low Risk Ports: {low}")
    report.append("")
    
    if critical > 0:
        report.append("[!] CRITICAL FINDINGS - IMMEDIATE ACTION REQUIRED")
        report.append("")
    
    # Open ports details
    if results['open_ports']:
        report.append("-" * 70)
        report.append("OPEN PORTS & SERVICES DETECTED:")
        report.append("-" * 70)
        report.append("")
        
        # Sort by risk level
        risk_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        sorted_ports = sorted(results['open_ports'], 
                            key=lambda x: risk_order.get(x['risk'], 4))
        
        for idx, port_info in enumerate(sorted_ports, 1):
            report.append(f"{idx}. PORT {port_info['port']}")
            report.append(f"   Service: {port_info['service']}")
            report.append(f"   Description: {port_info['description']}")
            report.append(f"   Risk Level: {port_info['risk']}")
            report.append(f"   Category: {port_info['category']}")
            report.append("")
    else:
        report.append("No open ports detected during scan.")
        report.append("")
    
    # Recommendations
    report.append("-" * 70)
    report.append("SECURITY RECOMMENDATIONS:")
    report.append("-" * 70)
    report.append("")
    
    if critical > 0:
        report.append("1. URGENT: Close or secure all CRITICAL ports immediately.")
        report.append("   - These ports represent severe security vulnerabilities.")
        report.append("   - Implement firewall rules to restrict access.")
        report.append("")
    
    if high > 0:
        report.append(f"{2 if critical > 0 else 1}. HIGH PRIORITY: Address all HIGH-risk ports.")
        report.append("   - These services should be secured with authentication.")
        report.append("   - Consider running on non-standard ports.")
        report.append("   - Implement network segmentation and access controls.")
        report.append("")
    
    report.append(f"{3 if critical > 0 or high > 0 else 1}. General Security Practices:")
    report.append("   - Keep all services and systems up to date with patches")
    report.append("   - Implement strong authentication mechanisms")
    report.append("   - Use encryption for sensitive data transmission")
    report.append("   - Deploy network monitoring and intrusion detection")
    report.append("   - Conduct regular security audits and penetration tests")
    report.append("")
    
    report.append("=" * 70)
    report.append(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 70)
    
    # Write to file
    with open(filename, 'w') as f:
        f.write("\n".join(report))
    
    return filename


def scan_target(host: str, ports: List[int] = None, threads: int = 50) -> Dict:
    """
    Scan multiple ports on target host using threading
    
    Args:
        host: Target IP address
        ports: List of ports to scan (defaults to COMMON_PORTS)
        threads: Number of concurrent threads
    
    Returns:
        Dictionary containing scan results
    """
    if ports is None:
        ports = COMMON_PORTS
    
    if not is_valid_ip(host):
        print(f"{Colours.RED}[!] Invalid IP address: {host}{Colours.RESET}")
        sys.exit(1)
    
    print(f"\n{Colours.BLUE}[*] Starting scan on {host}...{Colours.RESET}")
    print(f"{Colours.BLUE}[*] Scanning {len(ports)} ports with {threads} threads...{Colours.RESET}\n")
    
    open_ports = []
    
    # Use ThreadPoolExecutor for concurrent scanning
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(scan_port, host, port): port for port in ports}
        completed = 0
        
        for future in as_completed(futures):
            completed += 1
            port, is_open = future.result()
            
            if is_open:
                port_info = get_port_info(port)
                port_data = {
                    'port': port,
                    'service': port_info['service'],
                    'description': port_info['description'],
                    'risk': port_info['risk'],
                    'category': port_info['category']
                }
                open_ports.append(port_data)
                
                risk_colour = get_risk_colour(port_info['risk'])
                print(f"{Colours.BOLD}[+] Open Port Found: {port}/{port_info['service']:<10} ({port_info['description']}) - {risk_colour}{port_info['risk']}{Colours.RESET}")
    
    results = {
        'target': host,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'ports_scanned': len(ports),
        'open_ports': open_ports
    }
    
    return results


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Network Port Scanner & Security Reporter',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python port_scanner.py 192.168.1.1
  python port_scanner.py 10.0.0.5 -p 22,80,443,3306
  python port_scanner.py 172.16.0.1 --all-ports
  python port_scanner.py 8.8.8.8 -t 100
        """
    )
    
    parser.add_argument('target', help='Target IP address to scan')
    parser.add_argument('-p', '--ports', help='Specific ports to scan (comma-separated)', type=str)
    parser.add_argument('-a', '--all-ports', action='store_true', help='Scan all 65535 ports (slow)')
    parser.add_argument('-t', '--threads', help='Number of concurrent threads (default: 50)', type=int, default=50)
    parser.add_argument('-o', '--output', help='Output report filename', type=str)
    parser.add_argument('-q', '--quiet', action='store_true', help='Suppress terminal output (report only)')
    
    args = parser.parse_args()
    
    # Determine ports to scan
    if args.all_ports:
        ports = list(range(1, 65536))
        print(f"{Colours.YELLOW}[!] Warning: Scanning all 65535 ports will take significant time...{Colours.RESET}")
    elif args.ports:
        try:
            ports = [int(p.strip()) for p in args.ports.split(',')]
        except ValueError:
            print(f"{Colours.RED}[!] Invalid port specification{Colours.RESET}")
            sys.exit(1)
    else:
        ports = COMMON_PORTS
    
    # Execute scan
    try:
        results = scan_target(args.target, ports, args.threads)
        
        # Display terminal output
        if not args.quiet:
            print(format_terminal_output(results))
        
        # Save report
        report_file = save_report(results, args.output)
        print(f"{Colours.GREEN}[✓] Report saved to: {report_file}{Colours.RESET}\n")
        
    except KeyboardInterrupt:
        print(f"\n{Colours.YELLOW}[!] Scan interrupted by user{Colours.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colours.RED}[!] Error during scan: {str(e)}{Colours.RESET}")
        sys.exit(1)


if __name__ == '__main__':
    main()
