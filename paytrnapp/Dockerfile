FROM python:3.9
WORKDIR /usr/src/paytrnapp
COPY ./bin ./bin
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "./bin/run.py"]
