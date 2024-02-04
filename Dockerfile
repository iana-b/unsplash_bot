FROM python:3.11

RUN apt-get update && apt-get install -y

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]