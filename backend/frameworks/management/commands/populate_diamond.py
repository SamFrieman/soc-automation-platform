from django.core.management.base import BaseCommand
from frameworks.models import DiamondAdversary, DiamondInfrastructure, DiamondCapability, DiamondVictim


class Command(BaseCommand):
    help = 'Populate Diamond Model sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Populating Diamond Model...")
        
        # Sample Adversaries
        adversaries = [
            {
                'name': 'APT29 (Cozy Bear)',
                'aliases': ['The Dukes', 'CozyDuke'],
                'country': 'Russia',
                'motivation': 'ESPIONAGE',
                'sophistication_level': 'NATION_STATE',
                'description': 'Russian state-sponsored group',
                'active': True,
            },
            {
                'name': 'FIN7',
                'aliases': ['Carbanak'],
                'country': 'Unknown',
                'motivation': 'FINANCIAL',
                'sophistication_level': 'ADVANCED',
                'description': 'Financial cybercrime group',
                'active': True,
            },
        ]
        
        adv_count = 0
        for data in adversaries:
            adv, created = DiamondAdversary.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                adv_count += 1
        
        # Sample Infrastructure
        infra = [
            {'infra_type': 'IP', 'value': '192.0.2.100', 'is_malicious': True, 'reputation_score': 15},
            {'infra_type': 'DOMAIN', 'value': 'malicious-c2.example.com', 'is_malicious': True, 'reputation_score': 10},
        ]
        
        infra_count = 0
        for data in infra:
            inf, created = DiamondInfrastructure.objects.get_or_create(
                infra_type=data['infra_type'],
                value=data['value'],
                defaults={k: v for k, v in data.items() if k not in ['infra_type', 'value']}
            )
            if created:
                infra_count += 1
        
        # Sample Capabilities
        capabilities = [
            {'name': 'Cobalt Strike', 'capability_type': 'TOOL', 'description': 'Penetration testing tool'},
            {'name': 'Mimikatz', 'capability_type': 'TOOL', 'description': 'Credential dumping tool'},
        ]
        
        cap_count = 0
        for data in capabilities:
            cap, created = DiamondCapability.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                cap_count += 1
        
        # Sample Victims
        victims = [
            {'organization': 'Sample Healthcare Corp', 'industry': 'HEALTHCARE', 'country': 'United States'},
        ]
        
        vic_count = 0
        for data in victims:
            vic, created = DiamondVictim.objects.get_or_create(
                organization=data['organization'],
                defaults=data
            )
            if created:
                vic_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'\nDiamond Model populated!'))
        self.stdout.write(f'Adversaries: {adv_count}, Infrastructure: {infra_count}')
        self.stdout.write(f'Capabilities: {cap_count}, Victims: {vic_count}')