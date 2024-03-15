def get_schema():
    return dict(
        name='Delete Assistant',
        description='Delete and OpenAI assistant',
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
                        'assistant_id'
                    ],
                    properties=dict(
                        assistant_id=dict(
                            type='string'
                        )
                    )
                ),
                outputs=dict(
                    type='object',
                    additionalProperties=True,
                    required=['assistant_id', 'deleted'],
                    properties=dict(
                        assistant_id=dict(
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
    resp = client.beta.assistants.delete(assistant_id=inputs['assistant_id'])
    return dict(assistant_id=resp.id, deleted=resp.deleted)
