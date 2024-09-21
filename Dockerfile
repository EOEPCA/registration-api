FROM ubuntu:jammy-20240911.1

# ARGS
ARG TZ="Etc/UTC"
ARG LANG="en_US.UTF-8"

# ENV settings
ENV TZ=${TZ} \
    LANG=${LANG} \
    DEBIAN_FRONTEND="noninteractive" \
    DEB_BUILD_DEPS="\
    software-properties-common \
    curl \
    unzip" \
    DEB_PACKAGES="\
    locales \
    tzdata \
    gunicorn \
    python3-flask \
    python3-dateutil \
    python3-gevent \
    python3-greenlet \
    python3-pip \
    python3-tz \
    python3-yaml \
    python3-pyproj \
    python3-rasterio \
    python3-shapely \
    python3-tinydb"

WORKDIR /pygeoapi

# Install operating system dependencies
RUN \
    apt-get update -y \
    && apt-get install -y ${DEB_BUILD_DEPS} \
    && add-apt-repository ppa:ubuntugis/ubuntugis-unstable \
    && apt-get --no-install-recommends install -y ${DEB_PACKAGES} \
    && apt-get remove --purge -y gcc ${DEB_BUILD_DEPS} \
    && apt-get clean \
    && apt autoremove -y  \
    && rm -rf /var/lib/apt/lists/*

ADD requirements.txt /pygeoapi/
ADD default.config.yml /pygeoapi/local.config.yml
ADD entrypoint.sh /entrypoint.sh

# Install pygeoapi
RUN python3 -m pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["/entrypoint.sh"]

