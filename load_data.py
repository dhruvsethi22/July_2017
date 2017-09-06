from sqlalchemy.orm import sessionmaker
from faker import Faker
import random
import itertools
import time
import datetime
import mysql_connection as mysql
import tables
import data_methods


session = sessionmaker(bind=mysql.transactions)()
city_session = sessionmaker(bind=mysql.cities)()
fake_data = Faker()


# optimization stuffs
engine = mysql.transactions
import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='michaelkunc',
                             password='welcome123',
                             db='transactions',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def customers(number):
    cities = city_session.execute(
        'select city,state_code,zip,latitude,longitude,country from cities order by rand() limit {}'.format(number))
    for x in cities:
        data = tables.Customer(customer_name=fake_data.company(),
                               address=fake_data.street_address(),
                               city=x[0],
                               state=x[1],
                               postal_code=x[2],
                               latitude=x[3],
                               longitude=x[4],
                               country=x[5]
                               )
        session.add(data)
    session.commit()
    print('Customers are populated.')
    city_session.close()


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

    def header_dict(id):
        return {'header_id': id, 'order_number': data_methods.number(),
                'sold_to_id': random.choice(customers), 'currency': 'USD'}

    headers = (header_dict(i) for i in range(1, number + 1))

    engine.execute(
        tables.OrderHeader.__table__.insert(), list(headers)
    )

    session.commit()
    print('Order Headers are populated.')


def line(order_header_quantity):
    weights = range(1, 5)
    price_list_id = 3
    product_prices = tuple(itertools.chain.from_iterable([[[x.product_id, x.list_price]] * random.choice(weights) for x in session.query(tables.ProductPrice.product_id, tables.ProductPrice.list_price).filter(
        tables.ProductPrice.price_list_id == price_list_id)]))

    shipping_type_ids = tuple(x.shipping_type_id for x in session.query(
        tables.ShippingType.shipping_type_id))
    header_ids = range(1, order_header_quantity + 1)
    ship_date = tuple(((datetime.datetime.now(
    ) - datetime.timedelta(random.choice(range(1, 365))) for i in range(0, 30))))
    line_range = range(0, 5)  # range(1, 8)

    def line_values(header_id):
        product_price = random.choice(product_prices)
        line_discount = random.randrange(10, 20)
        net_price = product_price[1] - (product_price[1] / line_discount)
        shipping_type_id = random.choice(shipping_type_ids)
        date = random.choice(ship_date)
        qty = random.randrange(1, 20)
        return (header_id, shipping_type_id, date, qty, product_price[0],
                price_list_id, line_discount, net_price)

    start = time.time()

    values = (line_values(i) for i in header_ids for x in line_range)

    q = """ insert into order_lines (
            header_id,shipping_type_id,schedule_ship_date,quantity,product_id,
            price_list_id, discount, net_price
            )
            values (%s, %s, %s, %s, %s, %s, %s, %s)
        """

    with connection.cursor() as cursor:
        cursor.executemany(q, values)

    connection.commit()
    session.commit()
    end = time.time()
    print('The write operation of the function took {}'.format(end - start))
    print('{} order lines have been added to the database.'.format(
        session.query(tables.OrderLine.line_id).count()))


script_start = time.time()
tables.drop_all()
tables.add_all()
tables.add_views()

orders = 20000

customers(100)
families()
subfamilies()
products(1000)
costs()
price_list()
prices()
shipping()
header(orders)
line(orders)


session.close()

script_end = time.time()

print('The database is hydrated, yo!')
print('Run time was {} seconds'.format(script_end - script_start))
