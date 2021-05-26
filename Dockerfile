FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apt-get update && apt-get install -y libgeos-dev libproj-dev
RUN pip install shapely --no-binary shapely
RUN pip install --no-cache-dir -r requirements.txt

COPY fetch-fmi-data.py .
COPY requirements.txt .
COPY transform_fmi_data.py .
COPY fetch-hirlam-forecasts.py .
COPY reduce_hirlam_forecasts.py .

CMD [ "bash" ]
