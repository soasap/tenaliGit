# *****  This is DB Pythn class to serve DB connection & Data retrivals **** #
# ************************************************************************** #

# IMPORTS START HERE
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String

meta = MetaData()

# DB COnnection URL
db_conn_string = "mysql+pymysql://u29f0hbmctd3awi4wagi:pscale_pw_IRw1B2YHTflvBz66fvqEKyEiXkEg4F18kGzOmYfSXIV@aws.connect.psdb.cloud/vensun?charset=utf8mb4"

# Invoking engine
engine = create_engine(db_conn_string,
                       connect_args={"ssl": {
                           "ssl_ca": "/etc/ssl/cert.pem"
                       }})


# Creating function just send connection obect who ever call..
def getDBConnection():
  conn = engine.connect()
  return conn


# Creating function just send connection obect who ever call..
def getDBConnWithQuery(query):
  conn = engine.connect()
  return conn
  # Return query result records in table


# **************   End of DB Connection & Data retrivals   ***************

accounts = Table(
    'accounts',
    meta,
    Column('id', Integer, primary_key=True),
    Column('username', String),
    Column('password', String),
    Column('email', String),
)

#s = accounts.select()
#s = accounts.select().where(accounts.c.id == 1)
s = accounts.select().where((accounts.c.username == "test2")
                            & (accounts.c.password == "test3"))

conn = engine.connect()
myDbQuery = conn.execute(s)

#print("   DbQuery  : ", myDbQuery, "type (myDbQuery) = ", type(myDbQuery))

#print("   DbQuery  : ", myDbQuery, "type (myDbQuery) = ", type(myDbQuery))
# for row in myDbQuery:
#   print(row.id, row.username, row.password, row.email)

#rows = myDbQuery.fetchall()
myrow = myDbQuery.fetchone()
#print("  Rows: ", row)
print("  id : ", myrow.id, "username : ", myrow.username, "password : ",
      myrow.password, "   email:  ", myrow.email)
