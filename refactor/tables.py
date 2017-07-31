from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, Boolean, Date, DateTime, MetaData, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import mysql_connection as mysql

Base = declarative_base()
metadata = MetaData()
Session = sessionmaker(bind=mysql.engine)
session = Session()


class Country(Base):
    __tablename__ = 'countries'
    country_id = Column(Integer, primary_key=True)
    country_name = Column(String(500))
    created_date = Column(DateTime)
    last_updated_date = Column(DateTime)
    states_provs = relationship(
        "State_Prov", backref="country", lazy='dynamic')
    customer = relationship("Customer", backref="country", lazy="dynamic")


class State_Prov(Base):
    __tablename__ = 'states_provs'
    state_prov_id = Column(Integer, primary_key=True)
    state_name = Column(String(500))
    country_id = Column(Integer, ForeignKey(Country.country_id))
    created_date = Column(DateTime)
    last_updated_date = Column(DateTime)
    customer = relationship("Customer", backref="states_provs", lazy="dynamic")


class Customer(Base):
    __tablename__ = 'customers'
    customer_id = Column(Integer, primary_key=True)
    customer_name = Column(String(500))
    address = Column(String(100))
    city = Column(String(100))
    state_prov_id = Column(Integer, ForeignKey(State_Prov.state_prov_id))
    country_id = Column(Integer, ForeignKey(Country.country_id))
    postal_code = Column(String(20))
    ship_to = Column(Integer)
    sold_to = Column(Integer)
    created_date = Column(DateTime)
    last_updated_date = Column(DateTime)


class Product_Family(Base):
    __tablename__ = 'product_family'
    family_id = Column(Integer, primary_key=True)
    product_family_name = Column(String(5000))


class Product_Subfamily(Base):
    __tablename__ = 'product_subfamily'
    subfamily_id = Column(Integer, primary_key=True)
    product_subfamily_name = Column(String(500))
    family_id = Column(Integer, ForeignKey(Product_Family.family_id))
    family = relationship(Product_Family)


class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    product_number = Column(String(100))
    product_name = Column(String(500))
    description = Column(String(2000))
    uom = Column(String(20))
    manufacturer_id = Column(Integer)
    family_id = Column(Integer, ForeignKey(Product_Subfamily.family_id))
    subfamily_id = Column(Integer, ForeignKey(Product_Subfamily.subfamily_id))
    subfamily = relationship(Product_Subfamily, foreign_keys=[subfamily_id])
    family = relationship(Product_Subfamily, foreign_keys=family_id)


class ProductCost(Base):
    __tablename__ = 'product_costs'
    cost_id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    mtl_cost = Column(Numeric(precision=4, scale=2))
    labor_cost = Column(Numeric(precision=4, scale=2))
    burden_cost = Column(Numeric(precision=4, scale=2))


class PriceList(Base):
    __tablename__ = 'price_lists'
    price_list_id = Column(Integer, primary_key=True)
    active = Column(Boolean)
    list_start_date = Column(Date)
    list_end_date = Column(Date)


class ProductPrice(Base):
    __tablename__ = 'products_prices'
    price_id = Column(Integer, primary_key=True)
    price_list_id = Column(Integer, ForeignKey(PriceList.price_list_id))
    product_id = Column(Integer, ForeignKey(Product.product_id))
    list_price = Column(Numeric(precision=4, scale=2))


class Shipping_Type(Base):
    __tablename__ = 'shipping_types'
    shipping_type_id = Column(Integer, primary_key=True)
    description = Column(String(100))
    cost = Column(Integer)
    created_date = Column(DateTime)
    last_updated_date = Column(DateTime)


class Order_Header(Base):
    __tablename__ = 'order_headers'
    header_id = Column(Integer, primary_key=True)
    order_number = Column(String(20))
    sold_to_id = Column(String(20))
    #ship_to_id = Column(String(20))
    po_id = Column(String(20))
    currency = Column(String(5))
    created_date = Column(DateTime)
    last_updated_date = Column(DateTime)
    #soldid = relationship(Customers.Customer(), foreign_keys=Customers.Customer.customer_id)


class Order_Line(Base):
    __tablename__ = 'order_lines'
    line_id = Column(Integer, primary_key=True)
    header_id = Column(Integer, ForeignKey(Order_Header.header_id))
    shipping_type_id = Column(Integer, ForeignKey(
        Shipping_Type.shipping_type_id))
    line_number = Column(Integer)
    schedule_ship_date = Column(DateTime)
    quantity = Column(Integer)
    product_id = Column(Integer, ForeignKey(Product.product_id))
    price_list_id = Column(Integer)
    discount = Column(Float)
    net_price = Column(Float)
    created_date = Column(DateTime)
    last_updated_date = Column(DateTime)
    order_header = relationship(Order_Header)
    headerid = relationship(Order_Header, foreign_keys=header_id)
    shipping_types = relationship(Shipping_Type)
    shipping_typeid = relationship(
        Shipping_Type, foreign_keys=shipping_type_id)


# Drop and create tables
def drop_all():
    Base.metadata.drop_all(mysql.engine)
    print('All tables have been dropped.')


def add_all():
    Base.metadata.create_all(mysql.engine)
    print('All tables have been created.')

# Define views
view_defs = ("""create or replace view current_product_prices as
				select pp.product_id, pp.list_price, pl.price_list_id
				from products_prices pp
				inner join price_lists pl
				on pp.price_list_id = pl.price_list_id
				where pl.price_list_id = true""",
             """create or replace view current_product_costs as
			    select pc.product_id, pc.mtl_cost, pc.labor_cost, 
			    pc.burden_cost, pc.cost_id
				from product_costs pc
				 inner join (
				   select max(cost_id) as cost_id, product_id
				   from product_costs
				   group by 2
				   ) most_recent
				 on pc.cost_id = most_recent.cost_id"""
             )

# Create views


def add_views():
    for v in view_defs:
        session.execute(v)
    session.close()
    print('All views have been created.')
