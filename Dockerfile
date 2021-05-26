FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apt-get update && apt-get install -y libgeos-dev libproj-dev
RUN pip install shapely --no-binary shapely
RUN pip install --no-cache-dir -r requirements.txt

COPY fetch-fmi-data.py .
COPY requirements.txt .
COPY transform_fmi_data.py .
COPY hirlam_map_wind.py .
COPY map_cloud_cover.py .

CMD [ "bash" ]
