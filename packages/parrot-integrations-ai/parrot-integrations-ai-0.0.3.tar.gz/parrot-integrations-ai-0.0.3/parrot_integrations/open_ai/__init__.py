def get_integration_schema():
    return dict(
        type='object',
        additionalProperties=False,
        required=['extra_attributes', 'credentials'],
        properties=dict(
            extra_attributes=dict(
                type='object',
                additionalProperties=False,
                properties=dict(
                    organization_id=dict(
                        type='string',
                    )
                )
            ),
            credentials=dict(
                type='object',
                additionalProperties=False,
                required=[
                    'api_key'
                ],
                properties=dict(
                    api_key=dict(
                        type='string',
                    )
                )
            )
        )
    )


def get_client(integration):
    from openai import OpenAI
    api = OpenAI(organization=integration['extra_attributes']['organization_id'],
                 api_key=integration['credentials']['api_key'])
    return api


async def connect(extra_attributes, credentials):
    from openai import AsyncOpenAI
    client = AsyncOpenAI(organization=extra_attributes['organization_id'], api_key=credentials['api_key'])
    await client.models.list()
    return dict()
