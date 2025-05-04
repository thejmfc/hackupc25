from twilio.rest import Client
import requests
import time

link_shorten_url = "https://api-ssl.bitly.com/v4/shorten"
bitly_token = '6c63a6f9ac78118f84ba46923c6e73d95becdb91'
link_shorten_headers = {
    'Authorization': f'Bearer {bitly_token}',
    'Content-Type': 'application/json',
}


uk_sid = 'AC0fe18b3b5f636a3dae5d24f3e10baf9a'
uk_auth = '8335a04be85ad6717001a70673baf6fc'
uk_client = Client(uk_sid, uk_auth)
uk_from_number = "+447427859438"

def send(to_number, name, group_code, city, outbound, inbound, link):
    link_shorten_payload = { "long_url": link }

    response = requests.post(link_shorten_url, headers=link_shorten_headers, json=link_shorten_payload)
    print(link)
    print(response)
    errors = 0
    while not( response.status_code == 200 or response.status_code == 201):
        response = requests.post(link_shorten_url, headers=link_shorten_headers, json=link_shorten_payload)
        errors += 1
        print(f"retrying shorten {errors}")
        print(response.json())
        time.sleep(1)

    link = response.json().get("link")
    
    message = f"Dear {name}, your group travel for '{group_code}' has a new recommendation! Why not check out {city}? Flights: {outbound} and {inbound}. Book it: {link}"

    uk_msg = uk_client.messages.create(
        from_=uk_from_number,
        to="+"+to_number,
        body=message
    )