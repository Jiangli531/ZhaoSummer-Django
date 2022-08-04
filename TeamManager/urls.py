# publish/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    # path('url_name', api_name)
    # 这是一个样例，指定路由名为url_name，对应处理函数为当前app内views.py中的api_name
    path('groupBuild/', group_build),
    path('addMember/', add_member),
    path('deleteMember/', delete_member),
    path('addManager/', add_manager),
    path('deleteManager/', delete_manger),
    path('getMemberInfo/', get_member_info),
    path('getGroupInfo/', get_group_info),
    path('groupViewProject/', group_view_project),
]
