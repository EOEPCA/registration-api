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

import logging

from pygeometa.core import import_metadata
import yaml

LOGGER = logging.getLogger(__name__)


def from_cwl(cwl: dict, url: str = None,
             parent_identifier: str = None) -> dict:
    """
    Transforms a CWL object to pygeometa MCF model

    :param cwl: `dict` of CWL object
    :param url: optional `str` of URL
    :param parent_identifier: optional `str` of parent identifier

    :returns: `dict` of MCF object
    """

    mcf = import_metadata('cwl', yaml.safe_dump(cwl))

    if parent_identifier is not None:
        mcf['metadata']['parentidentifier'] = parent_identifier

    if url is not None:
        mcf['distribution']['http'] = {
            'rel': 'canonical',
            'url': url,
            'type': 'application/x-yaml',
            'name': mcf['identification']['title'],
            'description': mcf['identification']['abstract']
        }

    LOGGER.info(f'MCF: {mcf}')

    return mcf
