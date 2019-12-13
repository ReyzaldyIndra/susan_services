from django.contrib import admin
from django.urls import include, path
# from django.conf.urls import url, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blackboard.urls')),
    # path('blackboard/', include('blackboard.urls')),
    
    
]
