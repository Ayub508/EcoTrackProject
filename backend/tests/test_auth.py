import json


def test_register_success(client, db):
    res = client.post('/api/auth/register', json={
        'email': 'new@example.com',
        'password': 'password123',
        'display_name': 'New User',
        'country_code': 'GB'
    })
    assert res.status_code == 201
    data = res.get_json()
    assert 'token' in data
    assert data['user']['email'] == 'new@example.com'
    assert data['user']['display_name'] == 'New User'


def test_register_duplicate_email(client, db):
    client.post('/api/auth/register', json={
        'email': 'dupe@example.com',
        'password': 'password123',
        'display_name': 'User 1'
    })
    res = client.post('/api/auth/register', json={
        'email': 'dupe@example.com',
        'password': 'password456',
        'display_name': 'User 2'
    })
    assert res.status_code == 409


def test_register_invalid_email(client, db):
    res = client.post('/api/auth/register', json={
        'email': 'not-an-email',
        'password': 'password123',
        'display_name': 'Bad User'
    })
    assert res.status_code == 400


def test_register_short_password(client, db):
    res = client.post('/api/auth/register', json={
        'email': 'short@example.com',
        'password': '123',
        'display_name': 'Short Pass'
    })
    assert res.status_code == 400


def test_login_success(client, db):
    client.post('/api/auth/register', json={
        'email': 'login@example.com',
        'password': 'password123',
        'display_name': 'Login User'
    })
    res = client.post('/api/auth/login', json={
        'email': 'login@example.com',
        'password': 'password123'
    })
    assert res.status_code == 200
    data = res.get_json()
    assert 'token' in data


def test_login_wrong_password(client, db):
    client.post('/api/auth/register', json={
        'email': 'wrong@example.com',
        'password': 'password123',
        'display_name': 'Wrong Pass'
    })
    res = client.post('/api/auth/login', json={
        'email': 'wrong@example.com',
        'password': 'wrongpassword'
    })
    assert res.status_code == 401


def test_get_profile(client, db, auth_headers):
    res = client.get('/api/auth/me', headers=auth_headers)
    assert res.status_code == 200
    data = res.get_json()
    assert data['user']['email'] == 'test@example.com'


def test_update_profile(client, db, auth_headers):
    res = client.put('/api/auth/me', headers=auth_headers, json={
        'display_name': 'Updated Name',
        'country_code': 'US'
    })
    assert res.status_code == 200
    assert res.get_json()['user']['display_name'] == 'Updated Name'
    assert res.get_json()['user']['country_code'] == 'US'


def test_protected_route_no_token(client, db):
    res = client.get('/api/auth/me')
    assert res.status_code == 401
