import time
from concurrent import futures

import grpc
import location_pb2
import location_pb2_grpc
from service import  LocationService
from kafka import KafkaConsumer, KafkaProducer


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
    LocationService.create(int(request.person_id), float(request.longitude), float(request.latitude))

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