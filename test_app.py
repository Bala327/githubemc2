import pytest
from app import app, db, HealthRecord
from datetime import datetime

@pytest.fixture
def client():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_create_record(client):
    data = {
        'patient_name': 'John Doe',
        'date_of_birth': '1990-01-01',
        'medical_condition': 'Flu',
        'treatment': 'Rest and fluids'
    }
    response = client.post('/record/new', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Health record created successfully!' in response.data

def test_view_record(client):
    # Create a test record
    record = HealthRecord(
        patient_name='Jane Doe',
        date_of_birth=datetime.strptime('1990-01-01', '%Y-%m-%d'),
        medical_condition='Cold',
        treatment='Rest'
    )
    with app.app_context():
        db.session.add(record)
        db.session.commit()
        record_id = record.id

    response = client.get(f'/record/{record_id}')
    assert response.status_code == 200
    assert b'Jane Doe' in response.data

def test_update_record(client):
    # Create a test record
    record = HealthRecord(
        patient_name='Jane Doe',
        date_of_birth=datetime.strptime('1990-01-01', '%Y-%m-%d'),
        medical_condition='Cold',
        treatment='Rest'
    )
    with app.app_context():
        db.session.add(record)
        db.session.commit()
        record_id = record.id

    data = {
        'patient_name': 'Jane Smith',
        'date_of_birth': '1990-01-01',
        'medical_condition': 'Flu',
        'treatment': 'Medicine'
    }
    response = client.post(f'/record/{record_id}/edit', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Health record updated successfully!' in response.data

def test_delete_record(client):
    # Create a test record
    record = HealthRecord(
        patient_name='Jane Doe',
        date_of_birth=datetime.strptime('1990-01-01', '%Y-%m-%d'),
        medical_condition='Cold',
        treatment='Rest'
    )
    with app.app_context():
        db.session.add(record)
        db.session.commit()
        record_id = record.id

    response = client.post(f'/record/{record_id}/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'Health record deleted successfully!' in response.data