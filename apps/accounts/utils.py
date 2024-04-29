import os
from uuid import uuid4

"""
Accounts utility (utils.py) functions for the accounts app.
"""


def generate_short_uuid(instance, length=8):
    """
    Recursive function that generates a unique short uuid of a given length.
    """
    short_uuid = str(uuid4()).replace('-', '')[:length].lower()
    instances = instance.__class__.objects.filter(short_uuid=short_uuid)

    if len(instances) > 0:
        short_uuid = generate_short_uuid(length)
    return short_uuid


def upload_to_profile_images(instance, filename):
    if filename:
        return os.path.join('accounts', str(instance.uuid), 'profile-image', filename)
    else:
        return os.path.join('accounts', str(instance.uuid), 'profile-image')
