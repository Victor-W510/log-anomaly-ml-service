FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python src/train.py

CMD ["python", "src/pedict.py"]