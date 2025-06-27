from flask import Flask, render_template, request, redirect, flash, session, url_for, jsonify
import sqlite3
import cohere
import os
from Modules.text_extractor import extract_text_from_pdf
from werkzeug.utils import secure_filename
from ML.Predictor.predictor_bot import heart_disease_predictor




app = Flask(__name__)
app.secret_key = "supersecretkey"



# Cohere API
co = cohere.Client("xoPf1S2WDWlw5KCQehfAPQPdsehkrnMZn4VNJWA1")

# SQLite DB path
DB_PATH = "users.db"

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


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
# @app.route('/chatbot')
# def chatbot():
#     return render_template("views/chatbot.html", user_name=session.get('username', 'Guest'),
#                            user_phone=session.get('phone_no', ''),
#                            user_email=session.get('email', ''),
#                            latest_request={'Status': "Accepted", 'report': None})


@app.route('/chatbot')
def chatbot():
    if 'UserID' not in session:
        flash("Please log in to use the chatbot.", "warning")
        return redirect(url_for('user_login'))

    user_id = session['UserID']
    chats = []

    try:
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT query, response, timestamp 
            FROM chats 
            WHERE user_id = ? 
            ORDER BY timestamp DESC
        """, (user_id,))
        chats = cursor.fetchall()
        # print(chats)
        conn.close()
    except Exception as e:
        print("⚠️ Chat fetch error:", e)


    return render_template("views/chatbot.html",
                           user_name=session.get('username', 'Guest'),
                           user_phone=session.get('phone_no', ''),
                           user_email=session.get('email', ''),
                           latest_request={'Status': "Accepted", 'report': None},
                           chat_history=chats if user_id else [])



# -------------------- Chatbot API --------------------


# @app.route("/send_message", methods=["POST"])
# def send_message():
#     user_message = request.form.get("message", "")
#     uploaded_file = request.files.get("file", None)

#     pdf_text = ""
#     if uploaded_file and uploaded_file.filename.endswith(".pdf"):
#         try:
#             filename = secure_filename(uploaded_file.filename)
#             filepath = os.path.join(UPLOAD_FOLDER, filename)
#             uploaded_file.save(filepath)
#             pdf_text = extract_text_from_pdf(filepath)
#         except Exception as e:
#             print(f"⚠️ PDF Processing Error: {e}")
#             return jsonify({"reply": "Failed to read the PDF file."})

#     # Combine both inputs
#     combined_prompt = f"User: {user_message}\n\nPDF Content:\n{pdf_text.strip()}\n\nBot:"

#     try:
#         response = co.generate(
#             model="command",
#             prompt=combined_prompt,
#             max_tokens=500,
#             temperature=0.7
#         )
#         bot_reply = response.generations[0].text.strip()
#         return jsonify({"reply": bot_reply})

#     except Exception as e:
#         print(f"⚠️ Cohere Error: {e}")
#         return jsonify({"reply": "Sorry, I'm having trouble responding right now."})


# @app.route("/send_message", methods=["POST"])
# def send_message():
#     user_id = session.get("UserID")
#     user_message = request.form.get("message", "")
#     uploaded_file = request.files.get("file", None)

#     pdf_text = ""
#     if uploaded_file and uploaded_file.filename.endswith(".pdf"):
#         try:
#             filename = secure_filename(uploaded_file.filename)
#             filepath = os.path.join(UPLOAD_FOLDER, filename)
#             uploaded_file.save(filepath)
#             pdf_text = extract_text_from_pdf(filepath)
#         except Exception as e:
#             print(f"⚠️ PDF Processing Error: {e}")
#             return jsonify({"reply": "Failed to read the PDF file."})
        
#     #Ml model to predict heat disease based on input csv file
#     if uploaded_file and uploaded_file.filename.endswith(".csv"):
#         try:
#             filename = secure_filename(uploaded_file.filename)
#             filepath = os.path.join(UPLOAD_FOLDER, filename)
#             uploaded_file.save(filepath)
#             results = heart_disease_predictor(filepath)
#         except Exception as e:
#             print(f"⚠️ PDF Processing Error: {e}")
#             return jsonify({"reply": "Failed to read the PDF file."})

            

#     combined_prompt = f"User: {user_message}\n\nPDF Content:\n{pdf_text.strip()}\n\nBot:"

#     try:
#         response = co.generate(
#             model="command",
#             prompt=combined_prompt,
#             max_tokens=500,
#             temperature=0.7
#         )
#         bot_reply = response.generations[0].text.strip()

#         # ✅ Store in database if user is logged in
#         if user_id:
#             try:
#                 conn = db_connection()
#                 cursor = conn.cursor()
#                 cursor.execute("""
#                     INSERT INTO chats (user_id, query, response)
#                     VALUES (?, ?, ?)
#                 """, (user_id, user_message, bot_reply))
#                 conn.commit()
#                 conn.close()
#             except Exception as db_error:
#                 print(f"⚠️ DB Insert Error: {db_error}")

#         return jsonify({"reply": bot_reply})

#     except Exception as e:
#         print(f"⚠️ Cohere Error: {e}")
#         return jsonify({"reply": "Sorry, I'm having trouble responding right now."})










# @app.route("/send_message", methods=["POST"])
# def send_message():
#     user_id = session.get("UserID")
#     user_message = request.form.get("message", "")
#     uploaded_file = request.files.get("file", None)

#     pdf_text = ""
#     prediction_result = None

#     if uploaded_file:
#         filename = secure_filename(uploaded_file.filename)
#         filepath = os.path.join(UPLOAD_FOLDER, filename)
#         uploaded_file.save(filepath)

#         # Handle PDF
#         if filename.endswith(".pdf"):
#             try:
#                 pdf_text = extract_text_from_pdf(filepath)
#             except Exception as e:
#                 print(f"⚠️ PDF Processing Error: {e}")
#                 return jsonify({"reply": "Failed to read the PDF file."})

#         # Handle CSV
#         if filename.endswith(".csv"):
#             try:
#                 prediction_result = heart_disease_predictor(filepath)

#                 # Prepare reply from prediction
#                 if prediction_result:
#                     reply = f"{prediction_result['verdict']} Probability: {prediction_result['probability']}%"

#                     # ✅ Save prediction result to DB as a chat
#                     if user_id:
#                         try:
#                             conn = db_connection()
#                             cursor = conn.cursor()
#                             cursor.execute("""
#                                 INSERT INTO chats (user_id, query, response)
#                                 VALUES (?, ?, ?)
#                             """, (user_id, uploaded_file.filename, reply))
#                             conn.commit()
#                             conn.close()
#                         except Exception as db_error:
#                             print(f"⚠️ DB Insert Error (CSV Prediction): {db_error}")

#                     # ✅ Send prediction as chatbot reply
#                     return jsonify({"reply": reply})
                
#                 os.remove(filepath)
#             except Exception as e:
#                 print(f"⚠️ CSV Prediction Error: {e}")
#                 return jsonify({"reply": "Failed to process the CSV file."})

#     # Fallback: AI response from Cohere if not CSV
#     combined_prompt = f"User: {user_message}\n\nPDF Content:\n{pdf_text.strip()}\n\nBot:"

#     try:
#         response = co.generate(
#             model="command",
#             prompt=combined_prompt,
#             max_tokens=500,
#             temperature=0.7
#         )
#         bot_reply = response.generations[0].text.strip()

#         # ✅ Store normal chat in DB
#         if user_id:
#             try:
#                 conn = db_connection()
#                 cursor = conn.cursor()
#                 cursor.execute("""
#                     INSERT INTO chats (user_id, query, response)
#                     VALUES (?, ?, ?)
#                 """, (user_id, user_message, bot_reply))
#                 conn.commit()
#                 conn.close()
#             except Exception as db_error:
#                 print(f"⚠️ DB Insert Error: {db_error}")

#         return jsonify({"reply": bot_reply})

#     except Exception as e:
#         print(f"⚠️ Cohere Error: {e}")
#         return jsonify({"reply": "Sorry, I'm having trouble responding right now."})






@app.route("/send_message", methods=["POST"])
def send_message():
    user_id      = session.get("UserID")
    user_message = request.form.get("message", "")
    uploaded     = request.files.get("file", None)

    pdf_text = ""
    # —————————————————————————————
    # 1) Handle file upload
    # —————————————————————————————
    if uploaded:
        fname    = secure_filename(uploaded.filename)
        fpath    = os.path.join(UPLOAD_FOLDER, fname)
        uploaded.save(fpath)

        # PDF → extract text
        if fname.lower().endswith(".pdf"):
            try:
                pdf_text = extract_text_from_pdf(fpath)
            except Exception as e:
                print("❌ PDF Error:", e)
                return jsonify({"reply": "Failed to read the PDF file."})

        # CSV → run predictor
        # CSV → run predictor
        if fname.lower().endswith(".csv"):
            try:
                result = heart_disease_predictor(fpath)

                if result is None:
                    raise ValueError("heart_disease_predictor returned None")

                prob    = result["probability"]
                result_in = str(f"Probability: {prob}%")
                
                prompt = (
                    f"You are a virtual health assistant. A user uploaded medical data and based on the analysis, "
                    f"the estimated probability of heart disease is {prob*100:.2f}%.\n\n"
                    
                    f"Your task is to:\n"
                    f"1. Explain this probability in simple, friendly language.\n"
                    f"2. Clearly state whether the risk is low, moderate, or high.\n"
                    f"3. Offer gentle, practical next steps (e.g., lifestyle advice, when to see a doctor).\n"
                    f"4. Avoid medical disclaimers or vague statements like 'not a definitive diagnosis'.\n\n"
                    
                    f"Output a short and human response (max 3 sentences), like you're speaking to a friend.\n\n"
                    f"Probability: {prob*100:.2f}%\n"
                    f"Response:"
                )

                
                cohere_response = co.generate(
                    model="command",
                    prompt=prompt,
                    max_tokens=100,
                    temperature=0.6
                )
                result_in = cohere_response.generations[0].text.strip()

                # store in DB as a chat
                if user_id:
                    try:
                        conn   = db_connection()
                        cursor = conn.cursor()
                        cursor.execute(
                            "INSERT INTO chats (user_id, query, response) VALUES (?, ?, ?)",
                            (user_id, fname, result_in )
                        )
                        conn.commit()
                        conn.close()
                    except Exception as db_e:
                        print("❌ DB Insert Error:", db_e)

                return jsonify({"reply": result_in})
            

            except Exception as e:
                print("❌ CSV Prediction Error:", e)
                return jsonify({"reply": "Failed to process the CSV file."})

                # — Option B: have Cohere rephrase it for you
                # prompt = f"The patient has a {prob}% chance of heart disease. Please summarize this professionally."
                # coh = co.generate(model="command", prompt=prompt, max_tokens=60)
                # phrased = coh.generations[0].text.strip()
                # return jsonify({"reply": phrased})

    # —————————————————————————————
    # 2) Fallback to Cohere for text or PDF
    # —————————————————————————————
    prompt = f"User: {user_message}\n\nPDF Content:\n{pdf_text.strip()}\n\nBot:"
    try:
        resp     = co.generate(model="command", prompt=prompt, max_tokens=500, temperature=0.7)
        bot_reply = resp.generations[0].text.strip()

        if user_id:
            try:
                conn   = db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO chats (user_id, query, response) VALUES (?, ?, ?)",
                    (user_id, user_message, bot_reply)
                )
                conn.commit()
                conn.close()
            except Exception as db_e:
                print("❌ DB Insert Error:", db_e)

        return jsonify({"reply": bot_reply})
    except Exception as e:
        print("❌ Cohere Error:", e)
        return jsonify({"reply": "Sorry, I'm having trouble responding right now."})


# -------------------- Run App --------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
