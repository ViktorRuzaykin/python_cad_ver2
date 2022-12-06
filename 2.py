
def format_decimal(number, decimal_places, types):
    if types == 'str':
        return "{:.{}f}".format(float(number), decimal_places)
    if types == 'float':
        return float("{:.{}f}".format(float(number), decimal_places))


print(type(format_decimal(231.254, 3, 'str')), format_decimal(231.250, 3, 'str'))
