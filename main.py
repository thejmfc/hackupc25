import database, json

from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect

import skyscanner
from gemini import fetch_travel_recommendations

import texts as twilio
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
                    print(flight_info)

                    flight_info["name"] = personal_data[i]["name"]
                    flight_info["phone_number"] = personal_data[i]["phone_number"]
                    flight_info["home_airport"] = personal_data[i]["airport"]
                    flight_info["dest_airport"] = recommendations["airport"]
                    flight_details.append(flight_info)

                    # print(flight_info["phone_number"])
                    # print(flight_info["name"])
                    # print(group_code)
                    # print(recommendations["airport"])
                    # print(f"{flight_info["outbound"]["carriers"]} at {flight_info["outbound"]["dep_time"]}")
                    # print(f"{flight_info["inbound"]["carriers"]} at {flight_info["inbound"]["dep_time"]}")
                    # print(flight_info["link"])

                    twilio.send(flight_info["phone_number"], flight_info["name"], group_code,
                                 recommendations["airport"], f"{flight_info["outbound"]["carriers"]} on {recommendations["outbound"]} at {flight_info["outbound"]["dep_time"]}",
                                 f"{flight_info["inbound"]["carriers"]} on {recommendations["inbound"]} at {flight_info["inbound"]["dep_time"]}", flight_info["link"])

                except Exception as e:
                    print(f"Error fetching flight info for personal_data[{i}]: {e}")

            # After the loop
            if not flight_details:
                flight_details.append({"error": "No flight details available at the moment."})
            print("exit success")
            return render_template("display.html", recommendations=recommendations, flight_details=flight_details)

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
        names = []
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
                flight_info["name"] = personal_data[i]["name"]
                flight_info["phone_number"] = personal_data[i]["phone_number"]
                flight_info["home_airport"] = personal_data[i]["airport"]
                print(flight_info)
                flight_details.append(flight_info)
                twilio.send(flight_info["phone_number"], flight_info["name"], group_code,
                                 recommendations["airport"], f"{flight_info["outbound"]["carriers"]} on {recommendations["outbound"]} at {flight_info["outbound"]["dep_time"]}",
                                 f"{flight_info["inbound"]["carriers"]} on {recommendations["inbound"]} at {flight_info["inbound"]["dep_time"]}", flight_info["link"])

                
                # name, phone number, flight choices
            except Exception as e:
                print(f"Error fetching flight info for personal_data[{i}]: {e}")

        # After the loop
        if not flight_details:
            flight_details.append({"error": "No flight details available at the moment."})

        return render_template("display.html", recommendations=recommendations, flight_details=flight_details)

    except Exception as e:
        return render_template("display.html", error=f"An error occurred: {str(e)}")



if __name__ == "__main__":
    app.run(debug=True)