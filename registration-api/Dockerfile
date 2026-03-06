###############################################################################
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
###############################################################################

FROM ubuntu:noble

# ARGS
ARG TZ="Etc/UTC"
ARG LANG="en_US.UTF-8"

# ENV settings
ENV TZ=${TZ} \
    LANG=${LANG} \
    DEBIAN_FRONTEND="noninteractive" \
    DEB_BUILD_DEPS="\
    software-properties-common \
    unzip" \
    DEB_PACKAGES="\
    curl \
    git \
    locales \
    tzdata \
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
    python3-tinydb \
    python3-venv" \
    REGISTRATION_API_SCHEMAS=/registration-api/schemas

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

ADD registration_api/resources/schemas ${REGISTRATION_API_SCHEMAS}
ADD requirements.txt /pygeoapi/
ADD docker/registration-api.config.yml /pygeoapi/local.config.yml
ADD docker/entrypoint.sh /entrypoint.sh
ADD registration_api /usr/local/lib/python3.12/dist-packages/registration_api

# Install pygeoapi
RUN python3 -m venv --system-site-packages /venv \
    && /venv/bin/python3 -m pip install --no-cache-dir -r requirements.txt \
    && chmod -R g=u /pygeoapi \
    && chown -R ubuntu /pygeoapi \
    && mkdir -p /openapi \
    && chmod -R g=u /openapi \
    && chown -R ubuntu /openapi

USER ubuntu

ENTRYPOINT ["/entrypoint.sh"]
