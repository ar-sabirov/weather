"""Utility module for dealing with weather unit
conversions
"""
CONVERSION = {
    'K': lambda x: x,
    'C': lambda x: x - 273.15,
    'F': lambda x: x * 9 / 5 - 459.67
}


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
