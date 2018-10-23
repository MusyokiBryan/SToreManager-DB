from flask import Flask
from flask_restplus import Api
from Instance.config import app_config
from Instance.config import config
from flask_cors import CORS
import psycopg2
import os


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)

    api = Api(app=app, description="Store Manager is a web application that helps store owners manage sales"
                                   " and product inventory records. This application"
                                   " is meant for use in a single store.",
              title="Store Manager",
              version='1.0',
              doc='/api/v2/documentation'
              )
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.url_map.strict_slashes = False

    CORS(app)

    return app


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        parameters = config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(database=os.getenv('Db'), host=os.getenv('host'), user=os.getenv('user'),
                                password=os.getenv('password'))
        cur = conn.cursor()
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
