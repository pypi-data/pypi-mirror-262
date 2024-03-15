from parrot_integrations.open_ai.assistants import format_assistant, OBJECT_SCHEMA


def get_schema():
    return dict(
        name='Update Assistant',
        description='Update an existing OpenAi assistant',
        is_trigger=False,
        schema=dict(
            type='object',
            additionalProperties=False,
            required=['inputs', 'outputs'],
            properties=dict(
                inputs=dict(
                    type='object',
                    additionalProperties=False,
                    required=['assistant_id'],
                    properties=dict(
                        assistant_id=dict(
                            type='string'
                        ),
                        model_id=dict(type='string'),
                        name=dict(type='string'),
                        description=dict(type='string'),
                        instructions=dict(type='string'),
                        file_ids=dict(
                            type='array',
                            items=dict(
                                type='string'
                            )
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
    if 'model_id' in inputs:
        inputs['model'] = inputs.pop('model_id')
    assistant = client.beta.assistants.update(**inputs)
    return format_assistant(assistant=assistant)
