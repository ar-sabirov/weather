import json
from datetime import datetime


class WeatherRecord():
    def __init__(self, json_data: dict):
        self.json_data = json_data
        self.city = self.json_data['name']
        self.weather = self.json_data['weather'][0]['description']
        self.temp = temp = self.json_data['main']['temp']
        self.ts = self.json_data['dt']

    def pretty(self, scale: str):
        dt = datetime.fromtimestamp(self.ts)
        date = dt.strftime("%a %d %b %Y %H:%M")
        target_temp = convert_kelvin(self.temp, scale)
        return f"{self.city}, {date}, {self.weather}, {target_temp}"


def convert_kelvin(temp: float, target: str = 'C') -> str:
    """Convert Kelvin temperature to other scale
    
    Parameters
    ----------
    temp : float
        Kelvin temperature
    target : str, optional
        Target scale name ("cl" - Celsius, "fh" - Fahrenheit),
        by default 'cl'
    
    Returns
    -------
    str
        Converted temperature with scale suffix (C/F)
    """
    conversion = {'C': lambda x: x - 273.15, 'F': lambda x: x * 9 / 5 - 459.67}
    t_conv = conversion[target](temp)
    return str(round(t_conv)) + target


if __name__ == "__main__":
    print(convert_kelvin(362, 'C'))
    print(convert_kelvin(362, 'F'))