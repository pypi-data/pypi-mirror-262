from parrot_integrations.open_ai.files import format_file, OBJECT_SCHEMA


def get_schema():
    return dict(
        name='List Files',
        description='List OpenAI Files',
        is_trigger=False,
        schema=dict(
            type='object',
            additionalProperties=False,
            required=['inputs', 'outputs'],
            properties=dict(
                inputs=dict(
                    type='object',
                    additionalProperties=False,
                    required=[],
                    properties=dict(
                        purpose=dict(
                            type='string',
                            enum=[
                                'assistants',
                                'fine-tune'
                            ]
                        )
                    )
                ),
                outputs=dict(
                    type='array',
                    maxItems=25,
                    items=OBJECT_SCHEMA
                ),
            )
        )
    )


def process(inputs, integration, **kwargs):
    from parrot_integrations.open_ai import get_client
    client = get_client(integration=integration)
    return [format_file(file=file) for file in client.files.list(**inputs)]
