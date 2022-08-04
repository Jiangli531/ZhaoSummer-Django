# publish/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    # path('url_name', api_name)
    # 这是一个样例，指定路由名为url_name，对应处理函数为当前app内views.py中的api_name
    path('projectCreate/', create_project),
    path('projectDelete/', delete_project),
    path('projectView/', view_project),
    path('projectRename/', rename_project),
    path('axureCreate/', create_page),
    path('axureRename/', rename_page),
    path('axureSave/', save_page),
    path('viewAxureList/', view_axure_list),
    path('recoverProject/', recover_project),
    path('destroyProject/', destroy_project),
    # path('checkAxureName/', check_AxureName),
]
