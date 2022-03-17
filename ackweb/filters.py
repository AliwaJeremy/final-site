import django_filters
from django.contrib.auth import get_user_model


User = get_user_model()

class AccountFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['first_name' , 'last_name' , 'email' , 'mobile_number']