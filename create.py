import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'PieDB'

TABLES = {}
TABLES['pietweets'] = (
	"CREATE TABLE `pietweets` ("
	"  `id` int NOT NULL AUTO_INCREMENT,"		
	"  `tweet_id` bigint NOT NULL,"
	"  `username` varchar(32) NOT NULL,"
	"  `geo_lat` float(53) NOT NULL,"
	"  `geo_long` float(53) NOT NULL,"
	"  `text` varchar(255) NOT NULL,"
	"  `timestamp` datetime NOT NULL,"
	"  PRIMARY KEY (`id`)"
	") ENGINE=InnoDB")
# DB credentials
config = {
  'user': 'piemaster',
  'password': 'piemaster123',
  'host': 'piedb.chhtgdmxqekc.us-east-1.rds.amazonaws.com',
  'database': 'PieDB',
  'raise_on_warnings': True,
}

# establish connection with DB config credentials
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

# try connecting to designated DB, if not exist - create this DB
try:
    cnx.database = DB_NAME    
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

# iterate through TABLES and create each table
for name, ddl in TABLES.iteritems():
    try:
        print("Creating table {}: ".format(name))
        cursor.execute(ddl)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

# closing db connection
cursor.close()
cnx.close()



