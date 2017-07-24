import pymysql
import datetime
from faker import Faker
from sqlalchemy import Column,String,Integer,Float,DateTime,ForeignKey, update
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy.sql.expression import func
import time
import Order_Data
import random
import Customers
import Product_table
import fake_data


class Order_Header(Base):
    __tablename__ = 'Order_Header'
    header_id = Column(Integer, primary_key=True)
    order_number = Column(String(20))
    sold_to_id = Column(String(20))
    #ship_to_id = Column(String(20))
    po_id = Column(String(20))
    currency = Column(String(5))
    created_date = Column(DateTime)
    last_updated_date = Column(DateTime)
    #soldid = relationship(Customers.Customer(), foreign_keys=Customers.Customer.customer_id)


class Shipping_Types(Base):
    __tablename__ = 'Shipping_Types'
    shipping_type_id = Column(Integer, primary_key=True)
    description = Column(String(100))
    cost = Column(Integer)
    created_date = Column(DateTime)
    last_updated_date = Column(DateTime)

class Order_Line(Base):
    __tablename__= 'Order_Line'
    line_id = Column(Integer, primary_key=True)
    header_id =Column(Integer, ForeignKey(Order_Header.header_id))
    shipping_type_id =Column(Integer, ForeignKey(Shipping_Types.shipping_type_id))
    line_number = Column(Integer)
    schedule_ship_date = Column(DateTime)
    quantity = Column(Integer)
    product_id = Column(Integer,ForeignKey (Product_table.Products.product_id))
    price_list_id = Column(Integer)
    discount = Column(Float)
    net_price = Column(Float)
    created_date = Column(DateTime)
    last_updated_date = Column(DateTime)
    order_header= relationship(Order_Header)
    headerid = relationship(Order_Header, foreign_keys=header_id)
    shipping_types = relationship(Shipping_Types)
    shipping_typeid = relationship(Shipping_Types, foreign_keys=shipping_type_id)



from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:Timepass22#@localhost/demo')
from sqlalchemy.orm import sessionmaker
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)


def populate_shipping(number):
    fake_data = Faker()
    fake = Order_Data.Order_Class()
    s = session()
    for k,v in Order_Data.Order_Class.shipping_description.items():
        st = Shipping_Types(shipping_type_id = fake_data.ean8(), description = k,
        cost = v, created_date = datetime.datetime.utcnow(),
        last_updated_date = datetime.datetime.utcnow())
        s.add(st)
    s.commit()
    s.close()

def populate_header(num):
    fake_data = Faker()
    fake = Order_Data.Order_Class()
    s = session()
    #row_sold = s.query(Customers.Customer).all()
    for i in range(0, num):
        row_sold = s.query(Customers.Customer).order_by(func.rand()).first()
        soldid = (row_sold.customer_id)
        oh = Order_Header(order_number = fake.order_number(), sold_to_id = soldid,
        po_id = fake_data.ean8(), currency = fake_data.currency_code(), created_date = datetime.datetime.utcnow(),
        last_updated_date = datetime.datetime.utcnow())
        s.add(oh)
    s.commit()
    s.close()

def populate_line(n):
    fake_data = Faker()
    fake = Order_Data.Order_Class()
    s = session()
    #row_product = s.query(Product_table.Products).all()
    row_price_list = s.query(Product_table.PriceList).filter(Product_table.PriceList.price_list_id == 3)
    #row_pricelist = s.query(Product_table.ProductsPrices).filter(Product_table.ProductsPrices.price_list_id == 3).all()
    for i in range(0, n):
        #row_product = s.query(Product_table.Products).order_by(func.rand()).first()
        row_pricelist = s.query(Product_table.ProductsPrices).filter(Product_table.ProductsPrices.price_list_id == 3).order_by(func.rand()).first()
        #productid = (row_product.product_id)
        pricelistid = (row_price_list[0].price_list_id)
        productid = (row_pricelist.product_id)
        pricelist = (row_pricelist.list_price)
        row_header = s.query(Order_Header).order_by(func.rand()).first()
        headerid = (row_header.header_id)
        row_shipping = s.query(Shipping_Types).order_by(func.rand()).first()
        shipping_typeid = (row_shipping.shipping_type_id)
        ol = Order_Line(header_id = headerid, shipping_type_id = shipping_typeid, schedule_ship_date = fake.future_date(),
        quantity = random.randint(1,10), product_id = productid, price_list_id = pricelistid, discount = random.randint(10,20), net_price = pricelist,
        created_date = datetime.datetime.utcnow(), last_updated_date = datetime.datetime.utcnow())
        s.add(ol)
        netpricequery = s.query(Order_Line)
        netpricediscount = (netpricequery[i].discount)
        #print (netpricediscount)
        netpricequantity = (netpricequery[i].quantity)
        #print (netpricequantity)
        #print ("Done printing discount and quantity values")
        netprice = (row_pricelist.list_price)
        #print (netprice)
        netpricecalculate = ((netprice - (netprice/netpricediscount))*netpricequantity)
        #print (netpricecalculate)
        #s.execute(update(Order_Line, values={Order_Line.net_price: netpricecalculate}))
        s.query(Order_Line).filter(Order_Line.line_id == i + 1).update({Order_Line.net_price: netpricecalculate})
        #print ("successfully calculated netprice")
    s.commit()
    s.close()


# def get_netprice():
#     s = session()
#     discountquery = s.query(Order_Line)
#     discountapplied =(discountquery[i].discount)
#     print (discountapplied)
#     quantitybought = (discountquery[i].quantity)
#     print (quantitybought)
#     print(pricelist)
#     netprice = ((pricelist - (pricelist/discountapplied))*quantitybought)
#     return round(netprice,2)

populate_shipping(5)
populate_header(10000)
populate_line(10000)


        # o
        # ol = Order_Line(header_id = something(), shipping_type_id = something(), line_number = something(), quantity = something(),
        # product_id = something(), price_list_id = something(), discount = something(), net_price = something(),
        # created_date = datetime.datetime.utcnow(),
        # last_updated_date = datetime.datetime.utcnow())
        # s.add(ol)

#
