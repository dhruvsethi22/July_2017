from sqlalchemy.orm import sessionmaker
from faker import Faker
import random
import itertools
import time
import mysql_connection as mysql
import tables
import data_methods


session = sessionmaker(bind=mysql.transactions)()
fake_data = Faker()


def countries():
    countries = ['USA']
    session.bulk_save_objects(
        [tables.Country(country_name=c) for c in countries])
    print('Countries are populated.')


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
        data = (tables.StateProv(state_name=s,
                                 country=country))
        session.add(data)
    session.commit()
    print('States and Provs are populated.')


def customers(number):
    countries = [x.country_id for x in session.query(tables.Country)]
    state_prov = [x.state_prov_id for x in session.query(tables.StateProv)]
    for i in range(0, number):
        data = tables.Customer(customer_name=fake_data.company(), address=fake_data.street_address(), city=fake_data.city(),
                               state_prov_id=random.choice(state_prov), country_id=random.choice(countries),
                               postal_code=fake_data.postalcode()
                               )
        session.add(data)
    session.commit()
    print('Customers are populated.')


def families():
    for k, v in data_methods.families.items():
        data = tables.ProductFamily(family_id=k,
                                    product_family_name=v)
        session.add(data)
    session.commit()
    print('Product Families are populated.')


def subfamilies():
    for i in data_methods.subfamilies:
        data = tables.ProductSubfamily(product_subfamily_name=i, family_id=random.choice(
            list(data_methods.families.keys())))
        session.add(data)
    session.commit()
    print('Product Sub-Families are populated.')


def products(number):
    row = [(x.subfamily_id, x.family_id)
           for x in session.query(tables.ProductSubfamily)]

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
    print('Products are populated.')


def costs():
    products = (x.product_id for x in session.query(tables.Product))
    costs = []
    for x in range(0, 4):
        for i in products:
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
    print('Product Costs are populated.')


def price_list():
    data = [tables.PriceList(active=0, list_start_date='2015-01-01', list_end_date='2015-12-31'),
            tables.PriceList(active=0, list_start_date='2016-01-01',
                             list_end_date='2016-12-31'),
            tables.PriceList(active=1, list_start_date='2017-01-01', list_end_date='2017-12-31')]
    for d in data:
        session.add(d)
    session.commit()
    print('Price Lists are populated.')


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
    print('Product Prices are populated.')


def shipping():
    for k, v in data_methods.shipping_description.items():
        data = tables.ShippingType(description=k,
                                   cost=v)
        session.add(data)
    session.commit()
    print('Shipping Types are populated.')


def header(number):
    customer_weights = (1, 2, 5, 10, 15, 20, 50)
    customers = list(itertools.chain.from_iterable(
        [[x[0]] * random.choice(customer_weights) for x in session.query(tables.Customer.customer_id)]))

    headers = [tables.OrderHeader(order_number=data_methods.number(), sold_to_id=random.choice(customers),
                                  currency='USD',
                                  ) for i in range(0, number)]
    session.bulk_save_objects(headers)
    session.commit()
    print('Order Headers are populated.')


def line():
    weights = (1, 2, 3, 4, 5)
    product_prices = tuple(itertools.chain.from_iterable([[[x.product_id, x.price_list_id, x.list_price]] * random.choice(weights) for x in session.query(tables.ProductPrice).filter(
        tables.ProductPrice.price_list_id == 3)]))
    shipping_type_ids = [x.shipping_type_id for x in session.query(
        tables.ShippingType)]
    header_ids = (x.header_id for x in session.query(tables.OrderHeader))
    ship_dates = tuple(itertools.chain.from_iterable(
        [[data_methods.future_date()] * random.choice(weights) for i in range(0, 30)]))
    quantity = range(1, 20)
    discount = range(10, 20)

    def create_line(header_id):
        product_price = random.choice(product_prices)
        data = tables.OrderLine(header_id=header_id, shipping_type_id=random.choice(shipping_type_ids),
                                schedule_ship_date=random.choice(ship_dates),
                                quantity=random.choice(quantity),
                                product_id=product_price[0],
                                price_list_id=product_price[1],
                                discount=random.choice(discount),
                                )
        data.net_price = (product_price[2] -
                          (product_price[2] / data.discount))
        return data

    line_range = [5]
    # range(1, 8)
    order_lines = (create_line(i)
                   for i in header_ids for x in range(0, random.choice(line_range)))

    # order_lines = [create_line(i)
    # for i in header_ids for x in range(0, random.choice(line_range))]
    session.bulk_save_objects(order_lines)
    session.commit()

    print('{} order lines have been added to the database.'.format(
        session.query(tables.OrderLine.line_id).count()))


script_start = time.time()
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
header(1000)
line()


session.close()

script_end = time.time()

print('The database is hydrated, yo!')
print('Run time was {} seconds'.format(script_end - script_start))
