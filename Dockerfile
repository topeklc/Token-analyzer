FROM alpine:latest
RUN apk update
RUN apk upgrade
RUN apk add bash
RUN apk --update add python3
RUN apk add --update nodejs npm
RUN apk add g++
RUN apk add gcc
RUN apk add make
RUN npm install -g ganache@7.0.1
COPY requirements.txt requirements.txt
RUN apk add py3-pip
RUN apk add python3-dev
RUN apk add libevent-dev
RUN apk add --no-cache libstdc++
RUN apk add musl-dev
RUN pip install --upgrade pip
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt
RUN apk add psmisc
RUN apk add libc6-compat
RUN ln -s /lib/libc.musl-x86_64.so.1 /lib/ld-linux-x86-64.so.2

COPY . .

CMD ["gunicorn"  , "-b", "0.0.0.0:8888", "app:app"]
