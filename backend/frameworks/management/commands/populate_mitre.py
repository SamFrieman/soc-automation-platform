from django.core.management.base import BaseCommand
import requests
from frameworks.models import MitreTactic, MitreTechnique, MitreSubTechnique


class Command(BaseCommand):
    help = 'Populate MITRE ATT&CK framework data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Fetching MITRE ATT&CK data...")
        
        url = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"
        
        try:
            response = requests.get(url, timeout=30)
            data = response.json()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed: {e}'))
            return
        
        # Process Tactics
        self.stdout.write("Processing tactics...")
        tactics = [obj for obj in data['objects'] if obj['type'] == 'x-mitre-tactic']
        
        for tactic_data in tactics:
            try:
                ext_ref = tactic_data.get('external_references', [{}])[0]
                tactic, created = MitreTactic.objects.get_or_create(
                    tactic_id=ext_ref.get('external_id', ''),
                    defaults={
                        'name': tactic_data.get('name', ''),
                        'description': tactic_data.get('description', ''),
                        'url': ext_ref.get('url', ''),
                    }
                )
                if created:
                    self.stdout.write(f'  Created: {tactic.name}')
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  Error: {e}'))
        
        # Process Techniques
        self.stdout.write("\nProcessing techniques...")
        techniques = [
            obj for obj in data['objects'] 
            if obj['type'] == 'attack-pattern' and not obj.get('x_mitre_is_subtechnique', False)
        ]
        
        count = 0
        for tech_data in techniques:
            try:
                ext_ref = tech_data.get('external_references', [{}])[0]
                tech_id = ext_ref.get('external_id', '')
                
                if not tech_id:
                    continue
                
                technique, created = MitreTechnique.objects.get_or_create(
                    technique_id=tech_id,
                    defaults={
                        'name': tech_data.get('name', ''),
                        'description': tech_data.get('description', ''),
                        'url': ext_ref.get('url', ''),
                        'platforms': tech_data.get('x_mitre_platforms', []),
                    }
                )
                
                # Link tactics
                if 'kill_chain_phases' in tech_data:
                    for phase in tech_data['kill_chain_phases']:
                        tactic_name = phase['phase_name'].replace('-', ' ').title()
                        try:
                            tactic = MitreTactic.objects.get(name__iexact=tactic_name)
                            technique.tactics.add(tactic)
                        except:
                            pass
                
                if created:
                    count += 1
                    if count % 50 == 0:
                        self.stdout.write(f'  Processed {count} techniques...')
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  Error: {e}'))
        
        # Process Sub-Techniques
        self.stdout.write("\nProcessing sub-techniques...")
        sub_techs = [
            obj for obj in data['objects']
            if obj['type'] == 'attack-pattern' and obj.get('x_mitre_is_subtechnique', False)
        ]
        
        sub_count = 0
        for sub_data in sub_techs:
            try:
                ext_ref = sub_data.get('external_references', [{}])[0]
                sub_id = ext_ref.get('external_id', '')
                
                if not sub_id or '.' not in sub_id:
                    continue
                
                parent_id = sub_id.split('.')[0]
                parent = MitreTechnique.objects.get(technique_id=parent_id)
                
                sub_tech, created = MitreSubTechnique.objects.get_or_create(
                    sub_technique_id=sub_id,
                    defaults={
                        'name': sub_data.get('name', ''),
                        'parent_technique': parent,
                        'description': sub_data.get('description', ''),
                    }
                )
                
                if created:
                    sub_count += 1
            except:
                pass
        
        self.stdout.write("\n" + "="*50)
        self.stdout.write(self.style.SUCCESS('MITRE ATT&CK populated!'))
        self.stdout.write(f'Tactics: {MitreTactic.objects.count()}')
        self.stdout.write(f'Techniques: {MitreTechnique.objects.count()}')
        self.stdout.write(f'Sub-Techniques: {MitreSubTechnique.objects.count()}')
        self.stdout.write("="*50)