import json
import uuid

import httpx
import jsf
import pytest
import responses
from parrot_integrations.core.common import list_operations, load_integration_module
from parrot_integrations.core.validation import validate_integration, validate_operation

INTEGRATION_KEY = 'parrot_integrations.open_ai'
OPERATION_KEYS = [[operation_key] for operation_key in list_operations(integration_key=INTEGRATION_KEY)]


def test_valid_integration_schema():
    validate_integration(integration_key=INTEGRATION_KEY)


@pytest.mark.parametrize(['operation_key'], OPERATION_KEYS)
def test_valid_operation_schemas(operation_key):
    validate_operation(integration_key=INTEGRATION_KEY, operation_key=operation_key)


@responses.activate
@pytest.mark.parametrize(['operation_key'], OPERATION_KEYS)
def test_operation(operation_key, respx_mock):
    import jsonschema
    from urllib.parse import urljoin
    base_url = 'https://api.openai.com/v1/"'
    request_url_mapping = {
        'assistant': 'assistants',
        'file': 'files',
        "message": "threads/{thread_id}/messages",
        "run": "threads/{thread_id}/runs",
        "thread": "threads",
    }
    method_mapping = dict(
        get='get',
        list='get',
        delete='delete',
        update='post',
        create='post',
        upload='post'
    )
    method = operation_key.split('.')[-1].split('_')[0]
    object_type = '_'.join(operation_key.split('.')[-1].split('_')[1:])
    if object_type.endswith('s'):
        object_type = object_type[:-1]
    path = request_url_mapping[object_type]
    base_url = urljoin(base_url, path)
    if method in ['get', 'update', 'delete']:
        url = base_url + '/{' + object_type + "_id}"
    else:
        url = base_url

    operation = load_integration_module(integration_key=INTEGRATION_KEY, operation_key=operation_key)
    schema = operation.get_schema()['schema']['properties']
    inputs = jsf.JSF(schema['inputs']).generate()
    integration = dict(
        credentials=dict(api_key='<KEY>'),
        extra_attributes=dict(organization_id='test')
    )
    for k, v in inputs.items():
        if k.endswith('_id'):
            inputs[k] = str(uuid.uuid4())
    resp = generate_open_ai_response(
        object_type=object_type,
        object_schema=schema['outputs'] if not hasattr(operation,'OBJECT_SCHEMA') else operation.OBJECT_SCHEMA
    )
    print(resp)
    if 'file_url' in inputs.keys():
        with open('./tests/mocks/upload.json', 'rb') as f:
            content = f.read()
            responses.add(method=responses.GET, url=inputs['file_url'], body=content, status=200)
    getattr(respx_mock, method_mapping[method])(url=url.format(**inputs)).side_effect = httpx.Response(200, json=resp)
    output = operation.process(inputs=inputs, integration=integration)
    print(json.dumps(output))
    jsonschema.validate(output, schema['outputs'])


def generate_open_ai_response(object_type, object_schema, num_items=1):
    resp = jsf.JSF(object_schema).generate()
    resp = clean_keys(object_type=object_type, resp=resp)
    if num_items > 1:
        resp = dict(
            object='list',
            data=[resp for _ in range(num_items)]
        )
    return resp


def clean_keys(object_type, resp):
    date_keys = []
    for k, v in resp.items():
        if k.endswith('_id'):
            resp[k] = str(uuid.uuid4())
        if k.endswith('_ts'):
            date_keys.append(k)
    for key in date_keys:
        resp[key.replace('_ts', '_at')] = resp.pop(key)
    resp['id'] = resp.pop(f'{object_type}_id')
    if 'model_id' in resp.keys():
        resp['model'] = resp.pop('model_id')
    if object_type == 'message':
        resp['content'] = generate_content()
    return resp

def generate_content():
    return [
        dict(
            type='text',
            value='Hello World!',
            annotations=[]
        ),
        dict(
            type='image_file',
            image_file=dict(file_id='file_id')
        )
    ]