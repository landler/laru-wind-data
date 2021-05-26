FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY fetch-fmi-data.py .
COPY requirements.txt .
COPY transform_fmi_data.py .

CMD [ "bash" ]
