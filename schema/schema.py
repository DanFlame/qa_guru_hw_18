from voluptuous import Schema, PREVENT_EXTRA

user_create_successful_schema = Schema(
    {
        "name": str,
        "job": str,
        "id": str,
        "createdAt": str
    },
    required=True,
    extra=PREVENT_EXTRA
)

user_update_successful_schema = Schema(
    {
        "name": str,
        "job": str,
        "updatedAt": str
    },
    required=True,
    extra=PREVENT_EXTRA
)

user_register_successful_schema = Schema(
    {
        "id": int,
        "token": str
    },
    required=True,
    extra=PREVENT_EXTRA
)

user_register_unsuccessful_schema = Schema(
    {
        "error": str
    },
    required=True,
    extra=PREVENT_EXTRA
)
