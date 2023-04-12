FROM python:3

RUN apt-get -y update --fix-missing && \
    apt-get -y upgrade && \
    apt-get clean
RUN apt-get install -y netcat
RUN apt-get install -y net-tools
RUN apt-get install -y iputils-ping
RUN apt-get install -y zsh
RUN apt-get install -y git
RUN python -m pip install --upgrade pip

WORKDIR /code

COPY requirements.txt .
RUN pip install -r /code/requirements.txt

RUN chmod +x ./run.sh
RUN chmod -R 777 ./

CMD ["./run.sh"]