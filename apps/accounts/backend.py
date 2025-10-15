from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        
        # Try to authenticate with username
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # If not found, try with email
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None
        
        if user and user.check_password(password):
            return user
        return None