# initiated notifi trigger
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import date, datetime
from models import db, Employee, Task
from exportpdf import generate_pdf

app = Flask(__name__)

#secret key for sessions
app.secret_key = 'a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef123456'

# App Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:4605@localhost:5432/task_manager'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Flask-Migrate
db.init_app(app)
migrate = Migrate(app, db)

ADMIN_USERNAME = 'xyz'
ADMIN_PASSWORD = '123'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form.get('role')

        if role == 'employee':
            return redirect(url_for('employee_input'))

        elif role == 'admin':
            username = request.form.get('username')
            password = request.form.get('password')

            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                return redirect(url_for('admin'))
            else:
                return render_template('login.html', error='Invalid admin credentials.')

    return render_template('login.html')


@app.route('/employee_input', methods=['GET', 'POST'])
def employee_input():
    if request.method == 'POST':
        name = request.form['name']
        employee_id = request.form['employee_id']

        # Check
        existing_employee = Employee.query.filter_by(employee_id=employee_id).first()
        if not existing_employee:
            
            new_employee = Employee(name=name, employee_id=employee_id)
            db.session.add(new_employee)
            db.session.commit()
            flash('Employee added successfully.', 'success')
            return redirect(url_for('task_input', emp_id=new_employee.employee_id))
        else:
            flash('Employee with this ID already exists.', 'info')
            # changed employee.id to employee.employee_id
            return redirect(url_for('task_input', emp_id=existing_employee.employee_id))

    return render_template('employee_input.html')


@app.route('/task/<string:emp_id>', methods=['GET', 'POST'])
def task_input(emp_id):
    # employee = Employee.query.get_or_404(emp_id)
    employee = Employee.query.filter_by(employee_id=emp_id).first_or_404()
    if request.method == 'POST':
        task_description = request.form['task_description']
        product = request.form['product']
        status = request.form['status']
        remarks = request.form.get('remarks')
        clickup_matis_id = request.form.get('clickup_matis_id')

        task = Task(
            task_description=task_description,
            product=product,
            status=status,
            remarks=remarks,
            clickup_matis_id=clickup_matis_id,
            # changed id to employee_id
            employee_id=employee.employee_id
        )
        db.session.add(task)
        db.session.commit()
        if request.form['submit'] == 'Close Day':
            return redirect(url_for('login'))
        elif request.form['submit'] == 'Next Task':
            return redirect(url_for('task_input', emp_id=emp_id))
    return render_template('task_input.html', employee=employee, date=date.today().strftime('%Y-%m-%d'))


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    try:
        if request.method == 'POST':
            emp_id = request.form.get('employee_id')
            date_from_str = request.form.get('date_from')
            date_to_str = request.form.get('date_to')

            # Convert date strings to date objects
            try:
                date_from = datetime.strptime(date_from_str, '%Y-%m-%d').date()
                date_to = datetime.strptime(date_to_str, '%Y-%m-%d').date()
            except ValueError:
                return 'Invalid date format. Use YYYY-MM-DD.', 400

            employee = Employee.query.filter_by(employee_id=emp_id).first()
            if employee:
                tasks = Task.query.filter(
                    Task.date.between(date_from, date_to),
                    Task.employee_id == employee.employee_id
                ).all()
                if tasks:
                    pdf_path = generate_pdf(tasks, employee, date_from, date_to)
                    return send_file(pdf_path, as_attachment=True)
                else:
                    return 'No tasks found for this employee on the given dates.', 404
            else:
                return 'Employee not found.', 404
        return render_template('admin.html')
    except Exception as e:
        print(f"An error occurred: {e}")
        return 'An internal error occurred.', 500

if __name__ == "__main__":
    app.run(debug=True)
