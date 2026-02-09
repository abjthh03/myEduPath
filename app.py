from flask import Flask, request, redirect, session,  render_template, send_from_directory, jsonify
from config import get_db_connection

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "myedupath_secret_key"


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


@app.route("/admin-login")
def admin_login_page():
    return render_template("admin-login.html")


@app.route("/admin-login", methods=["POST"])
def admin_login():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM admin WHERE username=%s AND password=%s",
        (request.form.get("username"), request.form.get("password"))
    )
    admin = cursor.fetchone()
    conn.close()

    if admin:
        session["admin_logged_in"] = True
        return redirect("/admin-dashboard")

    return "Invalid admin credentials"


@app.route("/admin-dashboard")
def admin_dashboard():
    if not session.get("admin_logged_in"):
        return redirect("/admin-login")
    return send_from_directory(app.static_folder, "admin-dashboard.html")


@app.route("/admin-logout")
def admin_logout():
    session.clear()
    return redirect("/admin-login")


# ---------------- COURSES (ADMIN) ----------------
@app.route("/add-course-form")
def add_course_form():
    if not session.get("admin_logged_in"):
        return "Access denied"
    return send_from_directory(app.static_folder, "add-course.html")


@app.route("/add-course", methods=["POST"])
def add_course():
    if not session.get("admin_logged_in"):
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


@app.route("/view-courses")
def view_courses():
    if not session.get("admin_logged_in"):
        return "Access denied"

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM courses")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)


# ---------------- JOBS (ADMIN) ----------------
@app.route("/add-job-form")
def add_job_form():
    if not session.get("admin_logged_in"):
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
    if not session.get("admin_logged_in"):
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


@app.route("/view-applications")
def view_applications():
    if not session.get("admin_logged_in"):
        return "Access denied"

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT job_applications.*, jobs.title
        FROM job_applications
        JOIN jobs ON job_applications.job_id = jobs.id
    """)
    apps = cursor.fetchall()
    conn.close()

    html = "<h2>Job Applications</h2><ul>"
    for a in apps:
        html += f"""
        <li>
            <b>{a['name']}</b> applied for <b>{a['title']}</b><br>
            Email: {a['email']} | Phone: {a['phone']}<br>
            Resume: <a href="{a['resume_link']}" target="_blank">View</a>
        </li><hr>
        """
    html += "</ul><a href='/admin-dashboard'>Back</a>"
    return html


# ---------------- PUBLIC API ----------------
@app.route("/api/courses")
def api_courses():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM courses")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

@app.route("/api/course/<int:id>")
def api_course(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM courses WHERE id=%s", (id,))
    data = cursor.fetchone()
    conn.close()
    return jsonify(data or {})

@app.route("/api/colleges")
def api_colleges():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM colleges")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

@app.route("/api/college/<int:id>")
def api_college(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM colleges WHERE id=%s", (id,))
    data = cursor.fetchone()
    conn.close()
    return jsonify(data or {})

@app.route("/api/jobs")
def api_jobs():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM jobs")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

@app.route("/api/job/<int:id>")
def api_job(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM jobs WHERE id=%s", (id,))
    data = cursor.fetchone()
    conn.close()
    return jsonify(data or {})


# ---------------- USER AUTH ----------------
@app.route('/signup')
def signup_page():
    return render_template('signup.html')


@app.route('/login')
def login():
    return render_template('login.html')



@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")



@app.route('/contact')
def contact():
    return render_template('contact.html')



# ---------------- RUN ----------------
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
