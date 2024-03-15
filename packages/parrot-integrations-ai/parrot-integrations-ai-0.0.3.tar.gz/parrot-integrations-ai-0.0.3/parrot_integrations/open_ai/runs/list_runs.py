from parrot_integrations.open_ai.runs import OBJECT_SCHEMA, format_run


def get_schema():
    return dict(
        name='List Runs',
        description='List runs for a particular Thread',
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
                    ],
                    properties=dict(
                        thread_id=dict(
                            type='string',
                        ),
                        after=dict(
                            type='string'
                        ),
                        before=dict(
                            type='string'
                        ),
                        order=dict(
                            type='string'
                        )
                    )
                ),
                outputs=dict(
                    type='array',
                    items=OBJECT_SCHEMA
                ),
            )
        )
    )


def process(inputs, integration, **kwargs):
    from parrot_integrations.open_ai import get_client
    client = get_client(integration=integration)
    return [format_run(run=run) for run in client.beta.threads.runs.list(**inputs)]
