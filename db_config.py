import os
from app import app
from flaskext.mysql import MySQL

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = os.getenv("MYSQL_DATABASE_USER")
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv("MYSQL_DATABASE_PASSWORD")
app.config['MYSQL_DATABASE_DB'] = os.getenv("MYSQL_DATABASE_DB")
app.config['MYSQL_DATABASE_HOST'] = os.getenv("MYSQL_DATABASE_HOST")
app.config['MYSQL_DATABASE_PORT'] = os.getenv("MYSQL_DATABASE_PORT")

mysql.init_app(app)
