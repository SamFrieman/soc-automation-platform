from celery import shared_task
from playbooks.models import PlaybookExecution, Playbook
from django.utils import timezone
from django.conf import settings
import subprocess
import json
import os


@shared_task
def execute_playbook_script(execution_id):
    """Execute a playbook script"""
    try:
        execution = PlaybookExecution.objects.get(id=execution_id)
        playbook = execution.playbook
        alert = execution.alert
        
        # Update status to running
        execution.status = 'RUNNING'
        execution.started_at = timezone.now()
        execution.save()
        
        # Prepare alert data for script
        alert_data = {
            'alert_id': alert.alert_id,
            'title': alert.title,
            'description': alert.description,
            'severity': alert.severity,
            'source_ip': str(alert.source_ip) if alert.source_ip else None,
            'destination_ip': str(alert.destination_ip) if alert.destination_ip else None,
            'affected_user': alert.affected_user,
            'affected_asset': alert.affected_asset,
            'raw_log': alert.raw_log,
        }
        
        # Build script path
        script_path = os.path.join(settings.PLAYBOOK_SCRIPTS_DIR, playbook.script_path)
        
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"Script not found: {script_path}")
        
        # Execute script
        process = subprocess.Popen(
            ['python', script_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=playbook.timeout_seconds
        )
        
        stdout, stderr = process.communicate(input=json.dumps(alert_data))
        
        # Update playbook statistics
        playbook.execution_count += 1
        
        if process.returncode == 0:
            # Success
            result = json.loads(stdout)
            execution.status = 'SUCCESS'
            execution.output = result.get('output', '')
            execution.actions_taken = result.get('actions_taken', [])
            playbook.success_count += 1
        else:
            # Failure
            execution.status = 'FAILED'
            execution.error_message = stderr
            playbook.failure_count += 1
        
        execution.completed_at = timezone.now()
        execution.save()
        playbook.save()
        
        return f"Playbook execution {execution_id} completed"
        
    except subprocess.TimeoutExpired:
        execution.status = 'TIMEOUT'
        execution.error_message = 'Execution timed out'
        execution.completed_at = timezone.now()
        execution.save()
        return f"Playbook execution {execution_id} timed out"
        
    except Exception as e:
        execution.status = 'FAILED'
        execution.error_message = str(e)
        execution.completed_at = timezone.now()
        execution.save()
        return f"Playbook execution {execution_id} failed: {str(e)}"