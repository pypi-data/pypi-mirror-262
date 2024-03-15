from parrot_integrations.open_ai.runs import OBJECT_SCHEMA, format_run


def get_schema():
    return dict(
        name='Run Thread',
        description='Run an OpenAI Thread',
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
                        'assistant_id'
                    ],
                    properties=dict(
                        thread_id=dict(
                            type='string',
                        ),
                        assistant_id=dict(
                            type='string',
                        )
                    )
                ),
                outputs=OBJECT_SCHEMA,
            )
        )
    )


def process(inputs, integration, **kwargs):
    from parrot_integrations.open_ai import get_client
    client = get_client(integration=integration)
    run = client.beta.threads.runs.create(
        **inputs
    )
    return format_run(run=run)
