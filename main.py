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

            personal_data = data.get("original_data", {})  # Extract the values
            recommendations = data.get("recommendations", {})

            if not recommendations or "outbound" not in recommendations or "inbound" not in recommendations:
                print(f"Error in recommendations: {recommendations}")
                return render_template("display.html",
                                       error="No recommendations available for the provided group code.")
            

            # Extract flight details
            flight_details = []
            for i in range(len(personal_data)):
                print(personal_data)
                # Validate input data
                if "airport" not in personal_data[i]:
                    print(f"Error: Missing 'airport' in personal_data[{i}]")
                    continue

                try:
                    flight_info = skyscanner.run(
                        personal_data[i].airport,
                        recommendations["outbound"],
                        recommendations["airport"],
                        recommendations["inbound"],
                        recommendations["locale"],
                        recommendations["home_currency"]
                    )
                    print("before flight info")
                    print(flight_info)
                    print("after flight info")
                    flight_details.append(flight_info)
                except Exception as e:
                    print(f"Error fetching flight info for personal_data[{i}]: {e}")

            # After the loop
            if not flight_details:
                flight_details.append({"error": "No flight details available at the moment."})
            print("exit success")
            return render_template("display.html", recommendations=recommendations, flight_details=flight_details, original_data=personal_data)

        except Exception as e:
            print("exit fail")
            print(e)
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
        group_code = "test"
        data = fetch_travel_recommendations(group_code)  # Get the dictionary

        personal_data = data.get("original_data", {})  # Extract the values
        recommendations = data.get("recommendations", {})

        print(f"Personal Data: {personal_data}")
        print(f"Recommendations: {recommendations}")

        # Handle missing recommendations
        if not recommendations or "outbound" not in recommendations or "inbound" not in recommendations:
            print(f"Error in recommendations: {recommendations}")
            return render_template("display.html", error="No recommendations available for the provided group code.")

        # Extract flight details
        flight_details = []
        for i in range(len(personal_data)):
            # Validate input data
            if "airport" not in personal_data[i]:
                print(f"Error: Missing 'airport' in personal_data[{i}]")
                continue
            
            try:
                flight_info = skyscanner.run(
                    personal_data[i]["airport"],
                    recommendations["outbound"],
                    recommendations["airport"],
                    recommendations["inbound"],
                    recommendations["locale"],
                    recommendations["home_currency"]
                )
                print(flight_info)
                flight_details.append(flight_info)
            except Exception as e:
                print(f"Error fetching flight info for personal_data[{i}]: {e}")

        # After the loop
        if not flight_details:
            flight_details.append({"error": "No flight details available at the moment."})

        return render_template("display.html", recommendations=recommendations, flight_details=flight_details, original_data=personal_data)

    except Exception as e:
        return render_template("display.html", error=f"An error occurred: {str(e)}")



if __name__ == "__main__":
    app.run(debug=True)