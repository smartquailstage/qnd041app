FROM python:3.11-slim
LABEL maintainer="support@smartquail.io"

# -----------------------------
# Variables de entorno
# -----------------------------
ENV PYTHONUNBUFFERED=1
ENV NODE_VERSION=qnd041app
ENV NODE_APP_NAME=qnd041app
ENV USER=qnd111
ENV VERSION=111

# -----------------------------
# Dependencias del sistema
# (uWSGI + WeasyPrint + Pillow)
# -----------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libc6-dev \
    python3-dev \
    libpcre2-dev \
    libssl-dev \
    libjpeg-dev \
    zlib1g-dev \
    libffi-dev \
    gettext \
    curl \
    git \
    ca-certificates \
    fonts-dejavu-core \
    fonts-liberation \
    fonts-noto \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# Clonar el proyecto
# -----------------------------
RUN git clone https://github.com/smartquailstage/${NODE_VERSION}.git

# -----------------------------
# Archivos del proyecto
# -----------------------------
COPY ./${VERSION}.txt /${VERSION}.txt
COPY ./scripts /scripts
COPY ./uwsgi_pro.ini /${NODE_VERSION}/${NODE_APP_NAME}/uwsgi_pro.ini

# -----------------------------
# Directorio de trabajo
# -----------------------------
WORKDIR /${NODE_VERSION}/${NODE_APP_NAME}

# -----------------------------
# Virtualenv + dependencias Python
# -----------------------------
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip setuptools wheel && \
    /py/bin/pip install -r /${VERSION}.txt

# -----------------------------
# Crear usuario no-root
# -----------------------------
RUN useradd --no-create-home --shell /usr/sbin/nologin ${USER}

# -----------------------------
# Carpetas necesarias
# -----------------------------
RUN mkdir -p \
        static \
        media \
        staticfiles \
        /var/log/uwsgi \
    && chown -R ${USER}:${USER} \
        static \
        media \
        staticfiles \
        /var/log/uwsgi \
        /${NODE_VERSION}

# -----------------------------
# PATH
# -----------------------------
ENV PATH="/py/bin:/scripts:$PATH"

# -----------------------------
# Permisos scripts
# -----------------------------
RUN chmod +x /scripts/uwsgi.sh

# -----------------------------
# Usuario final
# -----------------------------
USER ${USER}

# -----------------------------
# Puerto
# -----------------------------
EXPOSE 9000

# -----------------------------
# Comando de inicio
# -----------------------------
CMD ["uwsgi.sh"]
