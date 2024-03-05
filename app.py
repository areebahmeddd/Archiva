import os
import hashlib
from flask import Flask, render_template, redirect, url_for, request, session, send_from_directory, send_file

from database import create_table, execute_query, fetch_query

app = Flask(__name__)
app.secret_key = "12345"
app.config["UPLOAD_FOLDER"] = "archive"

@app.route("/")
def index():
    print("\nRoute /")

    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])

    create_table()
    return redirect(url_for("sign_in"))

@app.route("/sign_in", methods = ["GET", "POST"])
def sign_in():
    print("\nRoute /sign_in")
    error_message = None

    if request.method == "POST":
        user_data = {
            "username": request.form["username"],
            "password": hashlib.sha256(request.form["password"].encode()).hexdigest()
        }

        if fetch_query("SELECT * FROM users WHERE username = ? AND password = ?", (user_data["username"], user_data["password"])):
            session["username"] = user_data["username"]
            print(f'[Server] User "{user_data["username"]}" logged in successfully.')
            return redirect(url_for("dashboard"))
        else:
            print(f'[Server] Failed login attempt for user "{user_data["username"]}"')
            error_message = "Invalid Username or Password"

    return render_template("sign_in.html", error_message = error_message)

@app.route("/sign_up", methods = ["GET", "POST"])
def sign_up():
    print("\nRoute /sign_up")

    if request.method == "POST":
        user_data = {
            "username": request.form["username"],
            "email": request.form["email"],
            "phone": request.form["phone"],
            "password": hashlib.sha256(request.form["password"].encode()).hexdigest()
        }

        execute_query("INSERT INTO users (username, email, phone, password) VALUES (?, ?, ?, ?)",
                      (user_data["username"], user_data["email"], user_data["phone"], user_data["password"]))

        print(f'[Server] User "{user_data["username"]}" signed up successfully.')
        return redirect(url_for("sign_in"))

    return render_template("sign_up.html")

@app.route("/dashboard")
def dashboard():
    print("\nRoute /dashboard")

    if "username" in session:
        username = session["username"]
        uploaded_files = os.listdir(app.config["UPLOAD_FOLDER"])
        print(f'[Server] User "{username}" accessed the dashboard. User Files: {uploaded_files}')
        return render_template("dashboard.html", username = username, uploaded_files = uploaded_files)
    else:
        print("[Server] User not logged in. Redirecting to sign-in page.")
        return redirect(url_for("sign_in"))

@app.route("/log_out")
def log_out():
    print("\nRoute /log_out")

    if "username" in session:
        username = session.pop("username")
        print(f'[Server] User "{username}" logged out successfully.')
    else:
        print("[Server] No user was logged in.")

    return redirect(url_for("sign_in"))

@app.route("/upload_file", methods = ["POST"])
def upload_file():
    print("\nRoute /upload_file")
    file_input = request.files.getlist("fileInput")

    if any(file_input):
        for file in file_input:
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(file_path)

        print("[Server] Files uploaded successfully.")
    else:
        print("[Server] No files selected for upload.")

    return redirect(url_for("dashboard"))

@app.route("/open_file/<filename>")
def open_file(filename):
    print(f'\nRoute /open_file/{filename}')
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    if os.path.exists(file_path):
        print(f'[Server] File "{filename}" found.')
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)
    else:
        print(f'[Server] File "{filename}" not found.')

@app.route("/download_file/<filename>")
def download_file(filename):
    print(f'\nRoute /download_file/{filename}')
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    if os.path.exists(file_path):
        print(f'[Server] Initiating download for file: "{filename}"')
        return send_file(file_path, as_attachment = True)
    else:
        print(f'[Server] File "{filename}" not found.')

@app.route("/delete_file/<filename>")
def delete_file(filename):
    print(f'\nRoute /delete_file/{filename}')
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        print(f'[Server] File "{filename}" deleted successfully.')
    else:
        print(f'[Server] File "{filename}" not found.')

    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run()