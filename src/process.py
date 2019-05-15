import json
from datetime import datetime


def parse_weather(report: dict, temp_scale):
    dt = datetime.fromtimestamp(report['dt'])
    city = report['name']
    weather = report['weather'][0]['description']
    temp = report['main']['temp']
    target_temp = convert_kelvin(temp, temp_scale)
    date = dt.strftime("%a %d %b %Y %H:%M")
    return f"{city}, {date}, {weather}, {target_temp}"


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