"""
Generate ML-focused cybersecurity datasets for dashboard integration
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_malware_dataset(n_samples=5000):
    """
    Generate malware detection dataset with behavioral and static features.
    ML Task: Binary classification (malware vs benign)
    """
    print(f"Generating malware detection dataset with {n_samples} samples...")

    data = []
    malware_types = ['Trojan', 'Ransomware', 'Spyware', 'Adware', 'Worm', 'Rootkit', 'Backdoor']
    file_types = ['.exe', '.dll', '.bat', '.scr', '.com', '.pif', '.msi', '.pdf', '.docx', '.zip']

    for i in range(n_samples):
        # 60% malware, 40% benign for realistic class distribution
        is_malware = np.random.random() < 0.60

        # File characteristics
        file_size = np.random.lognormal(10, 2) if is_malware else np.random.lognormal(12, 1.5)
        file_type = random.choice(file_types)

        # Behavioral indicators (stronger signals for malware)
        api_calls = int(np.random.lognormal(5, 1.5)) if is_malware else int(np.random.lognormal(3, 1))
        network_connections = int(np.random.poisson(15)) if is_malware else int(np.random.poisson(3))
        registry_changes = int(np.random.poisson(25)) if is_malware else int(np.random.poisson(2))
        file_operations = int(np.random.poisson(30)) if is_malware else int(np.random.poisson(5))

        # Static analysis features
        entropy = np.random.uniform(6.5, 8.0) if is_malware else np.random.uniform(4.0, 6.5)
        packed = np.random.random() < 0.7 if is_malware else np.random.random() < 0.1
        code_sections = int(np.random.uniform(3, 8)) if is_malware else int(np.random.uniform(2, 5))
        imports_count = int(np.random.uniform(50, 200)) if is_malware else int(np.random.uniform(20, 100))

        # Suspicious behaviors
        suspicious_strings = int(np.random.poisson(10)) if is_malware else int(np.random.poisson(1))
        obfuscated_code = np.random.random() < 0.75 if is_malware else np.random.random() < 0.15
        anti_debug = np.random.random() < 0.65 if is_malware else np.random.random() < 0.05

        # Detection metadata
        detection_rate = np.random.uniform(0.6, 0.95) if is_malware else np.random.uniform(0, 0.15)

        data.append({
            'sample_id': f'SAMPLE_{i+1:05d}',
            'file_name': f'file_{i+1}{file_type}',
            'file_size_kb': round(file_size, 2),
            'file_type': file_type,
            'entropy': round(entropy, 3),
            'is_packed': packed,
            'code_sections': code_sections,
            'imports_count': imports_count,
            'api_calls_count': api_calls,
            'network_connections': network_connections,
            'registry_changes': registry_changes,
            'file_operations': file_operations,
            'suspicious_strings': suspicious_strings,
            'obfuscated_code': obfuscated_code,
            'anti_debug_detected': anti_debug,
            'av_detection_rate': round(detection_rate, 3),
            'malware_type': random.choice(malware_types) if is_malware else 'Benign',
            'is_malware': 1 if is_malware else 0
        })

    df = pd.DataFrame(data)
    print(f"Generated {len(df)} samples: {df['is_malware'].sum()} malware, {(1-df['is_malware']).sum()} benign")
    return df

def generate_phishing_dataset(n_samples=4000):
    """
    Generate phishing detection dataset with URL and content features.
    ML Task: Binary classification (phishing vs legitimate)
    """
    print(f"Generating phishing detection dataset with {n_samples} samples...")

    data = []
    legitimate_domains = ['google.com', 'microsoft.com', 'amazon.com', 'facebook.com', 'apple.com',
                         'linkedin.com', 'twitter.com', 'github.com', 'stackoverflow.com', 'youtube.com']
    tlds = ['.com', '.net', '.org', '.info', '.xyz', '.tk', '.ml', '.ga', '.cf']

    for i in range(n_samples):
        # 45% phishing, 55% legitimate
        is_phishing = np.random.random() < 0.45

        # URL features
        if is_phishing:
            url_length = int(np.random.uniform(60, 150))
            domain_age_days = int(np.random.uniform(1, 180))
            has_https = np.random.random() < 0.3
            subdomain_count = int(np.random.poisson(2))
            special_chars = int(np.random.uniform(5, 20))
            domain = f"{''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=random.randint(8, 15)))}{random.choice(tlds)}"
        else:
            url_length = int(np.random.uniform(20, 60))
            domain_age_days = int(np.random.uniform(365, 5000))
            has_https = np.random.random() < 0.85
            subdomain_count = int(np.random.poisson(0.5))
            special_chars = int(np.random.uniform(1, 5))
            domain = random.choice(legitimate_domains)

        # Content features
        external_links = int(np.random.poisson(15)) if is_phishing else int(np.random.poisson(5))
        forms_count = int(np.random.poisson(3)) if is_phishing else int(np.random.poisson(1))
        popup_windows = np.random.random() < 0.6 if is_phishing else np.random.random() < 0.1
        iframe_usage = np.random.random() < 0.7 if is_phishing else np.random.random() < 0.2

        # Technical indicators
        redirects_count = int(np.random.poisson(4)) if is_phishing else int(np.random.poisson(0.5))
        suspicious_keywords = int(np.random.poisson(5)) if is_phishing else 0
        favicon_different = np.random.random() < 0.8 if is_phishing else np.random.random() < 0.05

        # Security features
        dns_record_exists = np.random.random() < 0.4 if is_phishing else np.random.random() < 0.98
        ssl_valid = has_https and (np.random.random() < 0.2 if is_phishing else np.random.random() < 0.95)

        # Detection metadata
        reported_count = int(np.random.poisson(50)) if is_phishing else int(np.random.poisson(1))

        data.append({
            'url_id': f'URL_{i+1:05d}',
            'domain': domain,
            'url_length': url_length,
            'has_https': has_https,
            'ssl_valid': ssl_valid,
            'domain_age_days': domain_age_days,
            'subdomain_count': subdomain_count,
            'special_characters': special_chars,
            'external_links': external_links,
            'forms_count': forms_count,
            'popup_windows': popup_windows,
            'iframe_usage': iframe_usage,
            'redirects_count': redirects_count,
            'suspicious_keywords': suspicious_keywords,
            'favicon_different_domain': favicon_different,
            'dns_record_exists': dns_record_exists,
            'reported_phishing_count': reported_count,
            'is_phishing': 1 if is_phishing else 0
        })

    df = pd.DataFrame(data)
    print(f"Generated {len(df)} samples: {df['is_phishing'].sum()} phishing, {(1-df['is_phishing']).sum()} legitimate")
    return df

def generate_cve_dataset(n_samples=3000):
    """
    Generate CVE (Common Vulnerabilities and Exposures) dataset.
    ML Task: Severity prediction, vulnerability classification
    """
    print(f"Generating CVE vulnerability dataset with {n_samples} samples...")

    data = []
    vulnerability_types = ['SQL Injection', 'XSS', 'Buffer Overflow', 'Code Injection',
                          'Authentication Bypass', 'Privilege Escalation', 'Directory Traversal',
                          'CSRF', 'Remote Code Execution', 'Denial of Service']

    vendors = ['Microsoft', 'Oracle', 'Adobe', 'Apache', 'Cisco', 'IBM', 'Google',
              'Mozilla', 'Linux Kernel', 'WordPress', 'PHP', 'OpenSSL']

    products = ['Windows', 'Office', 'Exchange', 'SQL Server', 'Java', 'Flash Player',
               'HTTP Server', 'IOS', 'Chrome', 'Firefox', 'Kernel', 'Plugin']

    start_date = datetime(2020, 1, 1)

    for i in range(n_samples):
        # Generate CVE from 2020-2024
        pub_date = start_date + timedelta(days=np.random.randint(0, 1825))
        year = pub_date.year

        vuln_type = random.choice(vulnerability_types)
        vendor = random.choice(vendors)
        product = random.choice(products)

        # CVSS scores (0-10 scale)
        # Different vulnerability types have different severity distributions
        if vuln_type in ['Remote Code Execution', 'Authentication Bypass', 'Privilege Escalation']:
            base_score = np.random.uniform(7.0, 10.0)
            severity = 'CRITICAL' if base_score >= 9.0 else 'HIGH'
        elif vuln_type in ['SQL Injection', 'XSS', 'Buffer Overflow']:
            base_score = np.random.uniform(5.0, 9.0)
            if base_score >= 9.0:
                severity = 'CRITICAL'
            elif base_score >= 7.0:
                severity = 'HIGH'
            else:
                severity = 'MEDIUM'
        else:
            base_score = np.random.uniform(3.0, 8.0)
            if base_score >= 7.0:
                severity = 'HIGH'
            elif base_score >= 4.0:
                severity = 'MEDIUM'
            else:
                severity = 'LOW'

        # CVSS metrics
        exploitability = np.random.uniform(1.0, 4.0)
        impact_score = np.random.uniform(1.0, 6.0)

        # Exploitation status
        has_exploit = np.random.random() < (0.7 if base_score >= 7.0 else 0.3)
        exploit_public = has_exploit and np.random.random() < 0.6

        # Patch availability
        days_to_patch = int(np.random.lognormal(3, 1.5))
        patch_available = np.random.random() < 0.85

        # References and metadata
        references_count = int(np.random.poisson(5))
        cwe_id = f'CWE-{random.randint(1, 999)}'

        # Affected systems
        affected_versions = int(np.random.uniform(1, 20))

        data.append({
            'cve_id': f'CVE-{year}-{i+1:05d}',
            'published_date': pub_date.strftime('%Y-%m-%d'),
            'year': year,
            'vulnerability_type': vuln_type,
            'vendor': vendor,
            'product': product,
            'affected_versions': affected_versions,
            'cvss_base_score': round(base_score, 1),
            'severity': severity,
            'exploitability_score': round(exploitability, 2),
            'impact_score': round(impact_score, 2),
            'has_exploit': has_exploit,
            'exploit_public': exploit_public,
            'patch_available': patch_available,
            'days_to_patch': days_to_patch if patch_available else None,
            'cwe_id': cwe_id,
            'references_count': references_count
        })

    df = pd.DataFrame(data)
    print(f"Generated {len(df)} CVE records")
    print(f"Severity distribution:\n{df['severity'].value_counts()}")
    return df

def main():
    """Generate all ML-focused cybersecurity datasets"""
    print("=" * 80)
    print("Generating ML-Focused Cybersecurity Datasets")
    print("=" * 80)
    print()

    # Generate datasets
    malware_df = generate_malware_dataset(5000)
    phishing_df = generate_phishing_dataset(4000)
    cve_df = generate_cve_dataset(3000)

    # Save to data directory
    data_dir = '../data'

    print("\n" + "=" * 80)
    print("Saving datasets to data directory...")
    print("=" * 80)

    malware_df.to_csv(f'{data_dir}/malware_detection_dataset.csv', index=False)
    print(f"✓ Saved malware_detection_dataset.csv ({len(malware_df)} records)")

    phishing_df.to_csv(f'{data_dir}/phishing_detection_dataset.csv', index=False)
    print(f"✓ Saved phishing_detection_dataset.csv ({len(phishing_df)} records)")

    cve_df.to_csv(f'{data_dir}/cve_vulnerability_dataset.csv', index=False)
    print(f"✓ Saved cve_vulnerability_dataset.csv ({len(cve_df)} records)")

    print("\n" + "=" * 80)
    print("Dataset Summary")
    print("=" * 80)
    print(f"\nTotal records generated: {len(malware_df) + len(phishing_df) + len(cve_df)}")
    print(f"  • Malware Detection: {len(malware_df)} samples (ML: Binary Classification)")
    print(f"  • Phishing Detection: {len(phishing_df)} URLs (ML: Binary Classification)")
    print(f"  • CVE Vulnerabilities: {len(cve_df)} CVEs (ML: Severity Prediction)")
    print("\nAll datasets are ready for ML training and dashboard integration!")

if __name__ == '__main__':
    main()
