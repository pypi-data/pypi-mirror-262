from parrot_integrations.open_ai.files import format_file, OBJECT_SCHEMA


def get_schema():
    return dict(
        name='Get File',
        description='Get File from OpenAI',
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
                        'file_id'
                    ],
                    properties=dict(
                        file_id=dict(
                            type='string'
                        )
                    )
                ),
                outputs=OBJECT_SCHEMA
            )
        )
    )


def process(inputs, integration, **kwargs):
    from parrot_integrations.open_ai import get_client
    client = get_client(integration=integration)
    file = client.files.retrieve(file_id=inputs['file_id'])
    return format_file(file=file)
