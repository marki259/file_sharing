from flask import Flask, send_from_directory, render_template_string
from flask_httpauth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import logging

load_dotenv()

USERNAME = os.getenv("APP_USERNAME")
PASSWORD = os.getenv("APP_PASSWORD")

app = Flask(__name__)
auth = HTTPBasicAuth()

USERS = {USERNAME: PASSWORD}


@auth.verify_password
def verify_password(username, password):

    if USERS.get(username) == password:
        logging.log(logging.INFO, f"User {username} authenticated")
        return True
    logging.log(logging.INFO, f"User {username} not authenticated")
    print(f"User {username} not authenticated")
    return False


# Mapping of accessible folders. The keys are folder names, and the values are the folder paths.
FOLDERS = {
    "Articles": "data/articles",
    "Books": "data/books",
}


@app.route("/")
@auth.login_required
def index():
    folder_list = "<ul>"
    for folder in FOLDERS.keys():
        folder_list += f'<li><a href="/folder/{folder}">{folder}</a></li>'
    folder_list += "</ul>"
    return render_template_string("<h1>Folders</h1>" + folder_list)


@app.route("/folder/<folder_name>")
@auth.login_required
def list_files(folder_name):
    folder_path = FOLDERS.get(folder_name)
    if not folder_path or not os.path.exists(folder_path):
        return "Folder not found.", 404
    files = os.listdir(folder_path)
    files_list = "<ul>"
    for file in files:
        files_list += f'<li><a href="/files/{folder_name}/{file}">{file}</a></li>'
    files_list += "</ul>"
    return render_template_string(f"<h1>Files in {folder_name}</h1>" + files_list)


@app.route("/files/<folder_name>/<filename>")
@auth.login_required
def file(folder_name, filename):
    folder_path = FOLDERS.get(folder_name)
    if not folder_path:
        return "Folder not found.", 404
    return send_from_directory(folder_path, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
