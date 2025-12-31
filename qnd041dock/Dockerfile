FROM python:3.11-alpine
LABEL maintainer="support@smartquail.io"

ENV PYTHONUNBUFFERED=1
ENV NODE_VERSION=qnd041app
ENV NODE_APP_NAME=qnd041app
ENV USER=qnd111
ENV VERSION=111

# Instalar Git y clonar repositorio
RUN apk add --no-cache git
ARG username=smartquailDev
ARG password=ms1719183830
RUN git clone https://github.com/smartquailstage/${NODE_VERSION}.git

# Copiar archivos locales necesarios
COPY ./${VERSION}.txt /${VERSION}.txt
COPY ./scripts /scripts
COPY ./uwsgi_pro.ini /${NODE_VERSION}/${NODE_APP_NAME}/uwsgi_pro.ini
COPY ./qnode_ascii-art.txt /${NODE_VERSION}/${NODE_APP_NAME}/qnode_art.txt

WORKDIR /${NODE_VERSION}/${NODE_APP_NAME}
EXPOSE 9000

# Crear virtualenv, actualizar pip e instalar dependencias de Alpine
RUN python3.11 -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --no-cache postgresql-client libffi-dev jpeg-dev zlib-dev wget \
        fontconfig ttf-freefont font-noto terminus-font busybox-extras gettext \
        build-base curl postgresql-dev gcc musl-dev python3-dev linux-headers && \
    /py/bin/pip install -r /${VERSION}.txt

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

# Configuración de zona horaria y locales
RUN apk add --no-cache tzdata musl musl-utils musl-locales && \
    cp /usr/share/zoneinfo/America/Guayaquil /etc/localtime && \
    echo 'export LC_ALL=es_ES.UTF-8' >> /etc/profile.d/locale.sh && \
    sed -i 's|LANG=C.UTF-8|LANG=es_ES.UTF-8|' /etc/profile.d/locale.sh

ENV TZ=America/Guayaquil
ENV LANG=es_ES.UTF-8
ENV LANGUAGE=es_ES.UTF-8
ENV PATH="/py/bin:/scripts:$PATH"

USER ${USER}

CMD ["uwsgi.sh"]
