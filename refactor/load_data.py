from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from faker import Faker
import datetime
import random

import mysql_connection as mysql
import tables


engine = mysql.engine
Session = sessionmaker(bind=mysql.engine)

fake_data = Faker()


def countries():
    session = Session()
    countries = ['USA']
    for c in countries:
        data = tables.Country(
            country_name=c,
            created_date=datetime.datetime.utcnow(),
            last_updated_date=datetime.datetime.utcnow())
        session.add(data)
        session.commit()
    session.close()
    print('Countries table has been populated.')


countries()


def states_provs():
    session = Session()
    country = session.query(tables.Country).order_by(func.rand()).first()
    states = (
        'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
        'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho',
        'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
        'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
        'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
        'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
        'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon',
        'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
        'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
        'West Virginia', 'Wisconsin', 'Wyoming',
    )
    for s in states:
        data = tables.State_Prov(state_name=s,
                                 country=country,
                                 created_date=datetime.datetime.utcnow(),
                                 last_updated_date=datetime.datetime.utcnow())
        session.add(data)
        session.commit()
    session.close()
    print('States and Provs table has been populated.')

states_provs()


def customers(number_of_customers):
    session = Session()
    for i in range(0, number_of_customers):
        country = session.query(tables.Country).order_by(func.rand()).first()
        state_prov = session.query(
            tables.State_Prov).order_by(func.rand()).first()
        data = tables.Customer(customer_name=fake_data.name(), address=fake_data.street_address(), city=fake_data.city(),
                               state_prov_id=state_prov.state_prov_id, country=country, ship_to=random.randint(0, 1), sold_to=random.randint(0, 1),
                               postal_code=fake_data.postalcode(), created_date=datetime.datetime.utcnow(),
                               last_updated_date=datetime.datetime.utcnow())
        session.add(data)
        session.commit()
    session.close()
    print('Customers table has been populated.')

customers(100)
