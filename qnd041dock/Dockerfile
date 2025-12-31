FROM python:3.11-slim
LABEL maintainer="support@smartquail.io"

ENV PYTHONUNBUFFERED=1
ENV NODE_VERSION=qnd041app
ENV NODE_APP_NAME=qnd041app
ENV USER=qnd111
ENV VERSION=111

# Dependencias del sistema necesarias para uWSGI
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libc6-dev \
    python3-dev \
    libpcre3-dev \
    libssl-dev \
    libjpeg-dev \
    zlib1g-dev \
    gettext \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Clonar repo
RUN git clone https://github.com/smartquailstage/${NODE_VERSION}.git

COPY ./${VERSION}.txt /${VERSION}.txt
COPY ./scripts /scripts
COPY ./uwsgi_pro.ini /${NODE_VERSION}/${NODE_APP_NAME}/uwsgi_pro.ini

WORKDIR /${NODE_VERSION}/${NODE_APP_NAME}

# Virtualenv
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /${VERSION}.txt

# Usuario
RUN useradd --no-create-home --shell /usr/sbin/nologin ${USER}

# Carpetas
RUN mkdir -p static media /var/log/uwsgi && \
    chown -R ${USER}:${USER} static media /var/log/uwsgi /${NODE_VERSION}

ENV PATH="/py/bin:/scripts:$PATH"

RUN chmod +x /scripts/uwsgi.sh

USER ${USER}

EXPOSE 9000

CMD ["uwsgi.sh"]
