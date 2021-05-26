# laru-wind-data

Build docker container:

`docker build -t laru-forecast .`



Start interactive bash to run the scripts - mounting directory local-data on container as data dir used for input & output:

`docker run -v local-data:/data -it laru-forecast bash`
