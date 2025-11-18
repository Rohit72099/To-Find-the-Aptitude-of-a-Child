import pytest
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_register_and_profile(client):
    resp = client.post('/api/auth/register/', {'username': 'demo', 'email': 'demo@example.com', 'password': 'pass'})
    assert resp.status_code == 201
    user = User.objects.get(username='demo')
    assert user.email == 'demo@example.com'
