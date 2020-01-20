FROM python:3

COPY . .

RUN pip install -r requirements.txt

# default location - can be changed by setting the -url flag on docker run
RUN mkdir downloads

ENTRYPOINT [ "python", "run.py" ]