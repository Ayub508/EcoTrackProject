import pytest
from app import create_app
from app.extensions import db as _db


@pytest.fixture(scope='session')
def app():
    app = create_app('testing')
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture(scope='function')
def db(app):
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.rollback()
        for table in reversed(_db.metadata.sorted_tables):
            _db.session.execute(table.delete())
        _db.session.commit()


@pytest.fixture(scope='function')
def client(app):
    return app.test_client()


@pytest.fixture
def auth_headers(client, db):
    client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'password123',
        'display_name': 'Test User',
        'country_code': 'GB'
    })
    res = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    token = res.get_json()['token']
    return {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
