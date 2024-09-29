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

from jsonschema.validators import Draft202012Validator
from owslib.ogcapi.records import Records
import requests

from pygeoapi.process.base import BaseProcessor, ProcessorExecuteError

LOGGER = logging.getLogger(__name__)

REGISTER_SCHEMA = {
    '$schema': 'https://json-schema.org/draft/2020-12/schema',
    '$id': 'eoepca-registration-api-process-registrar-register',
    'title': 'EOEPCA registration API register schema',
    'description': 'EOEPCA registration API register schema',
    'type': 'object',
    'required': [
        'type',
        'source'
    ],
    'properties': {
        'type': {
            'type': 'string',
            'description': 'Resource type'
        },
        'source': {
            'oneOf': [{
                '$ref': 'https://raw.githubusercontent.com/radiantearth/stac-spec/refs/heads/master/item-spec/json-schema/item.json'  # noqa
            }, {
                'type': 'string',
                'format': 'uri',
                'description': 'Source data from URL'
            }]
        }
    }
}

DEREGISTER_SCHEMA = {
    '$schema': 'https://json-schema.org/draft/2020-12/schema',
    '$id': 'eoepca-registration-api-process-registrar-deregister',
    'title': 'EOEPCA registration API deregister schema',
    'description': 'EOEPCA registration API deregister schema',
    'type': 'object',
    'required': [
        'id'
    ],
    'properties': {
        'id': {
            'type': 'string',
            'description': 'Resource identifier'
        }
    }
}

PROCESS_REGISTER_METADATA = {
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
            'schema': REGISTER_SCHEMA['properties']['type'],
            'minOccurs': 1,
            'maxOccurs': 1,
            'keywords': ['type']
        },
        'source': {
            'title': 'Source',
            'description': 'Source of resource',
            'schema': REGISTER_SCHEMA['properties']['source'],
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


PROCESS_DEREGISTER_METADATA = {
    'version': '0.1.0',
    'id': 'deregistrar',
    'title': {
        'en': 'Resource deregistration'
    },
    'description': {
        'en': 'Resource deregistration'
    },
    'jobControlOptions': ['sync-execute', 'async-execute'],
    'keywords': ['resource', 'deregistration'],
    'links': [{
        'type': 'text/html',
        'rel': 'about',
        'title': 'information',
        'href': 'https://eoepca.readthedocs.io/projects/resource-registration',
        'hreflang': 'en-US'
    }],
    'inputs': {
        'id': {
            'id': 'Identifier',
            'description': 'Resource identifier',
            'schema': DEREGISTER_SCHEMA['properties']['id'],
            'minOccurs': 1,
            'maxOccurs': 1,
            'keywords': ['identifier']
        }
    },
    'outputs': {
        'deregistrar': {
            'title': 'Resource deregistration',
            'description': 'Resource deregistration',
            'schema': {
                'type': 'object',
                'contentMediaType': 'application/json'
            }
        }
    },
    'example': {
        'inputs': {
            'id': 'id123'
        }
    }
}


class RegisterProcessor(BaseProcessor):
    """Register Processor"""

    def __init__(self, processor_def):
        """
        Initialize object

        :param processor_def: provider definition

        :returns: pygeoapi.process.registration.RegisterProcessor
        """

        super().__init__(processor_def, PROCESS_REGISTER_METADATA)
        self.supports_outputs = True

    def execute(self, data, outputs=None):
        mimetype = 'application/json'

        validation_errors = []
        target = data.get('target')

        LOGGER.debug('Validating input against schema')
        validator = Draft202012Validator(REGISTER_SCHEMA)

        for error in validator.iter_errors(data):
            LOGGER.debug(f'{error.json_path}: {error.message}')
            validation_errors.append(f'{error.json_path}: {error.message}')

        if validation_errors:
            raise ProcessorExecuteError(validation_errors)

        content = requests.get(data['source']).json()

        id_ = content['id']

        r = Records(target)

        try:
            _ = r.collection_item('metadata:main', id_)
            r.collection_item_update('metadata:main', id_, content)
        except RuntimeError:
            r.collection_item_create('metadata:main', content)

        produced_outputs = {}

        if not bool(outputs):
            produced_outputs = {
                'id': PROCESS_REGISTER_METADATA['id'],
                'resource-and-data-catalogue-link': {
                    'href': f'{target}/collections/metadata:main/items/{id_}',
                    'rel': 'item',
                    'type': 'application/geo+json'
                }
            }

        return mimetype, produced_outputs

    def __repr__(self):
        return f'<RegisterProcessor> {self.name}'


class DeregisterProcessor(BaseProcessor):
    """Deregister Processor"""

    def __init__(self, processor_def):
        """
        Initialize object

        :param processor_def: provider definition

        :returns: pygeoapi.process.registration.DeregisterProcessor
        """

        super().__init__(processor_def, PROCESS_DEREGISTER_METADATA)
        self.supports_outputs = True

    def execute(self, data, outputs=None):
        mimetype = 'application/json'

        validation_errors = []
        target = data.get('target')

        LOGGER.debug('Validating input against schema')
        validator = Draft202012Validator(DEREGISTER_SCHEMA)

        for error in validator.iter_errors(data):
            LOGGER.debug(f'{error.json_path}: {error.message}')
            validation_errors.append(f'{error.json_path}: {error.message}')

        if validation_errors:
            raise ProcessorExecuteError(validation_errors)

        id_ = data['id']

        r = Records(target)

        try:
            _ = r.collection_item('metadata:main', id_)
            r.collection_item_delete('metadata:main', id_)
        except RuntimeError as err:
            LOGGER.error(err)

        produced_outputs = {}

        if not bool(outputs):
            produced_outputs = {
                'id': PROCESS_DEREGISTER_METADATA['id']
            }

        return mimetype, produced_outputs

    def __repr__(self):
        return f'<RegisterProcessor> {self.name}'
