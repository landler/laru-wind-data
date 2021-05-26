# laru-wind-data

Build docker container:

`docker build -t laru-forecast .`



Start interactive bash to run the scripts - mounting directory local-data on container as data dir used for input & output:

`docker run -v local-data:/data -it laru-forecast bash`


In container shell to download example data:

`cd /data && wget http://s3-eu-west-1.amazonaws.com/fmi-opendata-rcrhirlam-surface-grib/2021/05/24/00/numerical-hirlam74-forecast-WindUMS-20210524T000000Z.grb2`

`cd /data && wget http://s3-eu-west-1.amazonaws.com/fmi-opendata-rcrhirlam-surface-grib/2021/05/24/00/numerical-hirlam74-forecast-WindVMS-20210524T000000Z.grb2`