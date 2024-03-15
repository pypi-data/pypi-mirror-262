from parrot_integrations.open_ai.assistants import OBJECT_SCHEMA, format_assistant


def get_schema():
    return dict(
        name='List Assistants',
        description='List Existing OpenAI assistants',
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
                    )
                ),
                outputs=dict(
                    type='array',
                    items=OBJECT_SCHEMA
                ),
            )
        )
    )


def process(integration, **kwargs):
    from parrot_integrations.open_ai import get_client
    client = get_client(integration=integration)
    return [format_assistant(assistant=i) for i in client.beta.assistants.list()]
