import requests

# 🔐 Sandbox ключи
CLIENT_ID = "341h1GeRQSAUhe0GHoX8UVCfvJVQLCLw"
CLIENT_SECRET = "ObwqzXGvwnbea7Bd"

def get_access_token():
    auth_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    auth_data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    response = requests.post(auth_url, data=auth_data)
    if response.status_code != 200:
        print("❌ Ошибка авторизации:", response.status_code, response.text)
        return None

    print("✅ Access Token получен")
    return response.json().get("access_token")

def search_flights(origin, destination, departure_date, travel_class=None, adults=1):
    token = get_access_token()
    if not token:
        return []

    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": departure_date,
        "adults": adults,
        "currencyCode": "USD",
        "max": 10
    }

    if travel_class:
        params["travelClass"] = travel_class.upper()

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if not data.get("data") and travel_class:
            print("🔁 Повторный поиск без указания класса...")
            return search_flights(origin, destination, departure_date, travel_class=None, adults=adults)
        print(f"✅ Найдено рейсов: {len(data.get('data', []))}")
        return data.get("data", [])
    else:
        print("❌ Ошибка поиска рейсов:", response.status_code)
        print(response.text)
        return []
