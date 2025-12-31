FROM python:3.11-slim
LABEL maintainer="support@smartquail.io"

ENV PYTHONUNBUFFERED=1
ENV NODE_VERSION=qnd041app
ENV NODE_APP_NAME=qnd041app
ENV USER=qnd111
ENV VERSION=111

# -----------------------------
# Dependencias del sistema (uWSGI + WeasyPrint)
# -----------------------------
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
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# Clonar proyecto
# -----------------------------
RUN git clone https://github.com/smartquailstage/${NODE_VERSION}.git

# -----------------------------
# Archivos necesarios
# -----------------------------
COPY ./${VERSION}.txt /${VERSION}.txt
COPY ./scripts /scripts
COPY ./uwsgi_pro.ini /${NODE_VERSION}/${NODE_APP_NAME}/uwsgi_pro.ini

WORKDIR /${NODE_VERSION}/${NODE_APP_NAME}

# -----------------------------
# Virtualenv + dependencias Python
# -----------------------------
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip wheel setuptools && \
    /py/bin/pip install -r /${VERSION}.txt

# -----------------------------
# Usuario no root
# -----------------------------
RUN useradd --no-create-home --shell /usr/sbin/nologin ${USER}

# -----------------------------
# Carpetas y permisos
# -----------------------------
RUN mkdir -p static media /var/log/uwsgi && \
    chmod -R 755 static media /var/log/uwsgi /scripts && \
    chown -R ${USER}:${USER} static media /var/log/uwsgi /scripts /${NODE_VERSION}

# -----------------------------
# PATH
# -----------------------------
ENV PATH="/py/bin:/scripts:$PATH"

# -----------------------------
# Permisos scripts
# -----------------------------
RUN chmod +x /scripts/uwsgi.sh

USER ${USER}

EXPOSE 9000

CMD ["uwsgi.sh"]
