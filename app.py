import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
from functools import wraps

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'smartattendancesystem'  # For session management
app.config['DATABASE'] = 'database.db'

# Database helper functions
def get_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        db = get_db()
        with open('schema.sql', 'r') as f:
            db.executescript(f.read())
        db.commit()

# Create database tables if they don't exist
def setup_database():
    if not os.path.exists(app.config['DATABASE']):
        init_db()
        # Insert default users
        db = get_db()
        
        # Admin
        db.execute(
            'INSERT INTO users (username, password, role, name) VALUES (?, ?, ?, ?)',
            ('MeghaShinde', generate_password_hash('admin123'), 'admin', 'Megha Shinde')
        )
        
        # Teachers
        teachers = [
            ('saloni', generate_password_hash('teach123'), 'teacher', 'Saloni Purkar', 'Network & Info Security'),
            ('ashwini', generate_password_hash('teach456'), 'teacher', 'Ashwini Patil', 'Class Teacher'),
            ('jyoti', generate_password_hash('teach789'), 'teacher', 'Jyoti Chandwade', 'Mobile App Dev')
        ]
        for teacher in teachers:
            db.execute(
                'INSERT INTO users (username, password, role, name, subject) VALUES (?, ?, ?, ?, ?)',
                teacher
            )
        
        # Students
        students = [
            ('vikas', generate_password_hash('stud123'), 'student', 'Vikas Gaikwad'),
            ('vedant', generate_password_hash('stud456'), 'student', 'Vedant Shivade'),
            ('rushad', generate_password_hash('stud789'), 'student', 'Rushad Adikane'),
            ('divesh', generate_password_hash('stud101'), 'student', 'Divesh More')
        ]
        for student in students:
            db.execute(
                'INSERT INTO users (username, password, role, name) VALUES (?, ?, ?, ?)',
                student
            )
        
        db.commit()

# Authentication helper functions
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            flash('Admin access required')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'teacher':
            flash('Teacher access required')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'student':
            flash('Student access required')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        
        db = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE username = ? AND role = ?',
            (username, role)
        ).fetchone()
        
        error = None
        if user is None:
            error = 'Invalid username or role.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
            
        if error is None:
            # Store user info in session
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['name'] = user['name']
            session['role'] = user['role']
            
            # Redirect based on role
            if role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif role == 'teacher':
                return redirect(url_for('teacher_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))
                
        flash(error)
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # This is just a dummy form that doesn't actually send emails
        flash('Your message has been sent successfully!')
    return render_template('contact.html')

# Admin routes
@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    db = get_db()
    total_students = db.execute('SELECT COUNT(*) FROM users WHERE role = "student"').fetchone()[0]
    total_teachers = db.execute('SELECT COUNT(*) FROM users WHERE role = "teacher"').fetchone()[0]
    total_attendance = db.execute('SELECT COUNT(*) FROM attendance').fetchone()[0]
    
    return render_template('dashboard_admin.html', 
                          total_students=total_students,
                          total_teachers=total_teachers,
                          total_attendance=total_attendance)

@app.route('/admin/manage-students', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_students():
    db = get_db()
    
    # Add new student
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        
        error = None
        if not name or not username or not request.form['password']:
            error = 'All fields are required.'
        elif db.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone() is not None:
            error = f"Username {username} is already taken."
            
        if error is None:
            db.execute(
                'INSERT INTO users (username, password, role, name) VALUES (?, ?, ?, ?)',
                (username, password, 'student', name)
            )
            db.commit()
            flash('Student added successfully!')
            return redirect(url_for('manage_students'))
            
        flash(error)
    
    # Get list of students
    students = db.execute('SELECT * FROM users WHERE role = "student"').fetchall()
    return render_template('manage_students.html', students=students)

@app.route('/admin/manage-teachers', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_teachers():
    db = get_db()
    
    # Add new teacher
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        subject = request.form['subject']
        
        error = None
        if not name or not username or not request.form['password'] or not subject:
            error = 'All fields are required.'
        elif db.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone() is not None:
            error = f"Username {username} is already taken."
            
        if error is None:
            db.execute(
                'INSERT INTO users (username, password, role, name, subject) VALUES (?, ?, ?, ?, ?)',
                (username, password, 'teacher', name, subject)
            )
            db.commit()
            flash('Teacher added successfully!')
            return redirect(url_for('manage_teachers'))
            
        flash(error)
    
    # Get list of teachers
    teachers = db.execute('SELECT * FROM users WHERE role = "teacher"').fetchall()
    return render_template('manage_teachers.html', teachers=teachers)

@app.route('/admin/mark-attendance', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_mark_attendance():
    db = get_db()
    teachers = db.execute('SELECT * FROM users WHERE role = "teacher"').fetchall()
    students = db.execute('SELECT * FROM users WHERE role = "student"').fetchall()
    
    if request.method == 'POST':
        teacher_id = request.form['teacher_id']
        attendance_date = request.form['date']
        subject = db.execute('SELECT subject FROM users WHERE id = ?', (teacher_id,)).fetchone()['subject']
        
        # Process each student's attendance
        for student_id in request.form.getlist('student_ids'):
            status = 'present' if f'status_{student_id}' in request.form else 'absent'
            notes = request.form.get(f'note_{student_id}', '')
            
            # Check if attendance record already exists
            existing = db.execute(
                'SELECT * FROM attendance WHERE student_id = ? AND date = ? AND subject = ?', 
                (student_id, attendance_date, subject)
            ).fetchone()
            
            if existing:
                db.execute(
                    'UPDATE attendance SET status = ?, notes = ? WHERE student_id = ? AND date = ? AND subject = ?',
                    (status, notes, student_id, attendance_date, subject)
                )
            else:
                db.execute(
                    'INSERT INTO attendance (student_id, teacher_id, date, status, subject, notes) VALUES (?, ?, ?, ?, ?, ?)',
                    (student_id, teacher_id, attendance_date, status, subject, notes)
                )
                
        db.commit()
        flash('Attendance recorded successfully!')
    
    today = date.today().isoformat()
    return render_template('admin_mark_attendance.html', teachers=teachers, students=students, today=today)

@app.route('/admin/reports')
@login_required
@admin_required
def admin_reports():
    db = get_db()
    
    students = db.execute('SELECT * FROM users WHERE role = "student"').fetchall()
    
    # Get attendance data if student filter is applied
    student_id = request.args.get('student_id')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    attendance_data = []
    if student_id:
        query = '''
            SELECT a.*, s.name as student_name, t.name as teacher_name
            FROM attendance a
            JOIN users s ON a.student_id = s.id
            JOIN users t ON a.teacher_id = t.id
            WHERE a.student_id = ?
        '''
        params = [student_id]
        
        if date_from:
            query += ' AND a.date >= ?'
            params.append(date_from)
        if date_to:
            query += ' AND a.date <= ?'
            params.append(date_to)
            
        attendance_data = db.execute(query, params).fetchall()
    
    return render_template('admin_reports.html', students=students, attendance_data=attendance_data)

# Teacher routes
@app.route('/teacher/dashboard')
@login_required
@teacher_required
def teacher_dashboard():
    db = get_db()
    teacher_id = session['user_id']
    subject = db.execute('SELECT subject FROM users WHERE id = ?', (teacher_id,)).fetchone()['subject']
    
    total_students = db.execute('SELECT COUNT(*) FROM users WHERE role = "student"').fetchone()[0]
    
    # Get attendance statistics
    today = date.today().isoformat()
    today_present = db.execute(
        'SELECT COUNT(*) FROM attendance WHERE teacher_id = ? AND date = ? AND status = "present"',
        (teacher_id, today)
    ).fetchone()[0]
    
    return render_template('dashboard_teacher.html', 
                          subject=subject,
                          total_students=total_students,
                          today_present=today_present)

@app.route('/teacher/mark-attendance', methods=['GET', 'POST'])
@login_required
@teacher_required
def teacher_mark_attendance():
    db = get_db()
    teacher_id = session['user_id']
    subject = db.execute('SELECT subject FROM users WHERE id = ?', (teacher_id,)).fetchone()['subject']
    students = db.execute('SELECT * FROM users WHERE role = "student"').fetchall()
    
    # Set today's date as default
    selected_date = request.args.get('date', date.today().isoformat())
    
    # Get existing attendance data for the selected date
    attendance_data = {}
    notes_data = {}
    existing_records = db.execute(
        'SELECT student_id, status, notes FROM attendance WHERE teacher_id = ? AND date = ? AND subject = ?',
        (teacher_id, selected_date, subject)
    ).fetchall()
    
    for record in existing_records:
        attendance_data[record['student_id']] = record['status']
        notes_data[record['student_id']] = record['notes']
    
    if request.method == 'POST':
        attendance_date = request.form['date']
        
        # Process each student's attendance
        for student_id in request.form.getlist('student_ids'):
            status = 'present' if f'status_{student_id}' in request.form else 'absent'
            notes = request.form.get(f'note_{student_id}', '')
            
            # Check if attendance record already exists
            existing = db.execute(
                'SELECT * FROM attendance WHERE student_id = ? AND date = ? AND subject = ?', 
                (student_id, attendance_date, subject)
            ).fetchone()
            
            if existing:
                db.execute(
                    'UPDATE attendance SET status = ?, notes = ? WHERE student_id = ? AND date = ? AND subject = ?',
                    (status, notes, student_id, attendance_date, subject)
                )
            else:
                db.execute(
                    'INSERT INTO attendance (student_id, teacher_id, date, status, subject, notes) VALUES (?, ?, ?, ?, ?, ?)',
                    (student_id, teacher_id, attendance_date, status, subject, notes)
                )
                
        db.commit()
        flash('Attendance recorded successfully!')
        # Redirect to same page with the date parameter to show the updated records
        return redirect(url_for('teacher_mark_attendance', date=attendance_date))
    
    return render_template(
        'teacher_mark_attendance.html', 
        students=students, 
        today=selected_date, 
        subject=subject,
        attendance_data=attendance_data,
        notes_data=notes_data
    )

@app.route('/teacher/reports')
@login_required
@teacher_required
def teacher_reports():
    db = get_db()
    teacher_id = session['user_id']
    subject = db.execute('SELECT subject FROM users WHERE id = ?', (teacher_id,)).fetchone()['subject']
    
    students = db.execute('SELECT * FROM users WHERE role = "student"').fetchall()
    student_stats = []
    
    for student in students:
        total_classes = db.execute(
            'SELECT COUNT(*) FROM attendance WHERE student_id = ? AND teacher_id = ?',
            (student['id'], teacher_id)
        ).fetchone()[0]
        
        if total_classes > 0:
            present_count = db.execute(
                'SELECT COUNT(*) FROM attendance WHERE student_id = ? AND teacher_id = ? AND status = "present"',
                (student['id'], teacher_id)
            ).fetchone()[0]
            
            attendance_percent = round((present_count / total_classes) * 100, 2)
        else:
            attendance_percent = 0
            
        student_stats.append({
            'id': student['id'],
            'name': student['name'],
            'attendance_percent': attendance_percent,
            'total_classes': total_classes
        })
    
    return render_template('teacher_reports.html', student_stats=student_stats, subject=subject)

# Student routes
@app.route('/student/dashboard')
@login_required
@student_required
def student_dashboard():
    db = get_db()
    student_id = session['user_id']
    
    # Get attendance summary
    total_classes = db.execute(
        'SELECT COUNT(*) FROM attendance WHERE student_id = ?',
        (student_id,)
    ).fetchone()[0]
    
    present_count = db.execute(
        'SELECT COUNT(*) FROM attendance WHERE student_id = ? AND status = "present"',
        (student_id,)
    ).fetchone()[0]
    
    absent_count = total_classes - present_count
    
    attendance_percent = round((present_count / total_classes) * 100, 2) if total_classes > 0 else 0
    
    return render_template('dashboard_student.html', 
                          present_count=present_count,
                          absent_count=absent_count,
                          attendance_percent=attendance_percent)

@app.route('/student/view-attendance')
@login_required
@student_required
def student_view_attendance():
    db = get_db()
    student_id = session['user_id']
    
    attendance_records = db.execute('''
        SELECT a.*, t.name as teacher_name, t.subject 
        FROM attendance a
        JOIN users t ON a.teacher_id = t.id
        WHERE a.student_id = ?
        ORDER BY a.date DESC
    ''', (student_id,)).fetchall()
    
    return render_template('student_view_attendance.html', attendance_records=attendance_records)

# User management routes
@app.route('/admin/edit-student/<int:student_id>', methods=['POST'])
@login_required
@admin_required
def edit_student(student_id):
    db = get_db()
    
    name = request.form['name']
    username = request.form['username']
    password = request.form.get('password')
    
    # Check if username already exists for another user
    existing_user = db.execute('SELECT id FROM users WHERE username = ? AND id != ?', 
                               (username, student_id)).fetchone()
    if existing_user:
        flash(f"Username {username} is already taken.")
        return redirect(url_for('manage_students'))
    
    if password and password.strip():
        # Update with new password
        db.execute('UPDATE users SET name = ?, username = ?, password = ? WHERE id = ?',
                  (name, username, generate_password_hash(password), student_id))
    else:
        # Keep existing password
        db.execute('UPDATE users SET name = ?, username = ? WHERE id = ?',
                  (name, username, student_id))
    
    db.commit()
    flash('Student updated successfully!')
    return redirect(url_for('manage_students'))

@app.route('/admin/delete-student/<int:student_id>', methods=['POST'])
@login_required
@admin_required
def delete_student(student_id):
    db = get_db()
    
    # Delete student's attendance records first (foreign key constraint)
    db.execute('DELETE FROM attendance WHERE student_id = ?', (student_id,))
    
    # Then delete the student
    db.execute('DELETE FROM users WHERE id = ?', (student_id,))
    
    db.commit()
    flash('Student deleted successfully!')
    return redirect(url_for('manage_students'))

@app.route('/admin/edit-teacher/<int:teacher_id>', methods=['POST'])
@login_required
@admin_required
def edit_teacher(teacher_id):
    db = get_db()
    
    name = request.form['name']
    username = request.form['username']
    subject = request.form['subject']
    password = request.form.get('password')
    
    # Check if username already exists for another user
    existing_user = db.execute('SELECT id FROM users WHERE username = ? AND id != ?', 
                               (username, teacher_id)).fetchone()
    if existing_user:
        flash(f"Username {username} is already taken.")
        return redirect(url_for('manage_teachers'))
    
    if password and password.strip():
        # Update with new password
        db.execute('UPDATE users SET name = ?, username = ?, subject = ?, password = ? WHERE id = ?',
                  (name, username, subject, generate_password_hash(password), teacher_id))
    else:
        # Keep existing password
        db.execute('UPDATE users SET name = ?, username = ?, subject = ? WHERE id = ?',
                  (name, username, subject, teacher_id))
    
    db.commit()
    flash('Teacher updated successfully!')
    return redirect(url_for('manage_teachers'))

@app.route('/admin/delete-teacher/<int:teacher_id>', methods=['POST'])
@login_required
@admin_required
def delete_teacher(teacher_id):
    db = get_db()
    
    # Delete teacher's attendance records first (foreign key constraint)
    db.execute('DELETE FROM attendance WHERE teacher_id = ?', (teacher_id,))
    
    # Then delete the teacher
    db.execute('DELETE FROM users WHERE id = ?', (teacher_id,))
    
    db.commit()
    flash('Teacher deleted successfully!')
    return redirect(url_for('manage_teachers'))

# Main entry point
if __name__ == '__main__':
    setup_database()
    app.run(debug=True) 