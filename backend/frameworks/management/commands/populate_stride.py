from django.core.management.base import BaseCommand
from frameworks.models import StrideCategory


class Command(BaseCommand):
    help = 'Populate STRIDE threat categories'

    def handle(self, *args, **kwargs):
        self.stdout.write("Populating STRIDE...")
        
        stride_data = [
            {
                'stride_type': 'S',
                'name': 'Spoofing',
                'description': 'Illegally accessing and using another user authentication information.',
                'examples': 'Phishing, ARP spoofing, IP spoofing, session hijacking',
                'countermeasures': 'Strong authentication (MFA), digital certificates, encrypted protocols',
                'security_property': 'Authentication',
            },
            {
                'stride_type': 'T',
                'name': 'Tampering',
                'description': 'Malicious modification of data or code.',
                'examples': 'SQL injection, code injection, data modification in transit',
                'countermeasures': 'Digital signatures, input validation, integrity checks',
                'security_property': 'Integrity',
            },
            {
                'stride_type': 'R',
                'name': 'Repudiation',
                'description': 'Users denying actions without proof otherwise.',
                'examples': 'Log deletion, denying transactions, disabling audit logging',
                'countermeasures': 'Comprehensive logging, digital signatures, timestamps',
                'security_property': 'Non-repudiation',
            },
            {
                'stride_type': 'I',
                'name': 'Information Disclosure',
                'description': 'Exposing information to unauthorized individuals.',
                'examples': 'SQL injection revealing data, directory traversal, unencrypted transmission',
                'countermeasures': 'Encryption, access controls, secure error handling',
                'security_property': 'Confidentiality',
            },
            {
                'stride_type': 'D',
                'name': 'Denial of Service',
                'description': 'Denying service to valid users.',
                'examples': 'DDoS attacks, resource exhaustion, application-layer DoS',
                'countermeasures': 'Rate limiting, resource quotas, DDoS mitigation',
                'security_property': 'Availability',
            },
            {
                'stride_type': 'E',
                'name': 'Elevation of Privilege',
                'description': 'Unprivileged user gains privileged access.',
                'examples': 'Buffer overflows, SQL injection for admin rights, exploiting misconfigurations',
                'countermeasures': 'Least privilege, input validation, patching, RBAC',
                'security_property': 'Authorization',
            },
        ]
        
        created = 0
        for data in stride_data:
            category, was_created = StrideCategory.objects.get_or_create(
                stride_type=data['stride_type'],
                defaults=data
            )
            if was_created:
                created += 1
                self.stdout.write(f'  Created: {category}')
        
        self.stdout.write(self.style.SUCCESS(f'\nSTRIDE populated! Created: {created}/6'))