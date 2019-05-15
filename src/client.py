import requests

api_url_base = 'http://api.openweathermap.org/data/2.5/weather?q=London,uk&appid=332aff71953e43412a946ab10190bc7a'


class WeatherClient():
    def fetch(self):
        response = requests.get(api_url_base)
        if response.ok:
            return response
        else:
            return None
