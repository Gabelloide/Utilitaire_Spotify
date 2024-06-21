# SpotInsights

## General Information

SpotInsights is a client-server application designed to interact with the Spotify API. It allows users to see their recently played tracks, discover personalized recommendations, and analyze their listening habits. The application is divided into several main components:

- **Spotify Client**: Interacts with the Spotify API to retrieve information about users, their favorite tracks, albums, and artists.
- **Server**: Manages user information and interactions with a distant MySQL database.
- **User Interface**: Provides a graphical interface for interacting with the application.

## Client Installation

To install the application, you first need to install the necessary dependencies. Open a terminal and navigate to the root folder of the application. Execute the following command to install dependencies from the `requirements.txt` file:

```sh
pip install -r requirements.txt
```

## Server Installation

Go into the Server folder and install the necessary dependencies with pip:

```sh
pip install -r requirements.txt
```

## Running the Application

### Connect to the API
Due to the application being in development stage, you need to connect to the Spotify API manually. To do so, you need to create a Spotify Developer account and create a new application. Then, you need to provide the client ID and client secret to the application.
Put it in a file named `.env` with the following content:

```sh
SPOTIPY_CLIENT_ID=<client_id>
SPOTIPY_CLIENT_SECRET=<secret_token>
```

### Start a server
To run the application, you need to start the server and the client. First, start the server by running the following command in the Server folder:
- You need to have a MySQL database running on a public IP address that is accessible by the server (localhost is fine for testing). 
- You must create a database named `spotify_history` and a user with a password that will be provided to the server.
- You need to expose 3 ports on your server, so the three threads can listen for incoming connections. 

```sh
python main.py --zip_port <port> --trends_port <port> --userinfo_port <port>
--db_user <user> --db_password <password> --db_address <address> --db_port <port>
```

### Start a client
Then, start the client by running the following command in the root folder of the application:
- You need to match the ports of your server to communicate properly.
- You must provide the server IP address to reach it.

```sh
python main.py --zip_port <port> --trend_port <port> --userinfo_port <port> --server_address <address>
```

# Setup a server using Docker

To setup the server using Docker, you need to have Docker installed on your machine. Then, you need to build the Docker image and run it.
The python server image is built using the dockerfile : you can create an image separately, but it is recommended to use the docker-compose file to build the image alongside MySQL & PHPMyAdmin:

```sh
docker-compose up --build
```

**Examples passwords, users and ports are provided in the docker-compose file. You can change them if you want.**

Docker will launch MySQL, PHPMyAdmin, and the server. You can access PHPMyAdmin on `localhost:8080` and the server ports are exposed, you can see them in the Dockerfile & docker-compose file.
You can then launch a client with matching ports (see earlier). If docker is running on the same machine, server address is `localhost`, otherwise you need to provide the IP address of the server.