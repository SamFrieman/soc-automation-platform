#!/usr/bin/env python3
"""
Playbook: Enrich IoC with Threat Intelligence
Integrates with: VirusTotal, AbuseIPDB
"""

import sys
import json
import requests
import os
from datetime import datetime

VIRUSTOTAL_API_KEY = os.getenv('VIRUSTOTAL_API_KEY', '')
ABUSEIPDB_API_KEY = os.getenv('ABUSEIPDB_API_KEY', '')


def check_virustotal_ip(ip_address):
    """Check IP reputation on VirusTotal"""
    if not VIRUSTOTAL_API_KEY:
        return None, "VirusTotal API key not configured"
    
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip_address}"
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            stats = data['data']['attributes']['last_analysis_stats']
            return True, {
                'malicious': stats.get('malicious', 0),
                'suspicious': stats.get('suspicious', 0),
                'harmless': stats.get('harmless', 0),
            }
        return False, f"API returned {response.status_code}"
    except Exception as e:
        return False, str(e)


def check_abuseipdb(ip_address):
    """Check IP on AbuseIPDB"""
    if not ABUSEIPDB_API_KEY:
        return None, "AbuseIPDB API key not configured"
    
    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {"Key": ABUSEIPDB_API_KEY, "Accept": "application/json"}
    params = {"ipAddress": ip_address, "maxAgeInDays": 90}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()['data']
            return True, {
                'abuse_confidence_score': data.get('abuseConfidenceScore'),
                'total_reports': data.get('totalReports'),
                'country': data.get('countryCode'),
            }
        return False, f"API returned {response.status_code}"
    except Exception as e:
        return False, str(e)


def main(alert_data):
    """Main execution function"""
    enrichment_results = {}
    actions = []
    
    source_ip = alert_data.get('source_ip')
    
    if source_ip:
        # VirusTotal check
        vt_success, vt_data = check_virustotal_ip(source_ip)
        enrichment_results['virustotal'] = {
            'success': vt_success,
            'data': vt_data
        }
        actions.append({
            'action': 'virustotal_lookup',
            'target': source_ip,
            'success': vt_success,
            'timestamp': datetime.now().isoformat()
        })
        
        # AbuseIPDB check
        abuse_success, abuse_data = check_abuseipdb(source_ip)
        enrichment_results['abuseipdb'] = {
            'success': abuse_success,
            'data': abuse_data
        }
        actions.append({
            'action': 'abuseipdb_lookup',
            'target': source_ip,
            'success': abuse_success,
            'timestamp': datetime.now().isoformat()
        })
    
    return {
        'status': 'SUCCESS',
        'actions_taken': actions,
        'enrichment': enrichment_results,
        'output': f"IoC enrichment completed at {datetime.now()}"
    }


if __name__ == '__main__':
    alert_data = json.loads(sys.stdin.read())
    result = main(alert_data)
    print(json.dumps(result))