from django.core.management.base import BaseCommand
from frameworks.models import KillChainStage


class Command(BaseCommand):
    help = 'Populate Cyber Kill Chain stages'

    def handle(self, *args, **kwargs):
        self.stdout.write("Populating Cyber Kill Chain...")
        
        killchain_data = [
            {
                'stage_number': 1,
                'name': 'Reconnaissance',
                'description': 'Attacker gathers information about the target.',
                'indicators': 'Web crawling, port scanning, DNS queries, OSINT',
                'defensive_actions': 'Monitor for scanning, honeypots, limit public info',
                'example_tools': ['Nmap', 'Shodan', 'Maltego'],
            },
            {
                'stage_number': 2,
                'name': 'Weaponization',
                'description': 'Attacker creates malicious payload.',
                'indicators': 'Not directly observable (on attacker infrastructure)',
                'defensive_actions': 'Threat intelligence monitoring, vulnerability awareness',
                'example_tools': ['Metasploit', 'Cobalt Strike'],
            },
            {
                'stage_number': 3,
                'name': 'Delivery',
                'description': 'Attacker transmits weapon to target.',
                'indicators': 'Phishing emails, malicious links, USB drops',
                'defensive_actions': 'Email filtering, web filtering, endpoint protection',
                'example_tools': ['Email', 'Malicious websites'],
            },
            {
                'stage_number': 4,
                'name': 'Exploitation',
                'description': 'Exploit code executes on victim system.',
                'indicators': 'Unexpected processes, registry changes, privilege escalation',
                'defensive_actions': 'Patching, exploit prevention, behavior detection',
                'example_tools': ['Browser exploits', 'Zero-days'],
            },
            {
                'stage_number': 5,
                'name': 'Installation',
                'description': 'Malware installs persistent backdoor.',
                'indicators': 'New services, scheduled tasks, registry modifications',
                'defensive_actions': 'Application whitelisting, file integrity monitoring',
                'example_tools': ['RATs', 'Backdoors'],
            },
            {
                'stage_number': 6,
                'name': 'Command & Control',
                'description': 'Malware establishes command channel.',
                'indicators': 'Beaconing, unusual DNS, connections to suspicious IPs',
                'defensive_actions': 'Network segmentation, DNS filtering, IDS/IPS',
                'example_tools': ['IRC', 'HTTP/S C2'],
            },
            {
                'stage_number': 7,
                'name': 'Actions on Objectives',
                'description': 'Attacker achieves goals: exfiltration, destruction, encryption.',
                'indicators': 'Large data transfers, file encryption, lateral movement',
                'defensive_actions': 'DLP, network monitoring, backup procedures',
                'example_tools': ['Exfiltration tools', 'Ransomware'],
            },
        ]
        
        created = 0
        for data in killchain_data:
            stage, was_created = KillChainStage.objects.get_or_create(
                stage_number=data['stage_number'],
                defaults=data
            )
            if was_created:
                created += 1
                self.stdout.write(f'  Created: {stage}')
        
        self.stdout.write(self.style.SUCCESS(f'\nKill Chain populated! Created: {created}/7'))