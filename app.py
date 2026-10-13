from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "event-management-secret-key"

def init_db():
    conn = sqlite3.connect("event_management.db")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            course TEXT NOT NULL,
            event TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            session["admin_logged_in"] = True
            return redirect(url_for("admin"))

        return "Invalid username or password"

    return render_template("admin-login.html")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/event-details/<event_name>")
def event_details(event_name):

    if event_name == "ai":
        title = "AI & Machine Learning Workshop"
        description = "Learn the fundamentals of Artificial Intelligence and Machine Learning."
        image = "img1.jpg"

    elif event_name == "web":
        title = "Web Development Bootcamp"
        description = "Learn modern web development technologies."
        image = "img2.jpg"

    elif event_name == "python":
        title = "Python Programming Workshop"
        description = "Master the fundamentals of Python programming."
        image = "img3.jpg"

    else:
        return "Event not found", 404

    return render_template(
        "event-details.html",
        title=title,
        description=description,
        image=image,
        event_name=event_name
    )


@app.route("/register/<event_name>" , methods=["GET", "POST"])
def register(event_name):

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        course = request.form["course"]

        conn = sqlite3.connect("event_management.db")

        conn.execute("""
            INSERT INTO registrations (name, phone, course, event)
            VALUES (?, ?, ?, ?)
        """, (name, phone, course, event_name))

        conn.commit()
        conn.close()

        return "Registration Successful!"
    
    return render_template(
        "register.html",
        event_name=event_name
    )


@app.route("/ai-recommend", methods=["GET" , "POST"])
def ai_recommend():

    recommendation = ""
    recommended_event = ""

    if request.method == "POST":

        interest = request.form["interest"].lower()

        if ("python" in interest or
            "programming" in interest or
            "coding" in interest or
            "data science" in interest):
    
            recommendation = "Python Programming Workshop"
            recommended_event = "python"

        elif ("ai" in interest or
            "machine learning" in interest or
            "deep learning" in interest or
            "artificial intelligence" in interest):
    
            recommendation = "AI & Machine Learning Workshop"
            recommended_event = "ai"

        elif ("web" in interest or
            "website" in interest or
            "web development" in interest or
            "html" in interest or
            "css" in interest):
    
            recommendation = "Web Development Bootcamp"
            recommended_event = "web"

        else:
        
            recommendation = "We recommend exploring all our upcoming events."
            recommended_event = ""

    return render_template(
        "ai-recommend.html",
        recommendation=recommendation,
        recommended_event=recommended_event
    )

@app.route("/student-login", methods=["GET", "POST"])
def student_login():

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]

        conn = sqlite3.connect("event_management.db")

        student = conn.execute(
            "SELECT * FROM registrations WHERE name = ? AND phone = ?",
            (name, phone)
        ).fetchone()

        conn.close()

        if student:
            session["student_logged_in"] = True
            session["student_name"] = name
            return redirect(url_for("home"))

        return "Student not found. Please register first."

    return render_template("student-login.html")


@app.route("/admin")
def admin():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    conn = sqlite3.connect("event_management.db")

    search = request.args.get("search", "")

    if search:
        registrations = conn.execute(
            """
            SELECT * FROM registrations
            WHERE name LIKE ?
            OR course LIKE ?
            OR event LIKE ?
            """,
            (
                "%" + search + "%",
                "%" + search + "%",
                "%" + search + "%"
            )
        ).fetchall()
    else:
        registrations = conn.execute(
            "SELECT * FROM registrations"
        ).fetchall()

        print("REGISTRATIONS:", registrations)

    registrations = [
        (
            r[0],
            r[1],
            r[2],
            r[3],
            "AI & Machine Learning Workshop" if r[4] == "ai"
            else "Web Development Bootcamp" if r[4] == "web"
            else "Python Programming Workshop" if r[4] == "python"
            else r[4]
        )
        for r in registrations
    ]

    conn.close()

    return render_template(
        "admin.html",
        registrations=registrations
    )
@app.route("/delete-registration/<int:registration_id>")
def delete_registration(registration_id):

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    conn = sqlite3.connect("event_management.db")

    conn.execute(
        "DELETE FROM registrations WHERE id = ?",
        (registration_id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("admin"))


@app.route("/logout")
def logout():

    session.pop("admin_logged_in", None)

    return redirect(url_for("admin_login"))

@app.route("/student-logout")
def student_logout():

    session.pop("student_logged_in", None)
    session.pop("student_name", None)

    return redirect(url_for("home"))




if __name__ == "__main__":
    init_db()
    app.run(debug=True)
