from parrot_integrations.open_ai.assistants import OBJECT_SCHEMA, format_assistant


def get_schema():
    return dict(
        name='Create Assistant',
        description='Create an OpenAi Assistant',
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
                        'model_id',
                        'instructions'
                    ],
                    properties=dict(
                        name=dict(
                            type='string'
                        ),
                        description=dict(
                            type="string"
                        ),
                        model_id=dict(
                            type='string'
                        ),
                        file_ids=dict(
                            type='array',
                            items=dict(
                                type='string'
                            )
                        ),
                        instructions=dict(
                            type='string'
                        ),
                        tools=dict(
                            type='array',
                            items=dict(
                                type='string',
                                enum=[
                                    'code_interpreter',
                                    'retrieval'
                                ]
                            )
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
    inputs['model'] = inputs.pop('model_id')
    assistant = client.beta.assistants.create(**inputs)
    return format_assistant(assistant=assistant)
