
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session,Response
import pyodbc
import secrets
from flask_bcrypt import Bcrypt
import csv
from io import StringIO
from datetime import datetime



app = Flask(__name__)
bcrypt = Bcrypt(app)
# THIS IS  KEY FOR SESSIONS
app.secret_key = secrets.token_hex(16)

# Database connection
server = 'WANI-SOB\\MSSQLSERVER01'
database = 'event_management'
username = 'sa'
password = 'Server@123'
conn_str = (
    f"DRIVER=ODBC Driver 17 for SQL Server;"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password}"
)

# LANDING PAGE WHEN USER LOGS IN HE WILL BE REDIRECTED
@app.route('/index')
def index():
    # Check if user is logged in
    if not session.get('logged_in'):
        return redirect(url_for('/'))
     
    email = session.get('email')
    print(email)
    username = email[0:4]
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, description, event_date, last_registration_date,vacancies, venue, is_open FROM Events ORDER BY id DESC")
        events = cursor.fetchall()
        # current_date = datetime.now()    
        # print(current_date)   
        print(events)
        return render_template('/Landing_page/index.html',events=events, username=username)
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return render_template('error.html', error_message="An error occurred while fetching data.")
    
    finally:
        cursor.close()
        conn.close()

@app.route('/sign_up_user', methods=['GET', 'POST'])
def sign_up_user():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        password= hashed_password
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        print("hasshed",password)
        try:
            # Insert data into the sign_up_user table
            cursor.execute('''
                INSERT INTO signupuser (username, email, password)
                VALUES (?, ?, ?)
            ''', (username, email, password))

            
            conn.commit()

            return jsonify({
                'message': 'User registered successfully',
                'redirect_url': '/'
            }), 200
        
        except Exception as e:
            return jsonify({'message': str(e)}), 500
        
        finally:
            cursor.close()
            conn.close()
    
    else:
        return render_template('./userSignUpFolder/userSignUp.html')




@app.route('/login', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            session['is_admin'] = True
            return jsonify({
                'status': 'success', 
                'redirect_url': 'admin/dashboard',
                'message': 'Login successful'
            }), 200
        else:
            return jsonify({
                'status': 'error', 
                'message': 'Invalid credentials'
            }), 401

    return render_template('./Admin/admin_login.html')
@app.route('/')
def login_page():
    return render_template('./userLoginFolder/userLogin.html')
@app.route('/userLogin', methods=['POST'])
def userLogin():
    data = request.get_json()
    email = data.get('email')
    print("while logging email is :", email)
    login_password = data.get('password')
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    try:
        query = "SELECT password FROM signupuser WHERE email = ?"
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        print(user, "before fetching")
        if user:
            db_password = user[0]  # The password is the first element in the tuple
            
            if bcrypt.check_password_hash(db_password, login_password):
                # Create a session for the logged-in user
                session['logged_in'] = True
                session['email'] = email

                return jsonify({
                    "success": 'True', 
                    "redirect_url": "/index"
                }), 200
            else:
                return jsonify({"message": "Password is incorrect"}), 400
        else:
            return jsonify({
                "success": False, 
                "message": "Invalid email or password"
            }), 401
    
    except Exception as e:
        return jsonify({
            "success": False, 
            "message": str(e)
        }), 500
    
    finally:
        cursor.close()
        conn.close()
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('login_page'))
@app.route('/admin_loggedout')
def admin_loggedout():
    return render_template('Admin/admin_login.html')
@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('is_admin'):
        flash('Unauthorized access. Please log in as admin.', 'danger')
        return redirect(url_for('admin_login')) 
    return render_template('/Dashboard/admin_dashboard.html')
@app.route('/admin/events', methods=['GET', 'POST'])
def manage_events():
    if not session.get('is_admin'):
        flash('Unauthorized access. Please log in as admin.', 'danger')
        return redirect(url_for('admin_login'))  
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor() 
    try:
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            event_date = request.form['event_date']
            vacancies = request.form['vacancies']
            venue = request.form['venue']
            last_date = request.form['last_registration_date']
            is_open = request.form.get('is_open', '1')  # Default to '1' (Open) if not provided          
            cursor.execute("""
                INSERT INTO events (name, description, event_date, last_registration_date ,vacancies, venue, is_open) 
                VALUES (?, ?, ?, ?, ?, ? , ?)
            """, (name, description, event_date,last_date, vacancies, venue, int(is_open)))
            conn.commit()
            flash('Event created successfully!', 'success')
            return redirect(url_for('manage_events'))
        cursor.execute("""
            SELECT id, name, description, event_date, last_registration_date , vacancies, venue, is_open 
            FROM events
        """)
        events = cursor.fetchall()
        print(events)
        return render_template('/Manage_events/manage_events.html', events=events)
    finally:
        cursor.close()
        conn.close()
@app.route('/admin/delete_event/<int:event_id>')
def delete_event(event_id):
    if not session.get('is_admin'):
        flash('Unauthorized access. Please log in as admin.', 'danger')
        return redirect(url_for('admin_login'))
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Events WHERE id = ?", event_id)
        conn.commit()
        flash('Event deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting event: {str(e)}', 'danger')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('manage_events'))

@app.route('/admin/edit_event', methods=['POST'])
def edit_event():
    if not session.get('is_admin'):
        flash('Unauthorized access. Please log in as admin.', 'danger')
        return redirect(url_for('admin_login'))
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    try:
        event_id = request.form['event_id']
        name = request.form['name']
        description = request.form['description']
        event_date = request.form['event_date']
        vacancies = request.form['vacancies']
        last_registration_date = request.form['last_registration_date']
        cursor.execute("""
            UPDATE Events 
            SET name = ?, description = ?, event_date = ?, last_registration_date = ? , vacancies = ?
            WHERE id = ?
        """, (name, description, event_date,last_registration_date,  vacancies, event_id))
        conn.commit()
        flash('Event updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating event: {str(e)}', 'danger')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('manage_events'))

@app.route('/update_event_status/<int:event_id>/<int:new_status>', methods=['GET'])
def update_event_status(event_id, new_status):
    # Check if admin is logged in
    if not session.get('is_admin'):
        flash('Unauthorized access. Please log in as admin.', 'danger')
        return redirect(url_for('admin_login'))
    
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    try:
        cursor.execute("UPDATE events SET is_open = ? WHERE id = ?", (new_status, event_id))
        conn.commit()
        flash('Event status updated successfully!', 'success')
        message = "Event update successsfully"
    except Exception as e:
        flash(f'Error updating event status: {str(e)}', 'danger')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('manage_events', message=message))

@app.route('/search_events')
def search_events():
    if not session.get('logged_in'):
        flash('Please log in to search events', 'warning')
        return redirect(url_for('login_page'))
    
    query = request.args.get('query', '')
    filter_type = request.args.get('filter', 'name')
    email = session.get('email')
    
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    events = []
    message = None

    try:
        if filter_type == 'name' and query:
            # Search events by name
            cursor.execute("SELECT id, name, description, event_date, venue, last_registration_date ,vacancies,is_open FROM events WHERE name LIKE ?", f"%{query}%")
            events = cursor.fetchall()
            message = f"Events found for your search: '{query}' by name."
            if not events:
                message = f"No events found for your search: '{query}' by name."
        elif filter_type == 'date' and query:
            # Search events by date
            cursor.execute("SELECT id, name, description, event_date, venue,last_registration_date ,vacancies, is_open FROM events WHERE event_date = ?", query)
            events = cursor.fetchall()
            message = f"Events found for your search: '{query}' by date."
            if not events:
                message = f"No events found for your search: '{query}' by date."
        else:
            # Fetch all events if no search query
            message = "Please choose a filter type"
            cursor.execute("SELECT id, name, description, event_date, last_registration_date, vacancies,venue, is_open FROM events")
            events = cursor.fetchall()

    except pyodbc.Error as e:
        print(f"Database error: {e}")
    finally:
        cursor.close()
        conn.close()


    return render_template('/Landing_page/index.html', events=events, message=message)

def check_registration(event_id):
    user_email = session.get('email')
    
    if not user_email:
        return jsonify({
            'is_registered': False,
            'error': 'User not logged in'
        }), 401
    
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        query = """
        SELECT COUNT(*) AS registration_count 
        FROM Event_registrations 
        WHERE email = ? AND event_id = ?
        """
        cursor.execute(query, (user_email, event_id))
        
        result = cursor.fetchone()
        is_registered = result.registration_count > 0
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'is_registered': is_registered
        })
    
    except pyodbc.Error as e:
        return jsonify({
            'is_registered': False,
            'error': str(e)
        }), 500

def register_event():
    user_email = session.get('email')
    
    if not user_email:
        return jsonify({
            'success': False, 
            'message': 'User not logged in'
        }), 401
    
    data = request.json
    event_id = data.get('event_id')
    
    if not event_id:
        return jsonify({
            'success': False, 
            'message': 'Invalid event ID'
        }), 400
    
    try:
        
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        check_query = """
        SELECT COUNT(*) AS registration_count 
        FROM Event_registrations 
        WHERE email = ? AND event_id = ?
        """
        cursor.execute(check_query, (user_email, event_id))
        result = cursor.fetchone()
        
        if result.registration_count > 0:
            cursor.close()
            conn.close()
            return jsonify({
                'success': False, 
                'message': 'Already registered for this event'
            })
        
        insert_query = """
        INSERT INTO Event_registrations (email, event_id, registration_date) 
        VALUES (?, ?, GETDATE())
        """
        cursor.execute(insert_query, (user_email, event_id))
        message = f"Registration is Successfull"
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'success': True, message:message})
    
    except pyodbc.Error as e:
        if 'conn' in locals():
            conn.rollback()
        
        return jsonify({
            'success': False, 
            'message': f'Registration failed: {str(e)}'
        }), 500

@app.route('/check_registration/<int:event_id>')
def check_registration_route(event_id):
    return check_registration(event_id)

@app.route('/register_event', methods=['POST'])
def register_event_route():
    return register_event()

@app.route('/check_registration_status/<int:event_id>', methods=['GET'])
def check_registration_status(event_id):
    try:
        conn = pyodbc.connect(conn_str)

        cursor = conn.cursor()

        query = "SELECT is_open FROM events WHERE id = ?"
        cursor.execute(query, (event_id,))
        result = cursor.fetchone()

        conn.close()  # Close the database connection

        if result is not None:
            is_open = result[0]  # Assuming 1 = open, 0 = closed
            return jsonify({'is_open': bool(is_open)})  # Convert to boolean for clarity
        else:
            return jsonify({'error': 'Event not found'}), 404

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)