from sqlalchemy.orm import sessionmaker
from faker import Faker
import datetime
import random
import time

import mysql_connection as mysql
import tables
import data_methods


engine = mysql.engine
Session = sessionmaker(bind=mysql.engine)
session = Session()

fake_data = Faker()


def countries():
    countries = ['USA']
    for c in countries:
        data = tables.Country(
            country_name=c,
            created_date=datetime.datetime.utcnow(),
            last_updated_date=datetime.datetime.utcnow())
        session.add(data)
    session.commit()
    print('Countries table has been populated.')


def states_provs():
    country = session.query(tables.Country).first()
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
    print('States and Provs table has been populated.')


def customers(number):
    countries = [x.country_id for x in session.query(tables.Country)]
    state_prov = [x.state_prov_id for x in session.query(tables.State_Prov)]
    for i in range(0, number):
        data = tables.Customer(customer_name=fake_data.name(), address=fake_data.street_address(), city=fake_data.city(),
                               state_prov_id=random.choice(state_prov), country_id=random.choice(countries), ship_to=random.randint(0, 1), sold_to=random.randint(0, 1),
                               postal_code=fake_data.postalcode(), created_date=datetime.datetime.utcnow(),
                               last_updated_date=datetime.datetime.utcnow())
        session.add(data)
    session.commit()
    print('Customers table has been populated.')


def families():
    for k, v in data_methods.families.items():
        data = tables.Product_Family(family_id=k,
                                     product_family_name=v)
        session.add(data)
    session.commit()
    print('Product Family table has been populated.')


def subfamilies():
    for i in data_methods.subfamilies:
        data = tables.Product_Subfamily(product_subfamily_name=i, family_id=random.choice(
            list(data_methods.families.keys())))
        session.add(data)
    session.commit()
    print('Product sub-family table has been populated.')


def products(number):
    row = [(x.subfamily_id, x.family_id)
           for x in session.query(tables.Product_Subfamily)]

    def create_product(row):
        ids = random.choice(row)
        return tables.Product(product_number=data_methods.number(),
                              product_name=data_methods.name(),
                              description=data_methods.description(),
                              uom=data_methods.uom(),
                              subfamily_id=ids[0],
                              family_id=ids[1])

    products = [create_product(row) for i in range(0, number)]
    session.bulk_save_objects(products)
    session.commit()


def costs():
    products = (x.product_id for x in session.query(tables.Product))
    costs = []
    for i in products:
        for i in range(0, 4):
            data = tables.ProductCost(product_id=i,
                                      mtl_cost=round(
                                          random.uniform(.1, 10), 2),
                                      labor_cost=round(
                                          random.uniform(.1, 10), 2),
                                      burden_cost=round(
                                          random.uniform(.1, 10), 2)
                                      )
            costs.append(data)
    session.bulk_save_objects(costs)
    session.commit()
    print('product_costs table has been populated.')


def price_list():
    data = [tables.PriceList(active=0, list_start_date='2015-01-01', list_end_date='2015-12-31'),
            tables.PriceList(active=0, list_start_date='2016-01-01',
                             list_end_date='2016-12-31'),
            tables.PriceList(active=1, list_start_date='2017-01-01', list_end_date='2017-12-31')]
    for d in data:
        session.add(d)
    session.commit()
    print('price_lists has been populated.')


def prices():
    products = [x.product_id for x in session.query(tables.Product)]
    price_lists = [x.price_list_id for x in session.query(tables.PriceList)]
    prices = []
    for i in products:
        for x in price_lists:
            data = tables.ProductPrice(price_list_id=x,
                                       product_id=i,
                                       list_price=round(
                                           random.uniform(1, 100), 2)
                                       )

            prices.append(data)
    session.bulk_save_objects(prices)
    session.commit()
    print('products_prices has been populated.')


def shipping():
    for k, v in data_methods.shipping_description.items():
        data = tables.Shipping_Type(shipping_type_id=fake_data.ean8(), description=k,
                                    cost=v, created_date=datetime.datetime.utcnow(),
                                    last_updated_date=datetime.datetime.utcnow())
        session.add(data)
    session.commit()
    print('Shipping Types has been populated.')


def header(number):
    customers = [x.customer_id for x in session.query(tables.Customer)]
    now = datetime.datetime.utcnow()
    headers = [tables.Order_Header(order_number=data_methods.number(), sold_to_id=random.choice(customers),
                                   po_id=fake_data.ean8(), currency=fake_data.currency_code(),
                                   created_date=now,
                                   last_updated_date=now) for i in range(0, number)]
    session.bulk_save_objects(headers)
    session.commit()
    print('Order Headers has been populated')


def line():
    product_prices = [[x.product_id, x.price_list_id, x.list_price] for x in session.query(tables.ProductPrice).filter(
        tables.ProductPrice.price_list_id == 3)]
    shipping_type_ids = [x.shipping_type_id for x in session.query(
        tables.Shipping_Type)]
    header_ids = (x.header_id for x in session.query(tables.Order_Header))
    now = datetime.datetime.utcnow()

    def create_line(header_id, product_price):
        product_price = random.choice(product_prices)
        data = tables.Order_Line(header_id=header_id, shipping_type_id=random.choice(shipping_type_ids),
                                 schedule_ship_date=data_methods.future_date(), quantity=random.randint(1, 10),
                                 product_id=product_price[0],
                                 price_list_id=product_price[1],
                                 discount=random.randint(10, 20),
                                 created_date=now, last_updated_date=now)
        data.net_price = (product_price[2] -
                          (product_price[2] / data.discount))
        return data

    order_lines = [create_line(i, product_prices)
                   for i in header_ids for x in range(0, 5)]
    session.bulk_save_objects(order_lines)
    session.commit()
    print('Order lines has been populated')

script_start = datetime.datetime.now()

tables.drop_all()
tables.add_all()
tables.add_views()

countries()
states_provs()
customers(100)
families()
subfamilies()
products(1000)
costs()
price_list()
prices()
shipping()
header(100000)
line()

session.close()

script_end = datetime.datetime.now()

diff = script_end - script_start
run_time = (divmod(diff.days * 86400 + diff.seconds, 60))
print('Run time was {0} minutes {1} seconds'.format(run_time[0], run_time[1]))
