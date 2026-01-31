#!/usr/bin/env python3
"""
Playbook: Block Malicious IP Address (Simulation)
NOTE: This is a simulation - in production, integrate with your firewall API
"""

import sys
import json
from datetime import datetime


def block_ip_firewall(ip_address):
    """Simulate blocking IP (in production, call firewall API)"""
    try:
        # SIMULATION ONLY
        # In production, replace with actual firewall API calls:
        # - Palo Alto: panorama.Policies.SecurityRule
        # - Fortinet: fortigate.firewall.address
        # - pfSense: REST API
        
        print(f"[SIMULATION] Blocking IP: {ip_address}", file=sys.stderr)
        
        # Simulate success
        return True, f"Successfully blocked {ip_address} (SIMULATED)"
    except Exception as e:
        return False, f"Error: {str(e)}"


def main(alert_data):
    """Main execution function"""
    actions_taken = []
    
    source_ip = alert_data.get('source_ip')
    
    if source_ip:
        success, message = block_ip_firewall(source_ip)
        actions_taken.append({
            'action': 'block_ip',
            'target': source_ip,
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
    else:
        actions_taken.append({
            'action': 'block_ip',
            'success': False,
            'message': 'No source IP provided',
            'timestamp': datetime.now().isoformat()
        })
    
    return {
        'status': 'SUCCESS' if all(a['success'] for a in actions_taken) else 'PARTIAL',
        'actions_taken': actions_taken,
        'output': f"Playbook executed at {datetime.now()}"
    }


if __name__ == '__main__':
    alert_data = json.loads(sys.stdin.read())
    result = main(alert_data)
    print(json.dumps(result))