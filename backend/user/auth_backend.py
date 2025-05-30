from django.contrib.auth.backends import ModelBackend
from user.models import Passenger

print(">>> EmailAuthBackend загружен")
            
class EmailAuthBackend:
    """
    Аутентифицировать посредством адреса электронной почты.
    """
    def authenticate(self, request, email=None, password=None):
        try:
            user = Passenger.objects.get(email=email)
            if user.check_password(password):
                return user
            return None
        except (Passenger.DoesNotExist, Passenger.MultipleObjectsReturned):
            return None
    def get_user(self, user_id):
        try:
            return Passenger.objects.get(pk=user_id)
        except Passenger.DoesNotExist:
            return None