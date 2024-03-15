OBJECT_SCHEMA = dict(
    type='object',
    additionalProperties=False,
    required=[
        'file_id',
        'purpose',
        'filename'
    ],
    properties=dict(
        file_id=dict(type='string'),
        filename=dict(type='string'),
        purpose=dict(type='string', enum=['assistants', 'fine-tune'])
    )
)


def format_file(file):
    return dict(
        file_id=file.id,
        purpose=file.purpose,
        filename=file.filename
    )
