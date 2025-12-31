FROM python:3.11-alpine
LABEL maintainer="support@smartquail.io"

ENV PYTHONUNBUFFERED=1
ENV NODE_VERSION=qnd041app
ENV NODE_APP_NAME=qnd041app
ENV USER=qnd111
ENV VERSION=111
ENV PATH="/py/bin:/scripts:$PATH"

# Instalar dependencias básicas y build tools necesarias para uWSGI
RUN apk add --no-cache \
    build-base \
    python3-dev \
    libffi-dev \
    musl-dev \
    linux-headers \
    jpeg-dev \
    zlib-dev \
    postgresql-dev \
    postgresql-client \
    curl \
    wget \
    fontconfig \
    ttf-freefont \
    font-noto \
    busybox-extras \
    gettext \
    bash

# Crear virtualenv e instalar pip
RUN python3.11 -m venv /py && \
    /py/bin/pip install --upgrade pip wheel setuptools

# Copiar requerimientos y scripts
COPY ./${VERSION}.txt /${VERSION}.txt
COPY ./scripts /scripts
COPY ./uwsgi_pro.ini /${NODE_VERSION}/${NODE_APP_NAME}/uwsgi_pro.ini
COPY ./qnode_ascii-art.txt /${NODE_VERSION}/${NODE_APP_NAME}/qnode_art.txt

# Instalar dependencias Python (uWSGI ahora compilará bien)
RUN /py/bin/pip install -r /${VERSION}.txt

# Crear usuario y carpetas necesarias
RUN adduser --disabled-password --no-create-home ${USER} && \
    mkdir -p /${NODE_VERSION}/${NODE_APP_NAME}/static \
             /${NODE_VERSION}/${NODE_APP_NAME}/media \
             /${NODE_APP_NAME}/${NODE_APP_NAME}/staticfiles \
             /var/log/uwsgi && \
    chmod -R 755 /${NODE_VERSION}/${NODE_APP_NAME} \
                /scripts \
                /${NODE_APP_NAME}/${NODE_APP_NAME}/staticfiles \
                /var/log/uwsgi && \
    chown -R ${USER}:${USER} /${NODE_VERSION}/${NODE_APP_NAME} \
                             /${NODE_APP_NAME}/${NODE_APP_NAME}/staticfiles \
                             /var/log/uwsgi && \
    chmod -R +x /scripts

# Configurar zona horaria y locales
RUN apk add --no-cache tzdata musl musl-utils musl-locales && \
    cp /usr/share/zoneinfo/America/Guayaquil /etc/localtime && \
    echo 'export LC_ALL=es_ES.UTF-8' >> /etc/profile.d/locale.sh && \
    sed -i 's|LANG=C.UTF-8|LANG=es_ES.UTF-8|' /etc/profile.d/locale.sh

ENV TZ=America/Guayaquil
ENV LANG=es_ES.UTF-8
ENV LANGUAGE=es_ES.UTF-8

WORKDIR /${NODE_VERSION}/${NODE_APP_NAME}
EXPOSE 9000

USER ${USER}

CMD ["uwsgi.sh"]
