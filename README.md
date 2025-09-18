To access this mini project, please run this command in the CLI

    docker built -t nginx_image .
    docker run -p 8080:80 -d --name nginx_c nginx_image:latest

and follow this URL afterwards
    **http://localhost:8080**