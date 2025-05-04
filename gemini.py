from google import genai
import urllib.request, json
import database

def fetch_travel_recommendations(code):
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

    entries = []

    for entry in database.FormEntry.objects:
        if entry.group_code == code:
            entries.append(entry)
            prompt += entry.to_json()
            prompt += "\n"

    client = genai.Client(api_key="AIzaSyBxsgfGzrQuCVOlLPaANHIN2dVfuMm5Hyk")

    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt).text

    clean = response.strip("```json",)
    clean = clean.strip("```")

    json_data = json.loads(clean)

    # dest_airport = json_data["airport"]
    # outbound = json_data["outbound"]
    # inbound = json_data["inbound"]

    return {
        "original_data": entries,
        "recommendations": json_data
    }