from django.urls import include, path
from rest_framework import routers
from . import views, views2
# from django.conf.urls import url, include
# from rest_framework.urlpatterns import format_suffix_patterns
# from .views import GetView


router = routers.DefaultRouter()
router.register(r'question', views.NLPViewSet)
router.register(r'answer', views.AnswerViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('listener/', views.ListenerAPI.as_view(), name='listener'),
    path('ktp/', views2.ListenKTPAPI.as_view(), name='listenKTP'),
    path('ktp/update/', views.UpdateKTPApi.as_view(), name='updateKTP'),
    path('ktp/post/', views.PostKTPApi.as_view(), name='postKTP'),
    path('ner/', views2.ListenNERAPI.as_view(), name='listenNER'),
    path('ktp/avail/', views2.ListenAvailKTPAPI.as_view(), name='listenAvailKTP')
]

# {
#     # path('', views.index, name='index'),
#     url(r'^question/$', GetView.as_view(), name="create"),

# }

# urlpatterns = format_suffix_patterns(urlpatterns)
