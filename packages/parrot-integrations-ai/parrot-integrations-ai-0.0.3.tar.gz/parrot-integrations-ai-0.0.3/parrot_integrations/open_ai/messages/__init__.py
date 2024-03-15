OBJECT_SCHEMA = dict(
    type='object',
    additionalProperties=False,
    required=[
        'content',
        'role',
        'message_id',
        'file_ids',
        'metadata',
        'thread_id'
    ],
    properties=dict(
        thread_id=dict(
            type='string'
        ),
        message_id=dict(
            type='string'
        ),
        content=dict(
            type='array',
            items={
                "type": 'object',
                "required": [
                    'type',
                ],
                "properties": dict(
                    type=dict(
                        type='string',
                        enum=['image_file', 'text']
                    )
                ),
                "allOf": [
                    {
                        "if": {
                            "properties": {
                                "type": {"const": "text"}
                            }
                        },
                        "then": dict(
                            required=[
                                'value',
                                'annotations'
                            ],
                            properties=dict(
                                value=dict(
                                    type='string'
                                ),
                                annotations=dict(
                                    type='array',
                                    minItems=0,
                                    items=dict(
                                        oneOf=[
                                            dict(
                                                type='object',
                                                additionalProperties=False,
                                                required=[
                                                    'text',
                                                    'file_citation',
                                                    'start_index',
                                                    'end_index'
                                                ],
                                                properties=dict(
                                                    type=dict(
                                                        type='string',
                                                        enum=['file_citation']
                                                    ),
                                                    text=dict(type='string'),
                                                    file_citation=dict(
                                                        type='object',
                                                        additionalProperties=False,
                                                        required=[
                                                            'file_id',
                                                            'quote'
                                                        ],
                                                        properties=dict(
                                                            file_id=dict(type='string'),
                                                            quote=dict(type='string')
                                                        )
                                                    ),
                                                    start_index=dict(type='integer'),
                                                    end_index=dict(type='integer')
                                                )
                                            ),
                                            dict(
                                                type='object',
                                                additionalProperties=False,
                                                required=[
                                                    'type',
                                                    'text',
                                                    'file_path',
                                                    'start_index',
                                                    'end_index'
                                                ],
                                                properties=dict(
                                                    type=dict(
                                                        type='string',
                                                        enum=['file_path']
                                                    ),
                                                    text=dict(type='string'),
                                                    file_path=dict(
                                                        type='object',
                                                        required=[
                                                            'file_id'
                                                        ],
                                                        properties=dict(
                                                            file_id=dict(type='string'),
                                                        )
                                                    ),
                                                    start_index=dict(type='integer'),
                                                    end_index=dict(type='integer')
                                                )
                                            )
                                        ]
                                    )
                                )
                            )
                        ),
                    },
                    {
                        "if": {
                            "properties": {
                                "type": {"const": "image_file"}
                            }
                        },
                        "then": dict(
                            required=['image_file'],
                            properties=dict(
                                image_file=dict(
                                    type='object',
                                    required=['file_id'],
                                    additionalProperties=False,
                                    properties=dict(
                                        file_id=dict(
                                            type='string',
                                        )
                                    )
                                ),
                            )
                        )
                    }
                ]

            }
        ),
        role=dict(
            type='string',
            enum=['user', 'assistant']
        ),
        file_ids=dict(
            type='array',
            items=dict(
                type='string'
            )
        ),
        run_id=dict(
            type=['null', 'string']
        ),
        metadata=dict(
            type='object'
        )
    )
)


def format_message(message):
    clean_message = dict(
        message_id=message.id,
        run_id=message.run_id,
        content=[i.model_dump() for i in message.content],
        role=message.role,
        thread_id=message.thread_id,
        file_ids=message.file_ids,
        metadata=message.metadata
    )
    return clean_message
