import json
import os
import urllib.request

from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Input prompt for group code
code = input("Enter group code: \n")
data = ""

# Preparing prompt
prompt = """
Hello gemini, please can you suggest the Best Destination for friends around the world. Below you will find a list of names, home airports, interests/preferences, starting date and lengths, in the following format:
[
{
"Timestamp": "2025-05-02T23:16:45.000Z",
"group_code": "Group ID",
"name": "Friend's name",
"phone_number": "Phone number",
"airport": "Airport code",
"prefs": "List of user's interests and preferences",
"date": "Date, format YYYY-MM-DDTHH:MM:SS.MSZ",
"length": "Number of days"
}
]

Please ignore the phone_number and Timestamp fields.

You will also need to pick the best date to travel outbound and inbound based on the group (ideally the midpoint or average), and average out the length to pick the ideal number of days. Also some supplementary data as in the format that follows

Your result must be in the following format, with nothing before or after it; just the json:
{
"city": <resulting city>,
"airport": <airport code>,
"outbound": <outbound date>,
"inbound": <inbound date>,
"length": <number of days>,
"itinerary": [
<String detailing each day as separate element>
],
"temperature": <average temperature in celcius at time of trip in destination>,
"home_currency": <best currency code based on the home airports>,sh
"locale": <best locale based on the home airports provided. the language this prompt is in is irrelevant> 
}

Here is the list of data:

"""

# Fetching the data
try:
    with urllib.request.urlopen(f"https://script.google.com/macros/s/AKfycbzxvYh-HEpUz7xPXdK3S1jZ5pZYbc5D72jRRPUm8g46n4Z7RnqGscVWpkk1UcMqd9QHkg/exec?group_code={code}") as url:
        data = json.load(url)
except Exception as e:
    print("Error fetching data:", str(e))
    exit(1)

prompt += str(data)

# Dummy result generation (use a simpler API or logic instead of google.genai)
# For example, this dummy code generates static output
response = {
    "city": "Barcelona",
    "airport": "BCN",
    "outbound": "2025-06-01",
    "inbound": "2025-06-15",
    "length": 14,
    "itinerary": ["Day 1: Arrival", "Day 2: Explore the city"],
    "temperature": 25,
    "home_currency": "EUR",
    "locale": "es"
}

# Prepare and display the result
json_data = response
print(json_data)

# Generate itineraries for each participant
dest_airport = json_data["airport"]
outbound = json_data["outbound"]
inbound = json_data["inbound"]

for i in range(len(data)):
    print(f"{data[i]['name']}: {data[i]['airport']} -> {dest_airport} ({outbound}) ; {dest_airport} -> {data[i]['airport']} ({inbound})")