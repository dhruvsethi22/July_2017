import pymysql
import datetime
import random
from faker import Faker
from sqlalchemy import Column,String,Integer,Float,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()



class Countries(Base):
    __tablename__= 'Countries'
    country_id = Column(Integer, primary_key=True)
    country_name = Column(String(500))
    created_date = Column(DateTime)
    last_updated_date = Column(DateTime)
    states_provs = relationship("States_Provs", backref = "country", lazy = 'dynamic')
    customer = relationship ("Customer", backref = "country", lazy = "dynamic")

class States_Provs(Base):
    __tablename__= 'States_Provs'
    state_prov_id = Column(Integer, primary_key=True)
    state_name = Column(String(500))
    country_id = Column(Integer,ForeignKey(Countries.country_id))
    created_date = Column(DateTime)
    last_updated_date = Column(DateTime)
    customer = relationship ("Customer", backref = "states_provs", lazy = "dynamic")

class Customer(Base):
    __tablename__= 'Customer'
    customer_id = Column(Integer, primary_key=True)
    customer_name = Column(String(500))
    address = Column(String(100))
    city = Column(String(100))
    state_prov_id = Column(Integer, ForeignKey(States_Provs.state_prov_id))
    country_id = Column(Integer,ForeignKey(Countries.country_id))
    postal_code = Column(String(20))
    ship_to = Column(Integer)
    sold_to = Column(Integer)
    created_date = Column(DateTime)
    last_updated_date = Column(DateTime)




from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:Timepass22#@localhost/demo')
from sqlalchemy.orm import sessionmaker
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)


def populate_cus(number):
    fake_data = Faker()
    s = session()
    c = Countries(country_name = "USA", created_date = datetime.datetime.utcnow(),
    last_updated_date = datetime.datetime.utcnow())
    s.add(c)
    for i in range (0, number):
        sp = States_Provs(state_name = fake_data.state(), country = c, created_date = datetime.datetime.utcnow(),
        last_updated_date = datetime.datetime.utcnow())
        s.add(sp)
        for i in range(0,12):
            cus = Customer( customer_id = random.randint(1001, 999999), customer_name = fake_data.name(), address = fake_data.street_address(), city = fake_data.city(),
            state_prov_id = random.randint(1,10), country = c, ship_to = random.randint(0,1), sold_to = random.randint(0,1),
            postal_code = fake_data.postalcode(), created_date = datetime.datetime.utcnow(),
            last_updated_date = datetime.datetime.utcnow())
            s.add(cus)
    s.commit()
    s.close()


populate_cus(50)
