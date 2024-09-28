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

import requests

from pygeoapi.process.base import BaseProcessor, ProcessorExecuteError


LOGGER = logging.getLogger(__name__)

#: Process metadata and description
PROCESS_METADATA = {
    'version': '0.1.0',
    'id': 'registrar',
    'title': {
        'en': 'Resource registration'
    },
    'description': {
        'en': 'Resource registration'
    },
    'jobControlOptions': ['sync-execute', 'async-execute'],
    'keywords': ['resource', 'registration'],
    'links': [{
        'type': 'text/html',
        'rel': 'about',
        'title': 'information',
        'href': 'https://eoepca.readthedocs.io/projects/resource-registration',
        'hreflang': 'en-US'
    }],
    'inputs': {
        'type': {
            'title': 'Type',
            'description': 'Type of resource',
            'schema': {
                'type': 'string'
            },
            'minOccurs': 1,
            'maxOccurs': 1,
            'keywords': ['type']
        },
        'source': {
            'title': 'Source',
            'description': 'Source of resource',
            'schema': {
                '$ref': 'https://raw.githubusercontent.com/radiantearth/stac-spec/refs/heads/master/item-spec/json-schema/item.json'  # noqa
            },
            'minOccurs': 0,
            'maxOccurs': 1,
            'keywords': ['source']
        }
    },
    'outputs': {
        'registrar': {
            'title': 'Resource registration',
            'description': 'Resource registration',
            'schema': {
                'type': 'object',
                'contentMediaType': 'application/json'
            }
        }
    },
    'example': {
        'inputs': {
            'type': 'item',
            'source': 'https://raw.githubusercontent.com/radiantearth/stac-spec/refs/heads/master/examples/simple-item.json'  # noqa
        }
    }
}


class RegistrarProcessor(BaseProcessor):
    """Registrar Processor"""

    def __init__(self, processor_def):
        """
        Initialize object

        :param processor_def: provider definition

        :returns: pygeoapi.process.registration.RegistrarProcessor
        """

        super().__init__(processor_def, PROCESS_METADATA)
        self.supports_outputs = True

    def execute(self, data, outputs=None):
        mimetype = 'application/json'

        type_ = data.get('type')
        source = data.get('source')

        if None in [type_, source]:
            msg = 'Cannot process without a type and source'
            raise ProcessorExecuteError(msg)

        content = requests.get(source).json()

        produced_outputs = {}

        if not bool(outputs) or 'echo' in outputs:
            produced_outputs = {
                'id': PROCESS_METADATA['id'],
                'type': type_,
                'source': source,
                'content': content
            }

        return mimetype, produced_outputs

    def __repr__(self):
        return f'<RegistrarProcessor> {self.name}'
