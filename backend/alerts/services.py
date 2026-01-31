import re
from typing import List, Dict
from alerts.models import Alert
from frameworks.models import (
    MitreTechnique, OwaspCategory, StrideCategory, 
    KillChainStage, DiamondCapability
)


class AlertClassifier:
    """Automatically classify alerts against security frameworks"""
    
    def classify_alert(self, alert: Alert) -> Dict:
        """Main classification method"""
        classification = {
            'mitre': self.classify_mitre(alert),
            'owasp': self.classify_owasp(alert),
            'stride': self.classify_stride(alert),
            'kill_chain': self.classify_kill_chain(alert),
        }
        
        self._apply_classifications(alert, classification)
        return classification
    
    def classify_mitre(self, alert: Alert) -> List[MitreTechnique]:
        """Map alert to MITRE ATT&CK techniques"""
        techniques = []
        
        mitre_keywords = {
            'T1566': ['phishing', 'spearphishing', 'malicious email'],
            'T1190': ['exploit', 'vulnerability', 'CVE'],
            'T1059': ['powershell', 'cmd.exe', 'command line', 'script'],
            'T1071': ['C2', 'command and control', 'beacon'],
            'T1003': ['credential dump', 'lsass', 'mimikatz'],
            'T1486': ['ransomware', 'encryption', 'file encrypted'],
            'T1078': ['valid accounts', 'compromised credentials'],
            'T1021': ['remote services', 'RDP', 'SSH'],
        }
        
        alert_text = f"{alert.title} {alert.description}".lower()
        
        for technique_id, keywords in mitre_keywords.items():
            if any(keyword in alert_text for keyword in keywords):
                try:
                    technique = MitreTechnique.objects.get(technique_id=technique_id)
                    techniques.append(technique)
                except MitreTechnique.DoesNotExist:
                    pass
        
        return techniques
    
    def classify_owasp(self, alert: Alert) -> List[OwaspCategory]:
        """Map alert to OWASP Top 10"""
        categories = []
        
        owasp_keywords = {
            'A01': ['access control', 'authorization', 'privilege escalation', 'IDOR'],
            'A02': ['encryption', 'SSL', 'TLS', 'sensitive data', 'plaintext'],
            'A03': ['SQL injection', 'SQLi', 'XSS', 'command injection'],
            'A05': ['misconfiguration', 'default password', 'open port'],
            'A07': ['authentication', 'session', 'brute force'],
            'A09': ['logging', 'monitoring', 'audit'],
        }
        
        alert_text = f"{alert.title} {alert.description}".lower()
        
        for category_id, keywords in owasp_keywords.items():
            if any(keyword in alert_text for keyword in keywords):
                try:
                    category = OwaspCategory.objects.get(category_id=category_id, year='2021')
                    categories.append(category)
                except OwaspCategory.DoesNotExist:
                    pass
        
        return categories
    
    def classify_stride(self, alert: Alert) -> List[StrideCategory]:
        """Map alert to STRIDE categories"""
        categories = []
        
        stride_keywords = {
            'S': ['spoofing', 'impersonation', 'fake', 'forged'],
            'T': ['tampering', 'modification', 'altered', 'integrity'],
            'R': ['repudiation', 'log deletion', 'audit bypass'],
            'I': ['information disclosure', 'data leak', 'exposure'],
            'D': ['denial of service', 'DoS', 'DDoS', 'resource exhaustion'],
            'E': ['privilege escalation', 'elevation', 'admin rights'],
        }
        
        alert_text = f"{alert.title} {alert.description}".lower()
        
        for stride_type, keywords in stride_keywords.items():
            if any(keyword in alert_text for keyword in keywords):
                try:
                    category = StrideCategory.objects.get(stride_type=stride_type)
                    categories.append(category)
                except StrideCategory.DoesNotExist:
                    pass
        
        return categories
    
    def classify_kill_chain(self, alert: Alert) -> KillChainStage:
        """Determine Cyber Kill Chain stage"""
        stage_keywords = {
            1: ['reconnaissance', 'scanning', 'enumeration'],
            2: ['weaponization', 'malware creation'],
            3: ['delivery', 'phishing', 'email', 'exploit kit'],
            4: ['exploitation', 'exploit', 'vulnerability'],
            5: ['installation', 'persistence', 'backdoor'],
            6: ['command and control', 'C2', 'C&C', 'beacon'],
            7: ['exfiltration', 'data theft', 'ransomware'],
        }
        
        alert_text = f"{alert.title} {alert.description}".lower()
        
        for stage_num, keywords in stage_keywords.items():
            if any(keyword in alert_text for keyword in keywords):
                try:
                    return KillChainStage.objects.get(stage_number=stage_num)
                except KillChainStage.DoesNotExist:
                    pass
        
        return None
    
    def _apply_classifications(self, alert: Alert, classification: Dict):
        """Apply classifications to alert"""
        for technique in classification['mitre']:
            alert.mitre_techniques.add(technique)
        
        for category in classification['owasp']:
            alert.owasp_categories.add(category)
        
        for category in classification['stride']:
            alert.stride_categories.add(category)
        
        if classification['kill_chain']:
            alert.kill_chain_stage = classification['kill_chain']
        
        alert.save()