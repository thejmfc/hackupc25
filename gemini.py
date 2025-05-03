from google import genai
import json, os, urllib.request

code = input("Enter group code: \n")

data = ""
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

with urllib.request.urlopen(f"https://script.google.com/macros/s/AKfycbzxvYh-HEpUz7xPXdK3S1jZ5pZYbc5D72jRRPUm8g46n4Z7RnqGscVWpkk1UcMqd9QHkg/exec?group_code={code}") as url:
    data = json.load(url)
    # print(data)

prompt += str(data)
# print(prompt)

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

response = client.models.generate_content(
    model="gemini-2.0-flash", contents=prompt).text

clean = response.strip("```json",)
clean = clean.strip("```")

json_data = json.loads(clean)

print(json_data)

dest_airport = json_data["airport"]
outbound = json_data["outbound"]
inbound = json_data["inbound"]

for i in range(len(data)):
    print(f"{data[i]["name"]}: {data[i]["airport"]} -> {dest_airport} ({outbound}) ; {dest_airport} -> {data[i]["airport"]} ({inbound})")