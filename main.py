from flask import Flask, render_template
from gemini import fetch_travel_recommendations

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recommendations")
def display_recommendations():
    # Hardcoding the group code "sheff@upc"
    group_code = "sheff@upc"
    
    # Call the function from gemini.py
    recommendations = fetch_travel_recommendations(group_code)
    
    # If no recommendations are received, display an error message
    if not recommendations:
        recommendations = {"error": "No recommendations available for the provided group code."}

    # Render the recommendations in display.html
    return render_template("display.html", recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True)