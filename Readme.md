## Clone the git repo

## Docker commands to build and run a docker container

```bash
    
        // build a docker image
        docker build -t <imageName:version> dockerFilePath

        // list all docker images
        docker images

        // run the docker container
        docker run -it -d -p <outsidePort>:<dockerInsidePort> <imageName:version>

        // List all running container
        docker ps

```


## API to get the total cart price

```python

        http://localhost:5000/api/v1.0/data?items='AP1, AP1, CH1, AP1'

```

