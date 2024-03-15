from parrot_integrations.open_ai.threads import OBJECT_SCHEMA, format_thread


def get_schema():
    return dict(
        name='Create Thread',
        description='Create an OpenAPI thread',
        is_trigger=False,
        schema=dict(
            type='object',
            additionalProperties=False,
            required=['inputs', 'outputs'],
            properties=dict(
                inputs=dict(
                    type='object',
                    additionalProperties=False,
                    required=['messages'],
                    properties=dict(
                        metadata=dict(
                            type='object'
                        ),
                        messages=dict(
                            type='array',
                            items=dict(
                                type='object',
                                additionalProperties=False,
                                required=[
                                    'content',
                                    'role'
                                ],
                                properties=dict(
                                    content=dict(
                                        type='string'
                                    ),
                                    role=dict(
                                        type='string',
                                        enum=['user']
                                    ),
                                    file_ids=dict(
                                        type='array',
                                        items=dict(
                                            type='string'
                                        )
                                    ),
                                    metadata=dict(
                                        type='object'
                                    )
                                )
                            )
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
    thread = client.beta.threads.create(**inputs)
    return format_thread(thread=thread)
