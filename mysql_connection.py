from sqlalchemy import create_engine

mysql_un_pw = 'michaelkunc:welcome123'

transactions = create_engine(
    'mysql+pymysql://{}@localhost/transactions'.format(mysql_un_pw))

cities = create_engine(
    'mysql+pymysql://{}@localhost/us_cities'.format(mysql_un_pw))
