def get_schema():
    return dict(
        name='',
        description='',
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
                        thread_id=dict(
                            type='string'
                        )
                    )
                ),
                outputs=dict(
                    type='object',
                    additionalProperties=True,
                    required=['thread_id', 'deleted'],
                    properties=dict(
                        thread_id=dict(
                            type='string'
                        ),
                        deleted=dict(
                            type='boolean'
                        )
                    )
                ),
            )
        )
    )


def process(inputs, integration, **kwargs):
    from parrot_integrations.open_ai import get_client
    client = get_client(integration=integration)
    resp = client.beta.threads.delete(thread_id=inputs['thread_id'])
    return dict(thread_id=resp.id, deleted=resp.deleted)
