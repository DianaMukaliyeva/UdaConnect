import grpc
import location_pb2
import location_pb2_grpc

"""
Sample implementation of sending requests using gRPC.
"""


channel = grpc.insecure_channel("localhost:5005")
stub = location_pb2_grpc.LocationServiceStub(channel)

location = location_pb2.LocationMessage(
    person_id=5,
    longitude=22.22,
    latitude=22.33
)

print("Getting location...")
response = stub.Get(location_pb2.LocationMessage(id=30))
print(response)
print("Creating location...")
response = stub.Create(location)
print(response)