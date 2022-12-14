# publish/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    # path('url_name', api_name)
    # 这是一个样例，指定路由名为url_name，对应处理函数为当前app内views.py中的api_name
    path('viewDocList/', viewDocList),
    path('createDocument/', createDocument),
    path('viewDoc/', viewDoc),
    path('modifyDocName/', modifyDocName),
    path('modifyDocContent/', modifyDocContent),
    path('recycleDoc/', recycleDoc),
    path('delRecycleDoc/', delRecycleDoc),
    path('recover/', recover),
    path('viewProjectDocList/', viewProjectDocList),
    path('viewTeamDocList/', viewTeamDocList),


]
