from flask import Flask, request, redirect, session, render_template, send_from_directory, jsonify
from config import get_db_connection
import os

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "myedupath_secret_key"


# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('index.html')


# ---------------- FRONTEND PAGES ----------------
@app.route('/courses')
def courses():
    return render_template('courses.html')


@app.route('/colleges')
def colleges():
    return render_template('colleges.html')


@app.route('/jobs')
def jobs():
    return render_template('jobs.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route("/api/contact", methods=["POST"])
def api_contact():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    subject = data.get("subject")
    message = data.get("message")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO contacts (name, email, subject, message)
        VALUES (%s, %s, %s, %s)
    """, (name, email, subject, message))
    conn.commit()
    conn.close()

    return jsonify({"success": True})


# ---------------- USER AUTH ----------------
@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
            (name, email, password, "user")
        )
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("signup.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            session["user_role"] = user["role"]

            if user["role"] == "admin":
                return redirect("/admin-dashboard")

           return redirect("/dashboard")
       
        return "Invalid email or password"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- ADMIN ----------------
@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE name=%s AND password=%s AND role='admin'",
            (username, password)
        )
        admin = cursor.fetchone()
        conn.close()

        if admin:
            session["user_id"] = admin["id"]
            session["user_role"] = "admin"
            return redirect("/admin-dashboard")

        return "Invalid admin credentials"

    return render_template("admin-login.html")


@app.route("/admin-dashboard")
def admin_dashboard():
    if session.get("user_role") != "admin":
        return redirect("/login")

    return render_template("admin-dashboard.html")


@app.route("/admin-logout")
def admin_logout():
    session.clear()
    return redirect("/admin-login")


# ---------------- ADMIN: COURSES ----------------
@app.route("/admin/add-course")
def add_course_form():
    if session.get("user_role") != "admin":
        return redirect("/admin-login")

    return render_template("add-course.html")



@app.route("/add-course", methods=["POST"])
def add_course():
    if session.get("user_role") != "admin":
        return "Unauthorized"

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO courses (course_name, duration, eligibility, category, career_scope)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        request.form.get("course_name"),
        request.form.get("duration"),
        request.form.get("eligibility"),
        request.form.get("category"),
        request.form.get("career_scope")
    ))
    conn.commit()
    conn.close()

    return redirect("/admin-dashboard")


# ---------------- ADMIN: JOBS ----------------
@app.route("/admin/add-job")
def add_job_form():
    if session.get("user_role") != "admin":
        return "Access denied"

    return """
    <h2>Add Job</h2>
    <form method="POST" action="/add-job">
        <input name="title" placeholder="Job Title"><br><br>
        <input name="company" placeholder="Company"><br><br>
        <input name="location" placeholder="Location"><br><br>
        <input name="salary" placeholder="Salary"><br><br>
        <textarea name="description" placeholder="Description"></textarea><br><br>
        <button type="submit">Add Job</button>
    </form>
    <br>
    <a href="/admin-dashboard">⬅ Back</a>
    """


@app.route("/add-job", methods=["POST"])
def add_job():
    if session.get("user_role") != "admin":
        return "Unauthorized"

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO jobs (title, company, location, salary, description)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        request.form.get("title"),
        request.form.get("company"),
        request.form.get("location"),
        request.form.get("salary"),
        request.form.get("description")
    ))
    conn.commit()
    conn.close()

    return redirect("/admin-dashboard")


@app.route("/api/job/<int:job_id>")
def api_single_job(job_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM jobs WHERE id = %s", (job_id,))
    job = cursor.fetchone()
    conn.close()

    if job:
        return jsonify(job)
    else:
        return jsonify({"error": "Job not found"}), 404


# ---------------- PUBLIC API ----------------
@app.route("/api/courses")
def api_courses():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM courses")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)


@app.route("/api/colleges")
def api_colleges():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM colleges")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)


@app.route("/api/jobs")
def api_jobs():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM jobs")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)


@app.route("/admin/applications")
def view_applications():
    if session.get("user_role") != "admin":
        return redirect("/admin-login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT ja.*, j.title AS job_title, j.company
        FROM job_applications ja
        JOIN jobs j ON ja.job_id = j.id
        ORDER BY ja.created_at DESC
    """)
    applications = cursor.fetchall()
    conn.close()

    return render_template("admin-applications.html", applications=applications)


# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


#------------user dashboard------------

from flask import session, redirect, url_for, render_template

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html")
