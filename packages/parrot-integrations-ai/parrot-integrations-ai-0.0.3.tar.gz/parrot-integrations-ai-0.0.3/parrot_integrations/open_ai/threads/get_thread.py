from parrot_integrations.open_ai.threads import OBJECT_SCHEMA, format_thread


def get_schema():
    return dict(
        name='Get Thread',
        description='Get OpenAI Thread Details',
        is_trigger=False,
        schema=dict(
            type='object',
            additionalProperties=False,
            required=['inputs', 'outputs'],
            properties=dict(
                inputs=dict(
                    type='object',
                    additionalProperties=False,
                    required=['thread_id'],
                    properties=dict(
                        thread_id=dict(type='string')
                    )
                ),
                outputs=OBJECT_SCHEMA
            )
        )
    )


def process(inputs, integration, **kwargs):
    from parrot_integrations.open_ai import get_client
    client = get_client(integration=integration)
    thread = client.beta.threads.retrieve(thread_id=inputs['thread_id'])
    return format_thread(thread=thread)
