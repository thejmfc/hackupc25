from flask import Flask, render_template, request, jsonify

import database
from gemini import fetch_travel_recommendations

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        try:
            group_code = request.form.get("groupcode")
            recommendations = fetch_travel_recommendations(group_code)
            return render_template("display.html", recommendations=recommendations)
        except Exception as e:
            error_message = str(e)
            return render_template("index.html", error=error_message)
    return render_template("index.html")

@app.route("/form", methods=["GET","POST"])
def form():
    match request.method:
        case "POST":
            entry = database.FormEntry.from_json(request.json)
            return jsonify(entry.to_json())
        case "GET":
            entries = database.FormEntry.objects.all()
            return jsonify(entries=[e.to_json() for e in entries])

    return jsonify(message="Invalid request method"), 405

@app.route("/recommendations")
def display_recommendations():
    group_code = "sheff@upc"
    recommendations = fetch_travel_recommendations(group_code)
    
    # If no recommendations are received, display an error message
    if not recommendations:
        recommendations = {"error": "No recommendations available for the provided group code."}

    # Render the recommendations in display.html
    return render_template("display.html", recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True)