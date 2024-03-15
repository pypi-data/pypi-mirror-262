from parrot_integrations.open_ai.messages import OBJECT_SCHEMA, format_message


def get_schema():
    return dict(
        name='Get Thread messages',
        description='Get Thread messages',
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
                        'thread_id'
                    ],
                    properties=dict(
                        thread_id=dict(type='string'),
                        after=dict(type='string'),
                        order=dict(type='string', enum=['asc', 'desc'], default='asc')
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
    return [format_message(message=message) for message in client.beta.threads.messages.list(**inputs)]
