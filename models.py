

from datetime import date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    employee_id = db.Column(db.String(100), unique=True, nullable=False)
    tasks = db.relationship('Task', backref='employee', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=date.today, nullable=False)
    task_description = db.Column(db.String(200), nullable=False)
    product = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    remarks = db.Column(db.String(200))
    clickup_matis_id = db.Column(db.String(100))
    employee_id = db.Column(db.String(100), db.ForeignKey('employee.employee_id'), nullable=False)

