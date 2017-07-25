from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, Boolean, Date, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import mysql_connection as mysql

Base = declarative_base()
metadata = MetaData()
# session = sessionmaker()

# session.configure(bind=mysql.engine)

# Product Tables


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


class Products(Base):
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


class ProductCosts(Base):
    __tablename__ = 'product_costs'
    cost_id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    mtl_cost = Column(Numeric)
    labor_cost = Column(Numeric)
    burden_cost = Column(Numeric)


class PriceList(Base):
    __tablename__ = 'price_lists'
    price_list_id = Column(Integer, primary_key=True)
    active = Column(Boolean)
    list_start_date = Column(Date)
    list_end_date = Column(Date)


class ProductsPrices(Base):
    __tablename__ = 'products_prices'
    price_id = Column(Integer, primary_key=True)
    price_list_id = Column(Integer, ForeignKey(PriceList.price_list_id))
    product_id = Column(Integer, ForeignKey(Products.product_id))
    list_price = Column(Numeric)


# Drop all and create
Base.metadata.drop_all(mysql.engine)
Base.metadata.create_all(mysql.engine)
