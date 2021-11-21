import time
from concurrent import futures

import grpc
import location_pb2
import location_pb2_grpc
from service import  LocationService
from kafka import KafkaProducer
from json import dumps

TOPIC_NAME = 'locations'
KAFKA_SERVER = 'kafka-service:9092'

class LocationServicer(location_pb2_grpc.LocationServiceServicer):
  def Get(self, request, context):
    request_value = LocationService.get(request.id)
    return location_pb2.LocationMessage(**request_value)

  def Create(self, request, context):
    request_value = {
      "person_id": int(request.person_id),
      "longitude": float(request.longitude),
      "latitude": float(request.latitude),
    }
    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
    producer.send(TOPIC_NAME, dumps(request_value).encode())
    producer.flush()

    return location_pb2.LocationMessage(**request_value)


# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)


print("Server starting...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)