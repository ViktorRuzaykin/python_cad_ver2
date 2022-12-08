def format_decimal(number, decimal_places,):
    try:
        return "{:.{}f}".format(float(number), decimal_places)
    except ValueError:
        return number


print(format_decimal(2.0, 0))