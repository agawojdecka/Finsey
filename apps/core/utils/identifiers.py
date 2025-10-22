import uuid


def str_uuid() -> str:
    """Generate and return a random UUID4 string."""
    return str(uuid.uuid4())
