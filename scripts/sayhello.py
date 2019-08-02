from django.contrib.auth import get_user_model

def run():
    for u in get_user_model().objects.all():
        print('hi, {}'.format(u))