import random
from string import ascii_uppercase, digits
from datetime import datetime

families = {1: 'Electronic Kits & Modules', 2: 'Test & Measurment', 3: 'Tools & Equipment',
            4: 'Components & Hardware'}

subfamilies = ('Misc Electronic Components', 'Component Packs', 'Pre-Programmed Firmware',
               'Controller Automation', 'Audio Kits', 'Sensing Device', 'Relay Board Kits',
               'Data Loggers', 'Soldering', 'Power Inverters', 'Microcontrollers', 'Electrical Hardware',
               'Security Kits')


def number():
    prefix = ''.join(random.sample(ascii_uppercase, 3))
    suffix = ''.join(random.sample(digits, 8))
    return '{0}-{1}'.format(prefix, suffix)


def name():
    nouns = ('Resistor', 'Potentiometer', 'Capacitor',
             'Inductor', 'Oscillator', 'Relay', 'Transformer', 'Battery', 'Integrated Circuit',
             'Display', 'Condenser', 'Reactor', 'Isolator', 'Control Knob', 'PWB', 'Diode',
             'Thermistor', 'CMOS', 'Timer', 'Comparator', 'Regulator', 'Amplifier', 'Cerebra', 'Cerebro',
             'Extremis', 'Inducer', 'Centrifuge', 'Nanoparticulate')

    adjectives = ('Active', 'Arc', 'DC', 'Fused', 'Passive',
                  'Electromechanical', 'Constant Current', 'MOSFET', 'Incandescent',
                  'Diode', 'MIS', 'Piezoelectrical', 'Choke', 'Solenoid', 'Selenium',
                  'Distributed', 'Voltage Regulation', 'Light Emitting', 'Variable Capacitance',
                  'Carbon Film', 'Metal Film', 'Variable', 'CDS', 'NTC', 'PTC', 'CTR', 'Electrolytic',
                  'Tantalum', 'Ceramic', 'Multilayer', 'Polystyrene', 'Polypropylene', 'Mica', 'Repulsing',
                  'Mandroid', 'Sonic', 'Orbital', 'Nano', 'Negator', 'Enervation', 'Intensifier', 'Adamantium',
                  'Vibranium')

    return '{0} {1}'.format(random.choice(adjectives), random.choice(nouns))


def description():

    descriptions = ('FLIP-FLOP, 2 CIRCUITS', 'Logic IC Case Style',
                    'PDIP', 'No. of Pins: 14', 'Case Style: PDIP', 'Single Transmitter/Receiver',
                    'RS-422/RS-485', '8-Pin PDIP Tube', 'XOR Gate', '4-Element', '2-IN Bipolar',
                    '14-Pin PDIP,XOR Gate', '4-Element 2-IN', 'Bipolar 14-Pin', 'PDIP XOR Gate',
                    'IBUS', 'JIS', 'DC Block Type', 'Electrical Coil Sensor', 'Type 76553', 'Fiber Optic Circuit',
                    'Constant Input Resistance', 'Constant Output resistance', 'TI', 'Stark Industries Model',
                    'Reed Richards Design', 'Later Design Type', 'Reference 22320f', 'Von Doom Captive Design',
                    'McCoy Style Conversion', 'Cho Model', 'Log Counter Implementatoon', 'MK VI', 'MKVII',
                    'MacTaggert Implementation', 'Pym Particle Reduction', 'Bannertech', 'Technovore',
                    'StarkVision', 'J-RICE', 'Starsky')

    return '{0} {1}'.format(random.choice(descriptions), random.choice(descriptions))


def uom():
    uoms = ('Each', 'Case', '12 Pack', 'Pallet', '24 Pack')
    return random.choice(uoms)

shipping_description = {'Priority': 40, 'One Day': 25, 'Two Day': 10, 'Standard': 5,
                        'No Rush': 0}


def future_date():
    year = random.choice(range(2017, 2018))
    month = random.choice(range(8, 13))
    day = random.choice(range(1, 30))
    schedule_date = datetime(year, month, day)
    return schedule_date
