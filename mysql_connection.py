from sqlalchemy import create_engine


engine = create_engine(
    'mysql+pymysql://michaelkunc:welcome123@localhost/transactions')
