FROM python:3.11-slim
LABEL maintainer="support@smartquail.io"

ENV PYTHONUNBUFFERED=1
ENV NODE_VERSION=qnd041app
ENV NODE_APP_NAME=qnd041app
ENV USER=qnd111
ENV VERSION=111
ENV PATH="/py/bin:/scripts:$PATH"

# Dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libffi-dev \
    libjpeg-dev \
    zlib1g-dev \
    wget \
    curl \
    fonts-dejavu \
    gettext \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Crear virtualenv
RUN python3.11 -m venv /py && \
    /py/bin/pip install --upgrade pip wheel setuptools

# Copiar requerimientos y scripts
COPY ./${VERSION}.txt /${VERSION}.txt
COPY ./scripts /scripts
COPY ./uwsgi_pro.ini /${NODE_VERSION}/${NODE_APP_NAME}/uwsgi_pro.ini
COPY ./qnode_ascii-art.txt /${NODE_VERSION}/${NODE_APP_NAME}/qnode_art.txt

# Instalar dependencias Python
RUN /py/bin/pip install -r /${VERSION}.txt

# Crear usuario y carpetas
RUN adduser --disabled-password --gecos "" ${USER} && \
    mkdir -p /${NODE_VERSION}/${NODE_APP_NAME}/static \
             /${NODE_VERSION}/${NODE_APP_NAME}/media \
             /${NODE_APP_NAME}/${NODE_APP_NAME}/staticfiles \
             /var/log/uwsgi && \
    chmod -R 755 /${NODE_VERSION}/${NODE_APP_NAME} /scripts /var/log/uwsgi && \
    chown -R ${USER}:${USER} /${NODE_VERSION}/${NODE_APP_NAME} \
                             /var/log/uwsgi

WORKDIR /${NODE_VERSION}/${NODE_APP_NAME}
EXPOSE 9000
USER ${USER}

CMD ["uwsgi.sh"]
