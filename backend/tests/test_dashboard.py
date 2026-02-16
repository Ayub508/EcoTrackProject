from datetime import date, timedelta
from app.models import EmissionFactor


def _seed_and_create_activities(client, db, auth_headers):
    factor = EmissionFactor(
        category='transport', sub_category='car_petrol',
        factor_value=0.192, unit='kg CO2/km', source='DEFRA', region='UK', year=2023
    )
    db.session.add(factor)
    db.session.commit()

    today = date.today()
    for i in range(5):
        client.post('/api/activities', headers=auth_headers, json={
            'category': 'transport',
            'sub_category': 'car_petrol',
            'quantity': 20.0,
            'unit': 'km',
            'date': (today - timedelta(days=i)).isoformat()
        })


def test_dashboard_summary(client, db, auth_headers):
    _seed_and_create_activities(client, db, auth_headers)

    res = client.get('/api/dashboard/summary?period=week', headers=auth_headers)
    assert res.status_code == 200
    data = res.get_json()
    assert 'total_co2_kg' in data
    assert 'categories' in data
    assert data['total_co2_kg'] >= 0


def test_dashboard_trend(client, db, auth_headers):
    _seed_and_create_activities(client, db, auth_headers)

    res = client.get('/api/dashboard/trend?weeks=4', headers=auth_headers)
    assert res.status_code == 200
    data = res.get_json()
    assert 'trend' in data


def test_dashboard_prediction(client, db, auth_headers):
    res = client.get('/api/dashboard/prediction', headers=auth_headers)
    assert res.status_code == 200
    data = res.get_json()
    assert 'message' in data


def test_dashboard_requires_auth(client, db):
    res = client.get('/api/dashboard/summary')
    assert res.status_code == 401
