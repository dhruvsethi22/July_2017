import random
from datetime import datetime
from string import ascii_uppercase, digits

class Order_Class(object):
    shipping_description = {'Priority': 40, 'One Day': 25,'Two Day': 10, 'Standard': 5,
    'No Rush': 0}

    def order_number(self):
        prefix = ''.join(random.sample(ascii_uppercase, 2))
        suffix = ''.join(random.sample(digits, 8))
        return '{0}-{1}'.format(prefix, suffix)

    def future_date(self):
        year = random.choice(range(2017, 2018))
        month = random.choice(range(8, 13))
        day = random.choice(range(1, 30))
        schedule_date = datetime(year, month, day)
        return schedule_date
