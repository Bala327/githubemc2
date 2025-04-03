from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health_records.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class HealthRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    medical_condition = db.Column(db.String(200), nullable=False)
    treatment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

@app.route('/')
def index():
    records = HealthRecord.query.order_by(HealthRecord.created_at.desc()).all()
    return render_template('index.html', records=records)

@app.route('/record/new', methods=['GET', 'POST'])
def new_record():
    if request.method == 'POST':
        try:
            record = HealthRecord(
                patient_name=request.form['patient_name'],
                date_of_birth=datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d'),
                medical_condition=request.form['medical_condition'],
                treatment=request.form['treatment']
            )
            db.session.add(record)
            db.session.commit()
            flash('Health record created successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash('Error creating record. Please try again.', 'error')
            return render_template('new_record.html')
    return render_template('new_record.html')

@app.route('/record/<int:id>')
def view_record(id):
    record = HealthRecord.query.get_or_404(id)
    return render_template('view_record.html', record=record)

@app.route('/record/<int:id>/edit', methods=['GET', 'POST'])
def edit_record(id):
    record = HealthRecord.query.get_or_404(id)
    if request.method == 'POST':
        try:
            record.patient_name = request.form['patient_name']
            record.date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d')
            record.medical_condition = request.form['medical_condition']
            record.treatment = request.form['treatment']
            db.session.commit()
            flash('Health record updated successfully!', 'success')
            return redirect(url_for('view_record', id=record.id))
        except Exception as e:
            flash('Error updating record. Please try again.', 'error')
    return render_template('edit_record.html', record=record)

@app.route('/record/<int:id>/delete', methods=['POST'])
def delete_record(id):
    record = HealthRecord.query.get_or_404(id)
    try:
        db.session.delete(record)
        db.session.commit()
        flash('Health record deleted successfully!', 'success')
    except Exception as e:
        flash('Error deleting record. Please try again.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)