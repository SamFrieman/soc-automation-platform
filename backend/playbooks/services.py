from typing import List
from alerts.models import Alert
from playbooks.models import Playbook, PlaybookExecution
from playbooks.tasks import execute_playbook_script


class PlaybookOrchestrator:
    """Orchestrates playbook execution based on alert classifications"""
    
    def trigger_playbooks(self, alert: Alert) -> List[PlaybookExecution]:
        """Find and trigger relevant playbooks for an alert"""
        executions = []
        
        # Find playbooks matching MITRE techniques
        for technique in alert.mitre_techniques.all():
            playbooks = Playbook.objects.filter(
                mitre_techniques=technique,
                enabled=True
            )
            executions.extend(self._create_executions(alert, playbooks))
        
        # Find playbooks matching OWASP categories
        for category in alert.owasp_categories.all():
            playbooks = Playbook.objects.filter(
                owasp_categories=category,
                enabled=True
            )
            executions.extend(self._create_executions(alert, playbooks))
        
        # Find playbooks matching STRIDE categories
        for category in alert.stride_categories.all():
            playbooks = Playbook.objects.filter(
                stride_categories=category,
                enabled=True
            )
            executions.extend(self._create_executions(alert, playbooks))
        
        # Find playbooks matching Kill Chain stage
        if alert.kill_chain_stage:
            playbooks = Playbook.objects.filter(
                kill_chain_stages=alert.kill_chain_stage,
                enabled=True
            )
            executions.extend(self._create_executions(alert, playbooks))
        
        return executions
    
    def _create_executions(self, alert: Alert, playbooks) -> List[PlaybookExecution]:
        """Create playbook executions"""
        executions = []
        
        for playbook in playbooks:
            # Check if already executed for this alert
            if PlaybookExecution.objects.filter(playbook=playbook, alert=alert).exists():
                continue
            
            execution = PlaybookExecution.objects.create(
                playbook=playbook,
                alert=alert,
                status='PENDING'
            )
            
            # Trigger execution if auto-execute enabled
            if playbook.auto_execute:
                execute_playbook_script.delay(execution.id)
            
            executions.append(execution)
        
        return executions