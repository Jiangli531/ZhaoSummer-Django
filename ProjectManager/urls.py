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
    path('viewAxure/', view_Axure),
    path('confirmAuthority/', confirm_Authority),
    path('viewRecycle/', view_recycle_project),
    path('destroyProject/', destroy_project),
    path('searchProject/', search_project),
    path('OrderProjectByTimeUp/', order_project_by_time_up),
    path('OrderProjectByTimeDown/', order_project_by_time_down),
    path('OrderProjectByNameUp/', order_project_by_name_up),
    path('OrderProjectByNameDown/', order_project_by_name_down),
    path('projectCollect/', collect_project),
    path('projectUncollect/', cancel_collect_project),
    path('viewCollect/', get_collect_project_list),
    path('viewRecentProject/', getRecentProject),
    path('projectClick/', click_project),
    path('projectCopy/', copy_project),
    path('isCollect/', is_collect),
    path('createUML/', create_uml),
    path('saveUML/', uml_save),
    path('renameUML/', rename_uml),
    path('viewUMLList/', view_uml_list),
]
