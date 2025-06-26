from flask import Flask, render_template, request, redirect, flash, session, url_for, jsonify
import sqlite3
import cohere
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Cohere API
co = cohere.Client("xoPf1S2WDWlw5KCQehfAPQPdsehkrnMZn4VNJWA1")

# SQLite DB path
DB_PATH = "users.db"

def db_connection():
    return sqlite3.connect(DB_PATH)


# -------------------- Home --------------------
@app.route('/')
def home():
    return render_template('views/index1.html',
                           user_name=session.get('username', 'Guest'),
                           user_phone=session.get('phone_no', ''),
                           user_email=session.get('email', ''),
                           latest_request={'Status': "Accepted", 'report': None})


# -------------------- Signup --------------------
@app.route('/register_user', methods=['POST'])
def signup():
    try:
        data = request.form
        first_name = data['first_name']
        last_name = data['last_name']
        ern = data.get('ern')
        email = data['email']
        phone_no = data['phone_no']
        password = data['password']
        role_id = 3
        is_member = 1 if email.endswith('@gsfcuniversity.ac.in') else 0

        conn = db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (first_name, last_name, ern, email, phone_no, password, role_id, is_member)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (first_name, last_name, ern, email, phone_no, password, role_id, is_member))
        conn.commit()

        cursor.execute("""
            SELECT id, email, role_id, first_name, last_name, phone_no 
            FROM users WHERE email = ?
        """, (email,))
        user = cursor.fetchone()
        conn.close()

        if user:
            session.permanent = True
            session['UserID'] = user[0]
            session['email'] = user[1]
            session['RoleID'] = user[2]
            session['username'] = f"{user[3]} {user[4]}"
            session['phone_no'] = user[5]
            flash(f"Welcome {session['username']}!", 'success')
            return redirect(url_for('home'))

        flash("Signup failed.", 'danger')
        return redirect(url_for('user_login'))

    except sqlite3.IntegrityError:
        flash('Email already registered.', 'danger')
        return redirect(url_for('user_login'))

    except Exception as e:
        print(f"❌ Signup Error: {e}")
        flash('Unexpected error during signup.', 'danger')
        return redirect(url_for('user_login'))


# -------------------- Login --------------------
@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        login_input = request.form['login_input']
        password = request.form['login_password']

        try:
            conn = db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, email, password, role_id, first_name, last_name, phone_no 
                FROM users 
                WHERE email = ? OR phone_no = ?
            """, (login_input, login_input))
            user = cursor.fetchone()
            conn.close()

            if user:
                db_password = user[2]
                if password.strip() == db_password.strip():
                    session.permanent = True
                    session['UserID'] = user[0]
                    session['email'] = user[1]
                    session['RoleID'] = user[3]
                    session['username'] = f"{user[4]} {user[5]}"
                    session['phone_no'] = user[6]
                    flash(f"Welcome back, {session['username']}", 'success')
                    return redirect(url_for('home'))
                else:
                    flash("Incorrect password.", 'danger')
            else:
                flash("No account found with this email/phone.", 'danger')
            return redirect(url_for('user_login'))

        except Exception as e:
            print(f"⚠️ Login Error: {e}")
            flash('Login failed.', 'danger')
            return redirect(url_for('user_login'))

    return render_template('views/login.html')


# -------------------- Logout --------------------
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for('user_login'))


# -------------------- Chatbot Page --------------------
@app.route('/chatbot')
def chatbot():
    return render_template("views/chatbot.html", user_name=session.get('username', 'Guest'),
                           user_phone=session.get('phone_no', ''),
                           user_email=session.get('email', ''),
                           latest_request={'Status': "Accepted", 'report': None})



# -------------------- Chatbot API --------------------
@app.route("/send_message", methods=["POST"])
def send_message():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"reply": "I didn't receive any message."})

    try:
        response = co.generate(
            model="command",
            prompt=f"User: {user_message}\nBot:",
            max_tokens=100,
            temperature=0.7
        )
        bot_reply = response.generations[0].text.strip()
        return jsonify({"reply": bot_reply})

    except Exception as e:
        print(f"⚠️ Cohere Error: {e}")
        return jsonify({"reply": "Sorry, I'm having trouble responding right now."})


# -------------------- Dummy Routes --------------------
@app.route('/about')
def about():
    return render_template('views/about.html')

@app.route('/requests')
def requests_view():
    return "Requests Page (dummy route)"

@app.route('/dashboard')
def manager_dashboard():
    return "Manager Dashboard Page (dummy route)"

@app.route('/admin')
def admin_login():
    return "Admin Page (dummy route)"

@app.route("/book_equipment")
def book_equipment():
    return 'Book Equipment Page (dummy route)'

@app.route('/lab_equipment')
def lab_equipment():
    return 'Lab Equipment Page (dummy route)'


# -------------------- Run App --------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
