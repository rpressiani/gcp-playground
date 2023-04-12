FROM python:3.9-alpine

WORKDIR /srv/grpc

COPY src/route_guide_db.json src/route_guide_server.py src/route_guide_resources.py src/*.proto src/requirements.txt ./

RUN pip install -r requirements.txt && \
    python -m grpc_tools.protoc \
        -I. \
        --python_out=. \
        --grpc_python_out=. \
        route_guide.proto

CMD ["python", "route_guide_server.py"]
