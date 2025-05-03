import requests
import time
from calendar import monthrange


API_KEY = "sh967490139224896692439644109194"
url = "https://partners.api.skyscanner.net/apiservices/v3/flights/live/search/create"

headers = {
    'Content-Type': 'application/json',
    'x-api-key': API_KEY
}

def run(dep_airport, dd, arr_airport, rd, locale, currency):
    dep_date = dd.split("-")
    ret_date = rd.split("-")
    
    search_payload = {
        "query": {
            "market": "ES",
            "locale": locale,
            "currency": currency,
            "query_legs": [
                {
                    "origin_place_id": {"iata": dep_airport},
                    "destination_place_id": {"iata": arr_airport},
                    "date": {"year": int(dep_date[0]), "month": int(dep_date[1]), "day": int(dep_date[2])}
                },

                {
                    "origin_place_id": {"iata": arr_airport},
                    "destination_place_id": {"iata": dep_airport},
                    "date": {"year": int(ret_date[0]), "month": int(ret_date[1]), "day": int(ret_date[2])}
                }
            ],
            "cabin_class": "CABIN_CLASS_ECONOMY",
            "adults": 1
        }
    }
    response = requests.post(url, headers=headers, json=search_payload)
    if response.status_code == 200:
        data = response.json()
        session_token = data.get('sessionToken')
        poll_url = f'https://partners.api.skyscanner.net/apiservices/v3/flights/live/search/poll/{session_token}'
        time.sleep(2)
        poll_response = requests.post(poll_url, headers=headers)
        if poll_response.status_code == 200:
            poll_data = poll_response.json()
            error = 0
            while poll_data['status'] == "RESULT_STATUS_INCOMPLETE":
                time.sleep(2)
                error += 1
                poll_response = requests.post(poll_url, headers=headers)
                poll_data = poll_response.json()
                if error >= 5:
                    response = requests.post(url, headers=headers, json=search_payload)
                    data = response.json()
                    session_token = data.get('sessionToken')
                    poll_url = f'https://partners.api.skyscanner.net/apiservices/v3/flights/live/search/poll/{session_token}'
                    poll_response = requests.post(poll_url, headers=headers)
                    poll_data = poll_response.json()
                    error = 0
                    time.sleep(2)
            best_option = poll_data['content']['sortingOptions']['cheapest'][0]['itineraryId']

            content = poll_data.get('content', {})
            itineraries = content.get('results', {}).get('itineraries', {})
            legs = content.get('results', {}).get('legs', {})
            carriers = content.get('results', {}).get('carriers', {})

            selected_legs = itineraries[best_option]["legIds"]

            choice = itineraries[best_option]["pricingOptions"][0]

            outbound_leg = legs[selected_legs[0]]
            inbound_leg = legs[selected_legs[1]]

            outbound_carriers = [] #carriers[str(outbound_leg["operatingCarrierIds"][0])]["name"]
            inbound_carriers =[] #carriers[str(inbound_leg["operatingCarrierIds"][0])]["name"]

            for carrier in outbound_leg["operatingCarrierIds"]:
                outbound_carriers.append(carriers[carrier]["name"])

            for carrier in inbound_leg["operatingCarrierIds"]:
                inbound_carriers.append(carriers[carrier]["name"])

            outbound_dep_time = str(outbound_leg["departureDateTime"]["hour"]) + str(outbound_leg["departureDateTime"]["minute"])
            outbound_arr_time = str(outbound_leg["arrivalDateTime"]["hour"]) + str(outbound_leg["departureDateTime"]["minute"])
            outbound_day_offset = outbound_leg["arrivalDateTime"]["day"] - outbound_leg["departureDateTime"]["day"]
            if outbound_day_offset < -5:
                outbound_day_offset += monthrange(outbound_leg["departureDateTime"]["year"], outbound_leg["departureDateTime"]["month"])[1]

            inbound_dep_time = str(inbound_leg["departureDateTime"]["hour"]) + str(inbound_leg["arrivalDateTime"]["minute"])
            inbound_arr_time = str(inbound_leg["arrivalDateTime"]["hour"]) + str(inbound_leg["arrivalDateTime"]["minute"])
            inbound_day_offset = inbound_leg["arrivalDateTime"]["day"] - inbound_leg["departureDateTime"]["day"]
            if inbound_day_offset < 0:
                inbound_day_offset += monthrange(inbound_leg["departureDateTime"]["year"], inbound_leg["departureDateTime"]["month"])[1]

            price = choice["price"]
            price_amount = float(price["amount"])/1000

            link = choice["items"][0]["deepLink"]

            
            json_output = {
                "outbound" : {
                    "carriers" : outbound_carriers,
                    "dep_time" : outbound_dep_time,
                    "arr_time" : outbound_arr_time,
                    "day_offset" : outbound_day_offset
                },
                "inbound" : {
                    "carriers" : inbound_carriers,
                    "dep_time" : inbound_dep_time,
                    "arr_time" : inbound_arr_time,
                    "day_offset" : inbound_day_offset
                },
                "price" : price_amount,
                "link" : link
            }
            return json_output


print(run("MAN", "2025-08-21", "JFK", "2025-08-24", "en-GB", "GBP"))