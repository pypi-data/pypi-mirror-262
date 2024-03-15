OBJECT_SCHEMA = dict(
    type='object',
    additional_properties=False,
    required=[
        'assistant_id',
        'model_id',
        'name',
        'description',
        'file_ids',
        'instructions',
    ],
    properties=dict(
        assistant_id=dict(type='string', readOnly=True),
        model_id=dict(type='string'),
        name=dict(type='string'),
        description=dict(type='string'),
        instructions=dict(type='string'),
        file_ids=dict(
            type='array',
            maxItems=10,
            items=dict(
                type='string'
            )
        )
    )
)


def format_assistant(assistant):
    assistant_dict = dict(
        assistant_id=assistant.id,
        description=assistant.description,
        name=assistant.name,
        model_id=assistant.model,
        instructions=assistant.instructions,
        file_ids=assistant.file_ids
    )
    if assistant.tools is not None:
        assistant_dict['tools'] = [str(i) for i in assistant.tools]
    return assistant_dict