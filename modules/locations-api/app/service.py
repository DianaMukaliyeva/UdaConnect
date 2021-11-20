import os
import psycopg2

import location_pb2

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

def db_connect():
  return psycopg2.connect(dbname=DB_NAME,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
          )

class LocationService:
  @staticmethod
  def get(location_id) -> location_pb2.LocationMessage:
    db = db_connect()
    cursor = db.cursor()
    cursor.execute('SELECT id, person_id, ST_X(coordinate) AS longitude, ST_Y(coordinate) AS latitude, TO_CHAR(creation_time,\'MON-DD-YYYY HH12:MIPM\') creation_time FROM location WHERE id = %s', (location_id,))
    location = cursor.fetchone()
    cursor.close()
    db.close()

    return {
      "id": location[0],
      "person_id": location[1],
      "longitude": location[2],
      "latitude": location[3],
      "creation_time": location[4]
    }

  @staticmethod
  def create(person_id, longitude, latitude) -> location_pb2.LocationMessage:
    db = db_connect()
    cursor = db.cursor()
    cursor.execute('INSERT INTO location (person_id, coordinate) VALUES (%s, ST_POINT(%s, %s))', (person_id, latitude, longitude))
    db.commit()
    cursor.close()
    db.close()
