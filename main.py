import database, json

from datetime import datetime
from flask import Flask, render_template, request, jsonify
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
            entry = database.FormEntry.from_json(json.dumps(request.json))
            entry.save()
            return jsonify(json.loads(entry.to_json()))
        case "GET":
            entries = database.FormEntry.objects.all()
            return jsonify(entries=[json.loads(e.to_json()) for e in entries])

    return jsonify(message="Invalid request method"), 405

@app.route("/recommendations")
def display_recommendations():
    group_code = "sheff@upc"
    recommendations = fetch_travel_recommendations(group_code)
    
    # If no recommendations are received, display an error message
    if not recommendations:
        recommendations = {"error": "No recommendations available for the provided group code."}

    # Render the recommendations in display.html

    flight_details = {'outbound':
                          {'carriers': ['Ryanair UK Ltd.', 'Airline 2'], 'dep_time': '645', 'arr_time': '2245', 'day_offset': 0},
                      'inbound':
                          {'carriers': ['Icelandair'], 'dep_time': '2340', 'arr_time': '1140', 'day_offset': 2},
                      'price': 458.88}

    return render_template("display.html", recommendations=recommendations, flight_details=flight_details)

if __name__ == "__main__":
    app.run(debug=True)