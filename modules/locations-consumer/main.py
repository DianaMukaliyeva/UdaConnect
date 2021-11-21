import os
import psycopg2
from kafka import KafkaConsumer
from json import loads

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

TOPIC_NAME = 'locations'
KAFKA_SERVER = 'kafka-service:9092'

def db_connect():
  return psycopg2.connect(dbname=DB_NAME,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
          )

def create_location(location):
  db = db_connect()
  cursor = db.cursor()
  cursor.execute('INSERT INTO location (person_id, coordinate) VALUES (%s, ST_POINT(%s, %s))',
                  (location['person_id'], location['latitude'], location['longitude'])
                )
  db.commit()
  cursor.close()
  db.close()

while True:
  consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER)

  for location in consumer:
    create_location(loads(location.value.decode("utf-8")))