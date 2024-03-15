OBJECT_SCHEMA = dict(
    type='object',
    additionalProperties=False,
    required=[
        'thread_id',
        'metadata'
    ],
    properties=dict(
        thread_id=dict(
            type='string'
        ),
        metadata=dict(
            type='object'
        )
    )
)


def format_thread(thread):
    return dict(
        thread_id=thread.id,
        metadata=thread.metadata
    )
