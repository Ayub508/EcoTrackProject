from datetime import date


def test_create_goal(client, db, auth_headers):
    res = client.post('/api/goals', headers=auth_headers, json={
        'title': 'Reduce transport emissions',
        'category': 'transport',
        'target_co2_kg': 50.0,
        'period': 'weekly',
        'start_date': date.today().isoformat()
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data['goal']['title'] == 'Reduce transport emissions'
    assert data['goal']['target_co2_kg'] == 50.0
    assert data['goal']['status'] == 'active'


def test_list_goals(client, db, auth_headers):
    client.post('/api/goals', headers=auth_headers, json={
        'title': 'Goal 1',
        'target_co2_kg': 30.0,
        'period': 'weekly',
        'start_date': date.today().isoformat()
    })
    client.post('/api/goals', headers=auth_headers, json={
        'title': 'Goal 2',
        'target_co2_kg': 60.0,
        'period': 'monthly',
        'start_date': date.today().isoformat()
    })

    res = client.get('/api/goals?status=active', headers=auth_headers)
    assert res.status_code == 200
    assert len(res.get_json()['goals']) == 2


def test_delete_goal(client, db, auth_headers):
    create_res = client.post('/api/goals', headers=auth_headers, json={
        'title': 'Delete me',
        'target_co2_kg': 20.0,
        'period': 'weekly',
        'start_date': date.today().isoformat()
    })
    goal_id = create_res.get_json()['goal']['id']

    res = client.delete(f'/api/goals/{goal_id}', headers=auth_headers)
    assert res.status_code == 200

    res = client.get(f'/api/goals/{goal_id}', headers=auth_headers)
    assert res.status_code == 404


def test_goal_progress(client, db, auth_headers):
    from app.models import EmissionFactor
    factor = EmissionFactor(
        category='transport', sub_category='car_petrol',
        factor_value=0.192, unit='kg CO2/km', source='DEFRA', region='UK', year=2023
    )
    db.session.add(factor)
    db.session.commit()

    client.post('/api/goals', headers=auth_headers, json={
        'title': 'Weekly transport limit',
        'category': 'transport',
        'target_co2_kg': 20.0,
        'period': 'weekly',
        'start_date': date.today().isoformat()
    })

    client.post('/api/activities', headers=auth_headers, json={
        'category': 'transport',
        'sub_category': 'car_petrol',
        'quantity': 50.0,
        'unit': 'km',
        'date': date.today().isoformat()
    })

    res = client.get('/api/goals?status=active', headers=auth_headers)
    assert res.status_code == 200
    goals = res.get_json()['goals']
    assert len(goals) == 1
    assert goals[0]['current_co2_kg'] > 0


def test_create_goal_validation(client, db, auth_headers):
    res = client.post('/api/goals', headers=auth_headers, json={
        'title': '',
        'target_co2_kg': -10,
        'start_date': date.today().isoformat()
    })
    assert res.status_code == 400
