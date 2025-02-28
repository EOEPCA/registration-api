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

SOURCE_TYPES = {
    'collection': 'https://www.iana.org/go/rfc6573',
    'item': 'https://www.iana.org/go/rfc6573'
}
TARGET_TYPES = {
    'ogcapi-records': 'http://www.opengis.net/spec/ogcapi-records-1/1.0',
    'stac-api': 'https://api.stacspec.org/v1.0.0/core'
}

REGISTER_SCHEMA = {
    '$schema': 'https://json-schema.org/draft/2020-12/schema',
    '$id': 'eoepca-registration-api-process-registrar-register',
    'title': 'EOEPCA registration API register schema',
    'description': 'EOEPCA registration API register schema',
    'type': 'object',
    'required': [
        'source',
        'target'
    ],
    'properties': {
        'source': {
            'type': 'object',
            'description': 'Source data',
            'properties': {
                'rel': {
                    'type': 'string',
                    'description': 'Link relation of resource',
                    'enum': list(SOURCE_TYPES.keys())
                },
                'oneOf': [{
                    'content': {
                        'type': 'object',
                        'description': 'Source data from inline content',
                        'oneOf': [{
                            '$ref': 'https://raw.githubusercontent.com/radiantearth/stac-spec/refs/tags/v1.0.0/item-spec/json-schema/item.json'  # noqa
                        }, {
                            '$ref': 'https://raw.githubusercontent.com/radiantearth/stac-spec/refs/tags/v1.1.0/item-spec/json-schema/item.json'  # noqa
                        }, {
                            '$ref': 'https://raw.githubusercontent.com/radiantearth/stac-spec/refs/tags/v1.0.0/collection-spec/json-schema/collection.json'  # noqa
                        }, {
                            '$ref': 'https://raw.githubusercontent.com/radiantearth/stac-spec/refs/tags/v1.1.0/collection-spec/json-schema/collection.json'  # noqa
                        }, {
                            '$ref': 'https://raw.githubusercontent.com/EOEPCA/metadata-profile/refs/heads/master/schemas/resource.json'  # noqa
                        }]
                    },
                    'href': {
                        'type': 'string',
                        'format': 'uri',
                        'description': 'Source data from URL'
                    }
                }]
            },
            'oneOf': [{
                'required': [
                    'rel',
                    'content'
                ]
            }, {
                'required': [
                    'rel',
                    'href'
                ]
            }]
        },
        'target': {
            'type': 'object',
            'description': 'Target service',
            'properties': {
                'rel': {
                    'type': 'string',
                    'description': 'Link relation of resource',
                    'enum': list(TARGET_TYPES.values())
                },
                'href': {
                    'type': 'string',
                    'format': 'uri',
                    'description': 'Endpoint to register to'
                },
                'collection': {
                    'type': 'string',
                    'description': 'Collection name'
                }
            },
            'required': [
                'rel',
                'href'
            ]
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
        'id',
        'rel',
        'collection',
        'target'
    ],
    'properties': {
        'id': {
            'type': 'string',
            'description': 'Resource identifier'
        },
        'rel': {
            'type': 'string',
            'description': 'Link relation of resource',
            'enum': list(SOURCE_TYPES.keys())
        },
        'collection': {
            'type': 'string',
            'description': 'Collection name'
        },
        'target': REGISTER_SCHEMA['properties']['target']
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
        'source': {
            'title': 'Source',
            'description': 'Source of resource to register',
            'schema': REGISTER_SCHEMA['properties']['source'],
            'minOccurs': 1,
            'maxOccurs': 1,
            'keywords': ['source']
        },
        'target': {
            'title': 'Target',
            'description': REGISTER_SCHEMA['properties']['target']['description'],  # noqa
            'schema': REGISTER_SCHEMA['properties']['target'],
            'minOccurs': 1,
            'maxOccurs': 1,
            'keywords': ['target']
        },
    },
    'outputs': {
        'registrar': {
            'title': 'Resource registration',
            'description': 'Resource registration',
            'schema': {
                'contentMediaType': 'application/json',
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'string',
                        'description': 'Identifier'
                    },
                    'resource-and-data-catalogue-link': {
                        'type': 'object',
                        'description': 'Resource and Data Catalogue link',
                        'properties': {
                            'href': {
                                'type': 'string',
                                'description': 'URL of resource'
                            },
                            'rel': {
                                'type': 'string',
                                'description': 'link relation'
                            },
                            'type': {
                                'type': 'string',
                                'description': 'media type'
                            }
                        },
                        'required': [
                            'href',
                            'rel',
                            'type'
                        ]
                    }
                },
                'required': [
                    'id',
                    'resource-and-data-catalogue-link'
                ]
            }
        }
    },
    'example': {
        'inputs': {
            'source': {
                'rel': 'item',
                'href': 'https://raw.githubusercontent.com/radiantearth/stac-spec/refs/heads/master/examples/simple-item.json',  # noqa
            },
            'target': {
                'rel': TARGET_TYPES['ogcapi-records'],
                'href': 'http://localhost:5002'
            }
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
            'title': 'Identifier',
            'description': DEREGISTER_SCHEMA['properties']['id']['description'],  # noqa
            'schema': DEREGISTER_SCHEMA['properties']['id'],
            'minOccurs': 1,
            'maxOccurs': 1,
            'keywords': ['identifier']
        },
        'rel': {
            'title': 'Link relation of resource',
            'description': DEREGISTER_SCHEMA['properties']['rel']['description'],  # noqa
            'schema': DEREGISTER_SCHEMA['properties']['rel'],
            'minOccurs': 1,
            'maxOccurs': 1,
            'keywords': ['link relation']
        },
        'collection': {
            'title': 'Collection name',
            'description': DEREGISTER_SCHEMA['properties']['collection']['description'],  # noqa
            'schema': DEREGISTER_SCHEMA['properties']['collection'],
            'minOccurs': 1,
            'maxOccurs': 1,
            'keywords': ['collection']
        },
        'target': {
            'title': 'Target',
            'description': DEREGISTER_SCHEMA['properties']['target']['description'],  # noqa
            'schema': DEREGISTER_SCHEMA['properties']['target'],
            'minOccurs': 1,
            'maxOccurs': 1,
            'keywords': ['target']
        },
    },
    'outputs': {
        'deregistrar': {
            'title': 'Resource deregistration',
            'description': 'Resource deregistration',
            'schema': {
                'contentMediaType': 'application/json',
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'string',
                        'description': 'Identifier'
                    },
                },
                'required': [
                    'id'
                ]
            }
        }
    },
    'example': {
        'inputs': {
            'id': '20201211_223832_CS',
            'rel': 'item',
            'collection': 'sentinel-2-l2a',
            'target': {
                'rel': TARGET_TYPES['ogcapi-records'],
                'href': 'http://localhost:5002'
            }
        }
    }
}


class RegisterProcessor(BaseProcessor):
    """Register Processor"""

    def __init__(self, processor_def: dict) -> None:
        """
        Initialize object

        :param processor_def: provider definition

        :returns: pygeoapi.process.registration.RegisterProcessor
        """

        super().__init__(processor_def, PROCESS_REGISTER_METADATA)
        self.supports_outputs = True

    def execute(self, data: dict, outputs: dict = None) -> tuple:
        mimetype = 'application/json'

        LOGGER.debug('Validating input against schema')
        validation_errors = validate_json(REGISTER_SCHEMA, data)

        if validation_errors:
            raise ProcessorExecuteError(validation_errors)

        source = data['source']

        LOGGER.info(f"Registering {source['rel']}")

        if source['rel'] not in SOURCE_TYPES:
            msg = f'Invalid type (valid types are: {TARGET_TYPES.values()})'
            LOGGER.error(msg)
            raise ProcessorExecuteError(msg)

        if 'href' in source:
            LOGGER.debug('Source is a URL')
            content = requests.get(source['href']).json()
        else:
            LOGGER.debug('Source is an object')
            content = data['source']['content']

        if not isinstance(content, dict):
            msg = 'Content invalid'
            LOGGER.error(f'{msg}: {content}')
            raise ProcessorExecuteError(msg)

        id_ = content['id']

        target = data['target']
        collection = target.get('collection')

        if target['rel'] not in TARGET_TYPES.values():
            msg = f'Invalid type (valid types are: {TARGET_TYPES.values()})'
            LOGGER.error(msg)
            raise ProcessorExecuteError(msg)

        r = Records(target['href'])

        LOGGER.debug('Resolving collection identification')
        if target['rel'] == TARGET_TYPES['stac-api']:
            LOGGER.debug('STAC API mode detected')
            if collection is None:
                LOGGER.debug('Setting collection from content')
                collection = content.get('collection')
                if collection is None:
                    msg = 'Collection identifier required'
                    LOGGER.error(msg)
                    raise ProcessorExecuteError(msg)
            else:
                LOGGER.debug('Setting collection from target.collection')
                content['collection'] = collection

        if (target['rel'] == TARGET_TYPES['ogcapi-records'] and
                collection is None):
            LOGGER.debug('OGC API - Records mode detected')
            collection = 'metadata:main'

        LOGGER.debug(f'Collection: {collection}')

        if source['rel'] == 'item':
            try:
                _ = r.collection_item(collection, id_)
                r.collection_item_update(collection, id_, content)
            except RuntimeError:
                r.collection_item_create(collection, content)
        elif source['rel'] == 'collection':
            try:
                _ = r.collection(id_)
                r.collection_update(id_, content)
            except RuntimeError:
                r.collection_create(content)

        produced_outputs = {}

        if not bool(outputs):
            url = f"{target['href']}/collections/{collection}/items/{id_}"
            produced_outputs = {
                'id': PROCESS_REGISTER_METADATA['id'],
                'resource-and-data-catalogue-link': {
                    'href': url,
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

        LOGGER.debug('Validating input against schema')
        validation_errors = validate_json(DEREGISTER_SCHEMA, data)
        if validation_errors:
            raise ProcessorExecuteError(validation_errors)

        id_ = data['id']
        rel = data['rel']
        collection = data['collection']
        target = data['target']

        LOGGER.info(f'Deregistering {rel}')

        r = Records(target['href'])

        if rel == 'item':
            if collection is None:
                if target['rel'] == TARGET_TYPES['ogcapi-records']:
                    collection = 'metadata:main'
                elif rel == TARGET_TYPES['stac-api']:
                    msg = 'Collection identifier required'
                    LOGGER.error(msg)
                    raise ProcessorExecuteError(msg)
            try:
                _ = r.collection_item(collection, id_)
                r.collection_item_delete(collection, id_)
            except RuntimeError as err:
                LOGGER.error(err)
        elif rel == 'collection':
            try:
                _ = r.collection(id_)
                r.collection_delete(id_)
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


def get_collection(target: dict, content: dict, collection: str = None) -> str:
    """
    Helper function to derive a collection from a target


    :param target: `dict` of target definition
    :param content: `dict` of content payload
    :param collection: `str` of collection name (optional)

    :returns: `str` of collection name
    """

    LOGGER.debug('Resolving collection identification')
    if target['rel'] == TARGET_TYPES['stac-api']:
        LOGGER.debug('STAC API mode detected')
        if collection is None:
            LOGGER.debug('Setting collection from content')
            collection = content.get('collection')
            if collection is None:
                msg = 'Collection identifier required'
                LOGGER.error(msg)
                raise ProcessorExecuteError(msg)
        else:
            LOGGER.debug('Setting collection from target.collection')
            content['collection'] = collection

    if (target['rel'] == TARGET_TYPES['ogcapi-records'] and
            collection is None):
        LOGGER.debug('OGC API - Records mode detected')
        collection = 'metadata:main'

    LOGGER.debug(f'Collection: {collection}')


def validate_json(schema: dict, instance: dict) -> list:
    """
    Helper function to validate JSON against a JSON Schema

    :param schema: `dict` of JSON Schema
    :paran instance: `dict` of request instance

    :returns: `list` of valiation errors
    """

    validation_errors = []
    LOGGER.debug('Validating input against schema')
    validator = Draft202012Validator(schema)

    for error in validator.iter_errors(instance):
        LOGGER.debug(f'{error.json_path}: {error.message}')
        validation_errors.append(f'{error.json_path}: {error.message}')

    return validation_errors
