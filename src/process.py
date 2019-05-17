from datetime import datetime

CONVERSION = {
    'K': lambda x: x,
    'C': lambda x: x - 273.15,
    'F': lambda x: x * 9 / 5 - 459.67
}


class WeatherRecord():
    def __init__(self, city: str, weather: str, temp: int, ts: int):
        self.city = city
        self.weather = weather
        self.temp = temp
        self.ts = ts

    def pretty(self, scale: str):
        dt = datetime.fromtimestamp(self.ts)
        date = dt.strftime("%a %d %b %Y %H:%M")
        target_temp = convert_kelvin(self.temp, scale)
        return f"{self.city}, {date}, {self.weather}, {target_temp}"

    @classmethod
    def from_json(cls, json_data) -> 'WeatherRecord':
        city = json_data['name']
        weather = json_data['weather'][0]['description']
        temp = json_data['main']['temp']
        ts = json_data['dt']
        return WeatherRecord(city=city, weather=weather, temp=temp, ts=ts)


def convert_kelvin(temp: float, target: str) -> str:
    """Convert Kelvin temperature to other scale

    Parameters
    ----------
    temp : float
        Kelvin temperature
    target : str, optional
        Target scale name ("C" - Celsius, "F" - Fahrenheit)

    Returns
    -------
    str
        Converted temperature with scale suffix (C/F)
    """
    t_conv = CONVERSION[target](temp)
    return str(round(t_conv)) + target


if __name__ == "__main__":
    print(convert_kelvin(362, 'C'))
    print(convert_kelvin(362, 'F'))
