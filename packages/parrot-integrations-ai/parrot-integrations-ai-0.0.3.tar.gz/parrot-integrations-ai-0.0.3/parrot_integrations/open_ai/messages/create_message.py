from parrot_integrations.open_ai.messages import OBJECT_SCHEMA, format_message


def get_schema():
    return dict(
        name='Create Message',
        description='Create Message in Thread',
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
                        'thread_id',
                        'content'
                    ],
                    properties=dict(
                        thread_id=dict(
                            type='string'
                        ),
                        content=dict(
                            type='string'
                        ),
                        file_ids=dict(
                            type='array',
                            items=dict(
                                type="string"
                            )
                        ),
                    )
                ),
                outputs=OBJECT_SCHEMA
            )
        )
    )


def process(inputs, integration, **kwargs):
    from parrot_integrations.open_ai import get_client
    client = get_client(integration=integration)
    message = client.beta.threads.messages.create(
        thread_id=inputs['thread_id'],
        content=inputs['content'],
        file_ids=inputs.get('file_ids'),
        role='user'
    )
    return format_message(message=message)
