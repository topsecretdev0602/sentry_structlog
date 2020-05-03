from django.urls import include, re_path

urlpatterns = [
    # path('admin/', admin.site.urls),
    re_path('^app/', include('app.urls')),
]
