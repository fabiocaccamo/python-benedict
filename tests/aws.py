from decouple import config


def get_aws_credentials():
    aws_access_key_id = config("AWS_ACCESS_KEY_ID", default=None)
    aws_secret_access_key = config("AWS_SECRET_ACCESS_KEY", default=None)
    return aws_access_key_id, aws_secret_access_key


def get_aws_credentials_options():
    aws_access_key_id, aws_secret_access_key = get_aws_credentials()
    return {
        "aws_access_key_id": aws_access_key_id,
        "aws_secret_access_key": aws_secret_access_key,
    }


def has_aws_credentials():
    aws_access_key_id, aws_secret_access_key = get_aws_credentials()
    return all([aws_access_key_id, aws_secret_access_key])
