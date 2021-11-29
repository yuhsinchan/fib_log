# fib_log

## How to run

* Install project dependencies

```bash
# Install protobuf compiler
$ sudo apt-get install protobuf-compiler

# Install buildtools
$ sudo apt-get install build-essential make

# Install modules
$ pip3 install -r requirements.txt
```

* Compile protobuf schema to python wrapper

```bash
$ cd gRPC
$ make
```

### open first terminal

* Migrate database tables

```bash
$ cd django/
$ python3 manage.py migrate
```

* Run the backend server

```bash
$ python3 manage.py runserver 0.0.0.0:8080
```

### open second terminal

* Start the gRPC service

```bash
$ cd gRPC
$ python3 fib.py --ip 0.0.0.0 --port 8000
```

### open third terminal

* Run the eclipse mosquitto docker container

```bash
$ docker run -d -it -p 1883:1883 -v $(pwd)/mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto
```

* Start the gRPC service and the subscriber

```bash
$ cd gRPC
$ python3 log.py
```

### demo

https://youtu.be/RF79VCV46DM
