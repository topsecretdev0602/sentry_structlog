from django.urls import re_path

import app.views

urlpatterns = [
    re_path(r'^/?$', view=app.views.home, name='app_home'),
]
