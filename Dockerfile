FROM alpine:latest
RUN apk update upgrade
RUN apk add bash python3 nodejs npm g++ gcc make
RUN npm install -g ganache@7.0.1
COPY requirements.txt requirements.txt
RUN apk add py3-pip python3-dev libevent-dev libstdc++ musl-dev psmisc libc6-compat
RUN pip install --upgrade pip
RUN pip install pip setuptools wheel
RUN pip install -r requirements.txt
RUN ln -s /lib/libc.musl-x86_64.so.1 /lib/ld-linux-x86-64.so.2
COPY . .
CMD ["gunicorn"  , "-b", "0.0.0.0:8888", "app:app"]
