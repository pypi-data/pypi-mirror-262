import requests

from parrot_integrations.open_ai.files import OBJECT_SCHEMA, format_file


def get_schema():
    return dict(
        name='Upload File',
        description='Upload File to OpenAI',
        is_trigger=False,
        schema=dict(
            type='object',
            additionalProperties=False,
            required=['inputs', 'outputs'],
            properties=dict(
                inputs=dict(
                    type='object',
                    additionalProperties=False,
                    required=[
                        'purpose',
                        'file_url'
                    ],
                    properties=dict(
                        file_url=dict(
                            type='string',
                            format='uri'
                        ),
                        purpose=dict(
                            type='string',
                            enum=['assistants',
                                  'fine-tune']
                        )
                    )
                ),
                outputs=OBJECT_SCHEMA
            )
        )
    )


def process(inputs, integration, **kwargs):
    from parrot_integrations.open_ai import get_client
    from tempfile import TemporaryFile
    client = get_client(integration=integration)
    resp = requests.get(inputs['file_url'])
    with TemporaryFile('wb+') as f:
        f.write(resp.content)
        f.seek(0)
        file = client.files.create(
            purpose=inputs['purpose'],
            file=f
        )
    return format_file(file=file)
