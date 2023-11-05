# utils.py

from datetime import datetime
from rest_framework_simplejwt.tokens import Token

def custom_payload_handler(user):
    """
    Custom payload handler to include additional user data in the JWT token.
    """
    token = Token(user)
    token['user_id'] = user.id
    token['email'] = user.email
    token['username'] = user.username
    token['exp'] = datetime.utcnow() + token.lifetime

    return token
