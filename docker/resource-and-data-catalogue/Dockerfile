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

FROM ubuntu:noble-20250910

# ARGS
ARG TZ="Etc/UTC"
ARG LANG="en_US.UTF-8"

# ENV settings
ENV TZ=${TZ} \
    LANG=${LANG} \
    DEBIAN_FRONTEND="noninteractive" \
    DEB_BUILD_DEPS="\
    software-properties-common" \
    DEB_PACKAGES="\
    git \
    locales \
    tzdata \
    python3-pip \
    python3-venv"

ENV PYCSW_CONFIG=/etc/pycsw/pycsw.yml

WORKDIR /pycsw

ADD entrypoint.py /entrypoint.py
ADD requirements.txt /pycsw/

# Install operating system dependencies
RUN \
    apt-get update -y \
    && apt-get install -y ${DEB_BUILD_DEPS} \
    && apt-get --no-install-recommends install -y ${DEB_PACKAGES} \
    && apt-get remove --purge -y gcc ${DEB_BUILD_DEPS} \
    && apt-get clean \
    && apt autoremove -y  \
    && rm -rf /var/lib/apt/lists/*

# Install pycsw
RUN python3 -m venv --system-site-packages /venv \
    && /venv/bin/pip3 install --no-cache-dir -r requirements.txt \
    && chmod -R g=u /pycsw \
    && chown -R ubuntu /pycsw

USER ubuntu

ENTRYPOINT [ "/venv/bin/python3", "/entrypoint.py" ]
