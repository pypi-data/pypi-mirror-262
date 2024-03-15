from parrot_integrations.open_ai.assistants import OBJECT_SCHEMA, format_assistant


def get_schema():
    return dict(
        name='Get Assistant',
        description='Get existing OpenAI assistant',
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
                            type="string",
                            min_length=1
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
    assistant = client.beta.assistants.retrieve(assistant_id=inputs['assistant_id'])
    return format_assistant(assistant=assistant)
