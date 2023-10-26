from flask import Flask, request, render_template, jsonify, send_file
import pandas as pd
from io import BytesIO
from pymongo import MongoClient

app = Flask(__name__)

# ---------------------------------------------------------------------------

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["Hostel"]
collection = db["TE"]

# ----------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")

# ------------------------------------------------------------------------

@app.route("/add_fine", methods=["POST"])
def add_fine():
    room = int(request.form["room"])
    fine_to_add = float(request.form["fine_to_add"])
    
    collection.update_one({"room": room}, {"$inc": {"fine": fine_to_add}})
    
    return jsonify({"message": "Fine added successfully."})

# ------------------------------------------------------------------------------------------

@app.route("/remove_fine", methods=["POST"])
def remove_fine():
    room = int(request.form["room"])
    fine_to_remove = float(request.form["fine_to_remove"])
    
    collection.update_one({"room": room}, {"$inc": {"fine": -fine_to_remove}})
    
    return jsonify({"message": "Fine removed successfully."})

# -------------------------------------------------------------------------------------------

@app.route("/insert_student", methods=["GET", "POST"])
def insert_student():
    if request.method == "POST":
        name = request.form["name"]
        room = int(request.form["room"])
        
        # Default fine is set to zero
        fine = 0

        # Insert the student data into MongoDB
        record = {
            "name": name,
            "room": room,
            "fine": fine
        }
        collection.insert_one(record)

        return jsonify({"message": "Student data added successfully."})

    return render_template("insert_student.html")

# ------------------------------------------------------------------------------

@app.route("/export_excel")
def export_excel():
    cursor = collection.find()
    student_data = list(cursor)
    df = pd.DataFrame(student_data)
    
    excel_file = BytesIO()
    with pd.ExcelWriter(excel_file, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="StudentData", index=False)

    excel_file.seek(0)
    return send_file(excel_file, attachment_filename="student_data.xlsx", as_attachment=True)

# --------------------------------------------------------------------------------------

@app.route("/export_fine_defaulters")
def export_fine_defaulters():
    # Retrieve data from MongoDB for students with fines > 0
    cursor = collection.find({"fine": {"$gt": 0}})
    student_data = list(cursor)
    df = pd.DataFrame(student_data)

    # Create an Excel file
    excel_file = BytesIO()
    with pd.ExcelWriter(excel_file, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="FineDefaulters", index=False)

    # Return the Excel file as a downloadable response
    excel_file.seek(0)
    return send_file(excel_file, attachment_filename="fine_defaulters.xlsx", as_attachment=True)



if __name__ == "__main__":
    app.run(debug=True)
