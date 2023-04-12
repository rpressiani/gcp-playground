import logging
import random

import grpc

import route_guide_pb2
import route_guide_pb2_grpc
import route_guide_resources


def guide_get_one_feature(stub, point):
    feature = stub.GetFeature(point)
    if not feature.location:
        print("Server returned incomplete feature")
        return

    if feature.name:
        print(
            f"Feature called {feature.name} at latitude={feature.location.latitude} longitude={feature.location.longitude}"
        )
    else:
        print(
            f"Found no feature at latitude={feature.location.latitude} longitude={feature.location.longitude}"
        )


def guide_get_feature(stub):
    guide_get_one_feature(
        stub, route_guide_pb2.Point(latitude=409146138, longitude=-746188906)
    )
    guide_get_one_feature(stub, route_guide_pb2.Point(latitude=1, longitude=1))


def guide_list_features(stub):
    rectangle = route_guide_pb2.Rectangle(
        lo=route_guide_pb2.Point(latitude=400000000, longitude=-750000000),
        hi=route_guide_pb2.Point(latitude=420000000, longitude=-730000000),
    )
    print("Looking for features between 40, -75 and 42, -73")

    features = stub.ListFeatures(rectangle)

    for feature in features:
        if feature.name:
            print(
                f"Feature called {feature.name} at latitude={feature.location.latitude} longitude={feature.location.longitude}"
            )


def generate_route(feature_list):
    for _ in range(0, 10):
        random_feature = feature_list[random.randint(0, len(feature_list) - 1)]
        print(f"Visiting point {random_feature.location}")
        yield random_feature.location


def guide_record_route(stub):
    feature_list = route_guide_resources.read_route_guide_database()

    route_iterator = generate_route(feature_list)
    route_summary = stub.RecordRoute(route_iterator)
    print(f"Finished trip with {route_summary.point_count} points")
    print(f"Passed {route_summary.feature_count} features")
    print(f"Travelled {route_summary.distance} meters")
    print(f"It took {route_summary.elapsed_time} seconds")


def make_route_note(message, latitude, longitude):
    return route_guide_pb2.RouteNote(
        message=message,
        location=route_guide_pb2.Point(latitude=latitude, longitude=longitude),
    )


def generate_messages():
    messages = [
        make_route_note("First message", 0, 0),
        make_route_note("Second message", 0, 1),
        make_route_note("Third message", 1, 0),
        make_route_note("Fourth message", 0, 0),
        make_route_note("Fifth message", 1, 0),
    ]
    for msg in messages:
        print(f"Sending {msg.message} at {msg.location}")
        yield msg


def guide_route_chat(stub):
    responses = stub.RouteChat(generate_messages())
    for response in responses:
        print("Received message {response.message} at {response.location}")


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = route_guide_pb2_grpc.RouteGuideStub(channel)
        print("-------------- GetFeature --------------")
        guide_get_feature(stub)
        print("-------------- ListFeatures --------------")
        guide_list_features(stub)
        print("-------------- RecordRoute --------------")
        guide_record_route(stub)
        print("-------------- RouteChat --------------")
        guide_route_chat(stub)


if __name__ == "__main__":
    logging.basicConfig()
    run()
