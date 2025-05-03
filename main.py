import database, json

from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect

import skyscanner
from gemini import fetch_travel_recommendations
# from skyscanner import run
import urllib.request, json

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        try:
            group_code = request.form.get("groupcode")
            data = fetch_travel_recommendations(group_code)

            personal_data = data[0]
            recommendations = data[1]
            print(f"Recs: {recommendations}")

            flight_details = []

            for i in range (len(personal_data)):
                flight_details.append(skyscanner.run(personal_data[i].airport, recommendations.outbound, recommendations.airport, recommendations.inbound, recommendations.locale, recommendations.currency))

            return render_template("display.html", recommendations=recommendations, flight_details=flight_details)

        except Exception as e:
            error_message = str(e)
            return render_template("index.html", error=error_message)
    return render_template("index.html")

@app.route("/form", methods=["GET","POST"])
def form():
    match request.method:
        case "POST":
            entry = database.FormEntry(name=request.form.get("name"),
                                       phone_number=request.form.get("phone_number"),
                                       group_code=request.form.get("group_code"),
                                       airport=request.form.get("airport"),
                                       length=int(request.form.get("length")),
                                       date=request.form.get("date"),
                                       prefs=request.form.get("prefs").split("\n"))
            entry.save()
            return redirect("/")

        case "GET":
            entries = database.FormEntry.objects.all()
            return jsonify(entries=[json.loads(e.to_json()) for e in entries])

    return jsonify(message="Invalid request method"), 405

@app.route("/recommendations")
def display_recommendations():
    try:
        group_code = "sheff@upc"
        data = fetch_travel_recommendations(group_code)  # Get the dictionary

        personal_data = data.get("original_data", {})  # Extract the values
        recommendations = data.get("recommendations", {})

        print(f"Recs display: {recommendations}")

        # Handle missing recommendations
        if not recommendations:
            return render_template("display.html", error="No recommendations available for the provided group code.")

        # Mock flight details (replace with dynamic data if needed)
        flight_details = {
            'outbound': {
                'carriers': ['Ryanair UK Ltd.', 'Airline 2'],
                'dep_time': '645',
                'arr_time': '2245',
                'day_offset': 0
            },
            'inbound': {
                'carriers': ['Icelandair'],
                'dep_time': '2340',
                'arr_time': '1140',
                'day_offset': 2
            },
            'price': 458.88
        }

        return render_template("display.html", recommendations=recommendations, flight_details=flight_details)

    except Exception as e:
        return render_template("display.html", error=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)