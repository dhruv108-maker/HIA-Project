from flask import render_template, Flask, redirect, flash

app = Flask(__name__)


@app.route('/')
def home():
    # Dummy user info
    user_name = "Dhruv Verma"
    user_phone = "+91 9409045205"
    user_email = "23sc06007@gsfcuniversity.ac.in"

    # Dummy request stats
    user_total_requests = 10
    user_completed_requests = 6
    user_pending_requests = 2

    # Dummy latest request info
    latest_request = {
        'Status': "Accepted",
        'report': None
    }

    return render_template('views/index.html',
                           user_name=user_name,
                           user_phone=user_phone,
                           user_email=user_email,
                           user_total_requests=user_total_requests,
                           user_completed_requests=user_completed_requests,
                           user_pending_requests=user_pending_requests,
                           latest_request=latest_request)

# User login route
@app.route('/login')
def user_login():
    return "Login Page (dummy route)"

# About page
@app.route('/about')
def about():
    return render_template('views/about.html')


# Requests page
@app.route('/requests')
def requests_view():
    return "Requests Page (dummy route)"

# Manager dashboard
@app.route('/dashboard')
def manager_dashboard():
    return "Manager Dashboard Page (dummy route)"

# Admin login
@app.route('/admin')
def admin_login():
    return "Admin Page (dummy route)"

@app.route("/book_equipment")
def book_equipment():
    return 'Book Equipment Page (dummy route)'

@app.route('/lab_equipment')
def lab_equipment():
    return 'Lab Equipment Page (dummy route)'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)