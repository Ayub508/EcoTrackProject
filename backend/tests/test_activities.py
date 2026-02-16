import json
from app.models import EmissionFactor


def _seed_factor(db):
    factor = EmissionFactor(
        category='transport',
        sub_category='car_petrol',
        factor_value=0.192,
        unit='kg CO2/km',
        source='DEFRA 2023',
        region='UK',
        year=2023
    )
    db.session.add(factor)
    db.session.commit()
    return factor


def test_create_activity(client, db, auth_headers):
    _seed_factor(db)
    res = client.post('/api/activities', headers=auth_headers, json={
        'category': 'transport',
        'sub_category': 'car_petrol',
        'quantity': 50.0,
        'unit': 'km',
        'date': '2024-01-15'
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data['activity']['category'] == 'transport'
    assert data['activity']['co2_kg'] == 9.6  # 50 * 0.192


def test_create_activity_invalid_category(client, db, auth_headers):
    res = client.post('/api/activities', headers=auth_headers, json={
        'category': 'invalid',
        'sub_category': 'test',
        'quantity': 10.0,
        'unit': 'km',
        'date': '2024-01-15'
    })
    assert res.status_code == 400


def test_list_activities(client, db, auth_headers):
    _seed_factor(db)
    client.post('/api/activities', headers=auth_headers, json={
        'category': 'transport',
        'sub_category': 'car_petrol',
        'quantity': 10.0,
        'unit': 'km',
        'date': '2024-01-15'
    })
    client.post('/api/activities', headers=auth_headers, json={
        'category': 'transport',
        'sub_category': 'car_petrol',
        'quantity': 20.0,
        'unit': 'km',
        'date': '2024-01-16'
    })

    res = client.get('/api/activities', headers=auth_headers)
    assert res.status_code == 200
    data = res.get_json()
    assert len(data['activities']) == 2
    assert data['total'] == 2


def test_delete_activity(client, db, auth_headers):
    _seed_factor(db)
    create_res = client.post('/api/activities', headers=auth_headers, json={
        'category': 'transport',
        'sub_category': 'car_petrol',
        'quantity': 10.0,
        'unit': 'km',
        'date': '2024-01-15'
    })
    activity_id = create_res.get_json()['activity']['id']

    res = client.delete(f'/api/activities/{activity_id}', headers=auth_headers)
    assert res.status_code == 200

    res = client.get(f'/api/activities/{activity_id}', headers=auth_headers)
    assert res.status_code == 404


def test_filter_by_category(client, db, auth_headers):
    _seed_factor(db)
    client.post('/api/activities', headers=auth_headers, json={
        'category': 'transport',
        'sub_category': 'car_petrol',
        'quantity': 10.0,
        'unit': 'km',
        'date': '2024-01-15'
    })

    res = client.get('/api/activities?category=transport', headers=auth_headers)
    assert res.status_code == 200
    assert len(res.get_json()['activities']) == 1

    res = client.get('/api/activities?category=energy', headers=auth_headers)
    assert res.status_code == 200
    assert len(res.get_json()['activities']) == 0
