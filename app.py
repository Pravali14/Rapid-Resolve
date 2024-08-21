from flask import Flask, render_template_string, request, redirect, url_for, flash
import hashlib
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for flashing messages

# HTML template as a string (frontend)
template = '''
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapid Resolve Investigation Made Easy</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            text-align: center;
            margin: 0;
            padding: 20px;
        }

        h1 {
            margin-top: 20px;
        }

        .menu {
            display: flex;
            justify-content: center;
            margin-top: 50px;
        }

        .card {
            background-color: #fff;
            padding: 20px;
            margin: 10px;
            box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
            width: 300px;
            cursor: pointer;
            text-align: left;
        }

        .card h2 {
            margin-top: 0;
        }

        .file-upload {
            display: none;
        }

        .result-container {
            margin-top: 30px;
        }

        .result-container h3 {
            margin: 10px 0;
        }

        button {
            background-color: #007bff;
            color: #fff;
            padding: 10px 20px;
            border: none;
            margin-top: 10px;
            cursor: pointer;
        }

        button:hover {
            background-color: #0056b3;
        }
    </style>
</head>

<body>
    <h1>Rapid Resolve Investigation Made Easy</h1>
    <div class="menu">
        <div class="card" onclick="document.getElementById('file-upload').click();">
            <h2>Upload & Explore Raw</h2>
            <p>Upload and explore raw images securely.</p>
            <form action="/" method="POST" enctype="multipart/form-data">
                <input type="file" id="file-upload" name="file" class="file-upload" onchange="this.form.submit();">
            </form>
        </div>
    </div>

    {% if file_uploaded %}
    <div class="result-container">
        <h3>File Uploaded Successfully!</h3>
        <p><strong>File Name:</strong> {{ file_name }}</p>
        <p><strong>Generated Hash:</strong> {{ file_hash }}</p>
    </div>
    {% endif %}

    {% if error %}
    <div class="result-container">
        <h3 style="color: red;">{{ error }}</h3>
    </div>
    {% endif %}
</body>

</html>
'''

# Directory where files will be stored (you can change this)
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Set upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def generate_file_hash(file_path):
    """Generate SHA-256 hash of the file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

@app.route("/", methods=["GET", "POST"])
def upload_file():
    file_uploaded = False
    file_name = ""
    file_hash = ""
    error = ""

    if request.method == "POST":
        if "file" not in request.files:
            error = "No file part in the form!"
            return render_template_string(template, error=error)

        file = request.files["file"]

        if file.filename == "":
            error = "No selected file!"
            return render_template_string(template, error=error)

        if file:
            try:
                # Save file
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                file.save(file_path)

                # Generate hash
                file_hash = generate_file_hash(file_path)
                file_uploaded = True
                file_name = file.filename
            except Exception as e:
                error = f"An error occurred: {str(e)}"
                return render_template_string(template, error=error)

    return render_template_string(template, file_uploaded=file_uploaded, file_name=file_name, file_hash=file_hash, error=error)

if __name__ == "__main__":
    app.run(debug=True)
