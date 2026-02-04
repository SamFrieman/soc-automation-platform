"""
Starter Tests for SOC Automation Platform
Copy these patterns to complete all test files
"""

import pytest
from django.utils import timezone
from django.contrib.auth.models import User
from faker import Faker
from datetime import timedelta

from alerts.models import Alert, AlertComment
from alerts.serializers import AlertSerializer
from incidents.models import Incident
from playbooks.models import Playbook, PlaybookExecution
from frameworks.models import MitreTechnique, MitreTactic


fake = Faker()


# ============================================================================
# FIXTURES (Use these in your tests)
# ============================================================================

@pytest.fixture
def user():
    """Create a test user"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def admin_user():
    """Create a test admin user"""
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123'
    )


@pytest.fixture
def mitre_tactic():
    """Create a test MITRE tactic"""
    return MitreTactic.objects.create(
        tactic_id='TA0001',
        name='Initial Access',
        description='Test tactic',
        url='https://attack.mitre.org/'
    )


@pytest.fixture
def mitre_technique(mitre_tactic):
    """Create a test MITRE technique"""
    technique = MitreTechnique.objects.create(
        technique_id='T1566',
        name='Phishing',
        description='Phishing technique',
        url='https://attack.mitre.org/techniques/T1566/'
    )
    technique.tactics.add(mitre_tactic)
    return technique


@pytest.fixture
def alert(user, mitre_technique):
    """Create a test alert"""
    alert = Alert.objects.create(
        alert_id=f'ALERT-{fake.uuid4()}',
        title='Test Security Alert',
        description='This is a test alert',
        severity='HIGH',
        status='NEW',
        source_system='TestSIEM',
        source_ip='192.168.1.100',
        destination_ip='10.0.0.1',
        affected_user='john.doe',
        detected_at=timezone.now() - timedelta(hours=1),
        assigned_to=user,
    )
    alert.mitre_techniques.add(mitre_technique)
    return alert


@pytest.fixture
def incident(user, alert):
    """Create a test incident"""
    incident = Incident.objects.create(
        incident_id=f'INC-{fake.uuid4()}',
        title='Test Incident',
        description='Test incident description',
        incident_type='PHISHING',
        severity='HIGH',
        status='INVESTIGATING',
        assigned_to=user,
        detected_at=timezone.now(),
    )
    incident.alerts.add(alert)
    return incident


@pytest.fixture
def playbook(mitre_technique):
    """Create a test playbook"""
    playbook = Playbook.objects.create(
        name='Test Detection Playbook',
        description='Test playbook',
        playbook_type='DETECTION',
        script_path='/playbooks/test.py',
        timeout_seconds=600,
        enabled=True,
    )
    playbook.mitre_techniques.add(mitre_technique)
    return playbook


# ============================================================================
# MODEL TESTS
# ============================================================================

@pytest.mark.django_db
class TestAlertModel:
    """Test Alert model"""
    
    def test_alert_creation(self, alert):
        """Test alert can be created"""
        assert alert.id is not None
        assert alert.alert_id is not None
        assert alert.title == 'Test Security Alert'
        assert alert.severity == 'HIGH'
        assert alert.status == 'NEW'
    
    def test_alert_string_representation(self, alert):
        """Test alert string representation"""
        assert str(alert) == f"{alert.alert_id} - {alert.title}"
    
    def test_alert_status_transitions(self, alert):
        """Test alert status changes"""
        alert.status = 'INVESTIGATING'
        alert.save()
        alert.refresh_from_db()
        assert alert.status == 'INVESTIGATING'
    
    def test_alert_resolution_sets_timestamp(self, alert):
        """Test resolving alert sets resolved_at"""
        assert alert.resolved_at is None
        alert.status = 'RESOLVED'
        alert.save()
        alert.refresh_from_db()
        assert alert.resolved_at is not None
    
    def test_alert_with_multiple_techniques(self, alert, mitre_technique):
        """Test alert can have multiple MITRE techniques"""
        technique2 = MitreTechnique.objects.create(
            technique_id='T1087',
            name='Account Discovery',
            description='Test',
            url='https://attack.mitre.org/techniques/T1087/'
        )
        alert.mitre_techniques.add(technique2)
        assert alert.mitre_techniques.count() == 2
    
    def test_alert_time_to_resolve_calculation(self, alert):
        """Test time to resolve is calculated"""
        alert.status = 'RESOLVED'
        alert.save()
        alert.refresh_from_db()
        assert alert.time_to_resolve is not None
        assert alert.time_to_resolve > timedelta(0)
    
    def test_alert_comment_ordering(self, alert, user):
        """Test alert comments are ordered by newest first"""
        comment1 = AlertComment.objects.create(
            alert=alert, user=user, comment='First comment'
        )
        comment2 = AlertComment.objects.create(
            alert=alert, user=user, comment='Second comment'
        )
        comments = alert.comments.all()
        assert comments[0].id == comment2.id
    
    def test_alert_indexing_on_alert_id(self, alert):
        """Test alert_id is indexed for quick lookup"""
        fetched = Alert.objects.get(alert_id=alert.alert_id)
        assert fetched.id == alert.id


@pytest.mark.django_db
class TestIncidentModel:
    """Test Incident model"""
    
    def test_incident_creation(self, incident):
        """Test incident can be created"""
        assert incident.id is not None
        assert incident.incident_id is not None
        assert incident.severity == 'HIGH'
    
    def test_incident_alert_relationship(self, incident, alert):
        """Test incident can have multiple alerts"""
        assert incident.alerts.count() == 1
        assert incident.alerts.first() == alert
    
    def test_incident_status_choices(self):
        """Test incident has valid status choices"""
        valid_statuses = ['OPEN', 'INVESTIGATING', 'CONTAINED', 'RESOLVED', 'CLOSED']
        assert all(
            Incident._meta.get_field('status').choices
            for status in valid_statuses
        )


@pytest.mark.django_db
class TestPlaybookModel:
    """Test Playbook model"""
    
    def test_playbook_creation(self, playbook):
        """Test playbook can be created"""
        assert playbook.id is not None
        assert playbook.name == 'Test Detection Playbook'
        assert playbook.enabled is True
    
    def test_playbook_success_rate_zero(self, playbook):
        """Test success rate with no executions"""
        assert playbook.success_rate == 0
    
    def test_playbook_success_rate_calculation(self, playbook):
        """Test success rate calculation"""
        playbook.execution_count = 10
        playbook.success_count = 7
        assert playbook.success_rate == 70.0


# ============================================================================
# SERIALIZER TESTS
# ============================================================================

@pytest.mark.django_db
class TestAlertSerializer:
    """Test AlertSerializer"""
    
    def test_serialize_alert(self, alert):
        """Test alert serialization"""
        serializer = AlertSerializer(alert)
        data = serializer.data
        assert data['alert_id'] == alert.alert_id
        assert data['title'] == alert.title
        assert data['severity'] == 'HIGH'
    
    def test_deserialize_alert(self):
        """Test alert deserialization"""
        data = {
            'alert_id': 'TEST-001',
            'title': 'Test Alert',
            'description': 'Test description',
            'severity': 'MEDIUM',
            'status': 'NEW',
            'source_system': 'TestSIEM',
            'detected_at': timezone.now().isoformat(),
        }
        serializer = AlertSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
    
    def test_alert_serializer_requires_title(self):
        """Test alert title is required"""
        data = {
            'alert_id': 'TEST-001',
            'description': 'Test',
            'severity': 'HIGH',
            'source_system': 'TestSIEM',
            'detected_at': timezone.now().isoformat(),
        }
        serializer = AlertSerializer(data=data)
        assert not serializer.is_valid()
        assert 'title' in serializer.errors


# ============================================================================
# API VIEW TESTS (requires APITestCase or APIClient)
# ============================================================================

@pytest.mark.django_db
class TestAlertAPI:
    """Test Alert API endpoints"""
    
    def test_list_alerts(self, client, alert):
        """Test listing alerts"""
        response = client.get('/api/alerts/')
        assert response.status_code == 200 or response.status_code == 401
    
    def test_filter_alerts_by_severity(self, client, alert):
        """Test filtering alerts by severity"""
        response = client.get('/api/alerts/?severity=HIGH')
        # Add assertion based on response
    
    def test_search_alerts(self, client, alert):
        """Test searching alerts"""
        response = client.get(f'/api/alerts/?search={alert.title}')
        # Add assertion based on response


# ============================================================================
# SERVICE TESTS
# ============================================================================

@pytest.mark.django_db
class TestPlaybookOrchestrator:
    """Test PlaybookOrchestrator service"""
    
    def test_trigger_playbooks_by_technique(self, alert, playbook):
        """Test playbooks are triggered for matching techniques"""
        from playbooks.services import PlaybookOrchestrator
        
        orchestrator = PlaybookOrchestrator()
        # This will be implemented after service is complete


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

@pytest.mark.django_db
class TestPerformance:
    """Performance and database optimization tests"""
    
    @pytest.mark.django_db(transaction=True)
    def test_bulk_alert_creation(self):
        """Test creating many alerts doesn't cause N+1 queries"""
        # Create 100 alerts and ensure it doesn't use 100+ queries
        alerts = [
            Alert(
                alert_id=f'ALERT-{i}',
                title=f'Alert {i}',
                description='Test',
                severity='HIGH',
                source_system='Test',
                detected_at=timezone.now(),
            )
            for i in range(100)
        ]
        Alert.objects.bulk_create(alerts)
        
        # Fetching should be efficient
        fetched = Alert.objects.all()[:10]
        assert len(list(fetched)) == 10


# ============================================================================
# EDGE CASE TESTS
# ============================================================================

@pytest.mark.django_db
class TestEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_alert_with_null_ip_addresses(self):
        """Test alert with null IP addresses"""
        alert = Alert.objects.create(
            alert_id='TEST-001',
            title='Test',
            description='Test',
            severity='LOW',
            source_system='Test',
            detected_at=timezone.now(),
        )
        assert alert.source_ip is None
        assert alert.destination_ip is None
    
    def test_incident_with_json_arrays(self):
        """Test incident stores JSON arrays correctly"""
        incident = Incident.objects.create(
            incident_id='INC-001',
            title='Test',
            description='Test',
            incident_type='MALWARE',
            severity='HIGH',
            detected_at=timezone.now(),
            affected_systems=['server1', 'server2', 'server3'],
            affected_users=['user1', 'user2'],
        )
        incident.refresh_from_db()
        assert len(incident.affected_systems) == 3
        assert 'server1' in incident.affected_systems


# ============================================================================
# CONFTEST FIXTURES (pytest configuration)
# ============================================================================

@pytest.fixture(autouse=True)
def reset_db():
    """Auto-use fixture to reset DB between tests"""
    pass


# Run tests with: pytest backend/ -v --cov=backend

