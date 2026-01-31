from django.core.management.base import BaseCommand
from frameworks.models import OwaspCategory


class Command(BaseCommand):
    help = 'Populate OWASP Top 10 2021'

    def handle(self, *args, **kwargs):
        self.stdout.write("Populating OWASP Top 10 2021...")
        
        owasp_data = [
            {
                'category_id': 'A01',
                'year': '2021',
                'name': 'Broken Access Control',
                'description': 'Access control enforces policy such that users cannot act outside of their intended permissions.',
                'risk_rating': 'HIGH',
                'remediation': 'Implement proper access control checks, deny by default, use RBAC, validate JWT tokens properly.',
                'cwe_mapping': ['CWE-200', 'CWE-201', 'CWE-352'],
            },
            {
                'category_id': 'A02',
                'year': '2021',
                'name': 'Cryptographic Failures',
                'description': 'Failures related to cryptography which often lead to exposure of sensitive data.',
                'risk_rating': 'HIGH',
                'remediation': 'Encrypt data in transit and at rest, use strong encryption algorithms, proper key management.',
                'cwe_mapping': ['CWE-259', 'CWE-327', 'CWE-331'],
            },
            {
                'category_id': 'A03',
                'year': '2021',
                'name': 'Injection',
                'description': 'User-supplied data is not validated, filtered, or sanitized.',
                'risk_rating': 'CRITICAL',
                'remediation': 'Use parameterized queries, input validation, escaping special characters, WAF deployment.',
                'cwe_mapping': ['CWE-79', 'CWE-89', 'CWE-73'],
            },
            {
                'category_id': 'A04',
                'year': '2021',
                'name': 'Insecure Design',
                'description': 'Missing or ineffective control design.',
                'risk_rating': 'MEDIUM',
                'remediation': 'Implement threat modeling, secure design patterns, use reference architectures.',
                'cwe_mapping': ['CWE-209', 'CWE-256'],
            },
            {
                'category_id': 'A05',
                'year': '2021',
                'name': 'Security Misconfiguration',
                'description': 'Missing appropriate security hardening or improperly configured permissions.',
                'risk_rating': 'HIGH',
                'remediation': 'Harden configurations, remove default accounts, automated security scanning.',
                'cwe_mapping': ['CWE-16', 'CWE-209'],
            },
            {
                'category_id': 'A06',
                'year': '2021',
                'name': 'Vulnerable and Outdated Components',
                'description': 'Using components with known vulnerabilities.',
                'risk_rating': 'HIGH',
                'remediation': 'Inventory dependencies, continuous vulnerability scanning, patch management.',
                'cwe_mapping': ['CWE-1104'],
            },
            {
                'category_id': 'A07',
                'year': '2021',
                'name': 'Identification and Authentication Failures',
                'description': 'Confirmation of user identity, authentication, and session management is critical.',
                'risk_rating': 'HIGH',
                'remediation': 'Implement MFA, strong password policies, secure session management.',
                'cwe_mapping': ['CWE-297', 'CWE-287'],
            },
            {
                'category_id': 'A08',
                'year': '2021',
                'name': 'Software and Data Integrity Failures',
                'description': 'Code and infrastructure that does not protect against integrity violations.',
                'risk_rating': 'MEDIUM',
                'remediation': 'Digital signatures, CI/CD security, dependency verification.',
                'cwe_mapping': ['CWE-502', 'CWE-829'],
            },
            {
                'category_id': 'A09',
                'year': '2021',
                'name': 'Security Logging and Monitoring Failures',
                'description': 'Insufficient logging and monitoring allows attackers to persist.',
                'risk_rating': 'MEDIUM',
                'remediation': 'Comprehensive logging, real-time monitoring, SIEM integration.',
                'cwe_mapping': ['CWE-117', 'CWE-532'],
            },
            {
                'category_id': 'A10',
                'year': '2021',
                'name': 'Server-Side Request Forgery (SSRF)',
                'description': 'SSRF flaws occur when a web application fetches a remote resource without validating the user-supplied URL.',
                'risk_rating': 'HIGH',
                'remediation': 'Input validation, URL whitelisting, network segmentation.',
                'cwe_mapping': ['CWE-918'],
            },
        ]
        
        created = 0
        for data in owasp_data:
            category, was_created = OwaspCategory.objects.get_or_create(
                category_id=data['category_id'],
                year=data['year'],
                defaults=data
            )
            if was_created:
                created += 1
                self.stdout.write(f'  Created: {category}')
        
        self.stdout.write(self.style.SUCCESS(f'\nOWASP Top 10 populated! Created: {created}/10'))