import json

from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from Login.models import UserInfo
from TeamManager.models import *
from ProjectManager.models import *


@csrf_exempt
def create_project(request):
    if request.method == 'POST':
        project_name = request.POST.get('projectName')
        project_teamID = request.POST.get('projectTeamID')
        project_intro = request.POST.get('projectIntro')
        project_creatorID = request.POST.get('projectCreatorID')
        try:
            creator = UserInfo.objects.get(userID=project_creatorID)
        except:
            return JsonResponse({'error': 4001, 'msg': "用户不存在"})
        try:
            team = Group.objects.get(groupId=project_teamID)
        except:
            return JsonResponse({'error': 4002, 'msg': "团队不存在"})
        if ProjectInfo.objects.filter(projectName=project_name, projectTeam=team).exists():
            return JsonResponse({'error': 4004, 'msg': '项目名称重复啦！'})
        # print(project_name)
        # print(project_intro)
        # print(project_teamID)
        # print(project_creatorID)
        if GroupMember.objects.filter(group=team, user=creator).exists():
            new_project = ProjectInfo()
            new_project.projectName = project_name
            new_project.projectCreator = creator
            new_project.projectTeam = team
            new_project.projectIntro = project_intro
            new_project.save()
            return JsonResponse({'error': 0, 'msg': "项目创建成功"})
        else:
            return JsonResponse({'error': 4003, 'msg': "非团队成员无权限操作"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt
def delete_project(request):
    if request.method == 'POST':
        project_name = request.POST.get('projectName')
        project_teamID = request.POST.get('projectTeamID')
        project_userID = request.POST.get('projectUserID')
        try:
            user = UserInfo.objects.get(userID=project_userID)
        except:
            return JsonResponse({'error': 4001, 'msg': "用户不存在"})
        try:
            team = Group.objects.get(groupId=project_teamID)
        except:
            return JsonResponse({'error': 4002, 'msg': "团队不存在"})
        try:
            project = ProjectInfo.objects.get(projectName=project_name)
        except:
            return JsonResponse({'error': 4003, 'msg': "项目不存在"})
        if project.projectStatus:
            return JsonResponse({'error': 4003, 'msg': "项目不存在"})
        if ProjectInfo.objects.filter(projectName=project_name, projectTeam=team).exists():
            if GroupMember.objects.filter(group=team, user=user).exists():
                project.projectStatus = True
                project.save()
                return JsonResponse({'error': 0, 'msg': "删除成功"})
            else:
                return JsonResponse({'error': 4004, 'msg': "非团队成员，无权限删除"})
        else:
            return JsonResponse({'error': 4005, 'msg': "非本团队项目，无权限删除"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt
def view_project(request):
    if request.method == 'POST':
        projectID = request.POST.get('projectID')
        try:
            project = ProjectInfo.objects.get(projectID=projectID)
        except:
            return JsonResponse({'error': 4001, 'msg': "项目不存在"})
        if project.projectStatus:
            return JsonResponse({'error': 4001, 'msg': "项目不存在"})
        project_name = project.projectName
        project_team = project.projectTeam
        project_id = project.projectID
        project_creator = project.projectCreator
        project_intro = project.projectIntro
        project_create_time = project.projectCreateTime
        project_doc_num=project.docNum
        project_page_num=project.pageNum
        user_list = []
        for user_info in GroupMember.objects.filter(group=project_team):

            user = user_info.user
            user_item = {
                'username': user.username,
                'isCreator': user_info.isCreator,
                'isManager': user_info.isManager,
            }
            user_list.append(user_item)
        return JsonResponse({'error': 0, 'msg': "查询成功", 'projectName': project_name,'projectID':project_id,
                             'teamName': project_team.groupName, 'creator': project_creator.username,
                             'projectIntro': project_intro, 'projectCreateTime': project_create_time,'docNum':project_doc_num,'pageNum':project_page_num,
                             'groupMember': user_list})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt
def rename_project(request):
    if request.method == 'POST':
        project_name = request.POST.get('projectName')
        project_teamID = request.POST.get('projectTeamID')
        project_userID = request.POST.get('projectUserID')
        project_new_name = request.POST.get('projectNewName')
        try:
            user = UserInfo.objects.get(userID=project_userID)
        except:
            return JsonResponse({'error': 4001, 'msg': "用户不存在"})
        try:
            team = Group.objects.get(groupId=project_teamID)
        except:
            return JsonResponse({'error': 4002, 'msg': "团队不存在"})
        try:
            project = ProjectInfo.objects.get(projectName=project_name)
        except:
            return JsonResponse({'error': 4003, 'msg': "项目不存在"})
        if project.projectStatus:
            return JsonResponse({'error': 4003, 'msg': "项目不存在"})
        if ProjectInfo.objects.filter(projectName=project_name, projectTeam=team).exists():
            if GroupMember.objects.filter(group=team, user=user).exists():
                if ProjectInfo.objects.filter(projectName=project_new_name, projectTeam=team).exists():
                    return JsonResponse({'error': 4006, 'msg': "项目名称重复！"})
                project.projectName = project_new_name
                project.save()
                return JsonResponse({'error': 0, 'msg': "重命名成功"})
            else:
                return JsonResponse({'error': 4004, 'msg': "非团队成员，无权限重命名"})
        else:
            return JsonResponse({'error': 4005, 'msg': "非本团队项目，无权限重命名"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt
def create_page(request):
    if request.method == 'POST':
        userid=request.POST.get('userID')
        projectid=request.POST.get('projectID')
        axureName=request.POST.get('axureName')
        try:
            user = UserInfo.objects.get(userID=userid)
        except:
            return JsonResponse({'error': 4001, 'msg': "用户不存在"})
        try:
            project = ProjectInfo.objects.get(projectID=projectid)
        except:
            return JsonResponse({'error': 4002, 'msg': "项目不存在"})
        if project.projectStatus:
            return JsonResponse({'error': 4002, 'msg': "项目不存在"})
        if PageInfo.objects.filter(pageName=axureName, pageProject=project,pageCreator=user).exists():
            return JsonResponse({'error': 4003, 'msg': "页面已存在"})
        page=PageInfo(pageName=axureName,pageProject=project, pageCreator=user)
        page.save()
        project.pageNum += 1
        project.save()
        return JsonResponse({'error': 0, 'msg': "创建成功", 'pageID': page.pageID})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt
def save_page(request):
    if request.method == 'POST':
        axureID=request.POST.get('axureID')
        axureData=request.POST.get('axureData')

        try:
            page=PageInfo.objects.get(pageID=axureID)
        except:
            return JsonResponse({'error': 4001, 'msg': "原型不存在"})

        page.pageContent=axureData
        page.save()
        return JsonResponse({'error': 0, 'msg': "保存成功"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt
def rename_page(request):
    if request.method == 'POST':
        pageID=request.POST.get('axureID')
        pageName=request.POST.get('axureName')
        page=PageInfo.objects.filter(pageID=pageID)
        if page:
            page.pageName=pageName
            page.save()
            return JsonResponse({'error': 0, 'msg': "重命名成功"})
        else:
            return JsonResponse({'error': 4003, 'msg': "页面不存在"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt
def view_axure_list(request):
    if request.method == 'POST':
        project_id = request.POST.get('projectID')
        try:
            project = ProjectInfo.objects.get(projectID=project_id)
        except:
            return JsonResponse({'error': 4001, 'msg': "项目不存在"})
        axure_list = []
        for axure in PageInfo.objects.filter(pageProject=project):
            axure_item = {
                'axureID': axure.pageID,
                'axureName': axure.pageName,
                'creatorID': axure.pageCreator.userID,

            }
            axure_list.append(axure_item)
        if not axure_list:
            return JsonResponse({'error': 4002, 'msg': '项目暂无原型信息'})
        return JsonResponse({'error': 0, 'msg': "查询成功", 'axure_list': axure_list})

    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt
def recover_project(request):
    if request.method == 'POST':
        project_ID = request.POST.get('projectID')
        project_teamID = request.POST.get('projectTeamID')
        project_userID = request.POST.get('projectUserID')
        try:
            user = UserInfo.objects.get(userID=project_userID)
        except:
            return JsonResponse({'error': 4001, 'msg': "用户不存在"})
        try:
            team = Group.objects.get(groupId=project_teamID)
        except:
            return JsonResponse({'error': 4002, 'msg': "团队不存在"})
        try:
            project = ProjectInfo.objects.get(projectID=project_ID, projectStatus=True)
        except:
            return JsonResponse({'error': 4003, 'msg': "项目不存在"})

        if ProjectInfo.objects.filter(projectID=project_ID, projectTeam=team).exists():
            if GroupMember.objects.filter(group=team, user=user).exists():
                if ProjectInfo.objects.get(projectID=project_ID, projectTeam=team).projectStatus:
                    project.projectStatus = False
                    project.save()
                    return JsonResponse({'error': 0, 'msg': "回收成功"})
                else:
                    return JsonResponse({'error': 4006, 'msg': "该项目不在回收站中"})
            else:
                return JsonResponse({'error': 4004, 'msg': "非团队成员，无权限回收"})
        else:
            return JsonResponse({'error': 4005, 'msg': "非本团队项目，无权限回收"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


#  永久删除回收站项目
@csrf_exempt
def destroy_project(request):
    if request.method == 'POST':
        project_ID = request.POST.get('projectID')
        project_teamID = request.POST.get('projectTeamID')
        project_userID = request.POST.get('projectUserID')
        try:
            user = UserInfo.objects.get(userID=project_userID)
        except:
            return JsonResponse({'error': 4001, 'msg': "用户不存在"})
        try:
            team = Group.objects.get(groupId=project_teamID)
        except:
            return JsonResponse({'error': 4002, 'msg': "团队不存在"})
        try:
            project = ProjectInfo.objects.get(projectID=project_ID)
        except:
            return JsonResponse({'error': 4003, 'msg': "项目不存在"})

        if ProjectInfo.objects.filter(projectID=project_ID, projectTeam=team).exists():
            if GroupMember.objects.filter(group=team, user=user).exists():
                if ProjectInfo.objects.get(projectID=project_ID, projectTeam=team).projectStatus:
                    project.delete()
                    return JsonResponse({'error': 0, 'msg': "删除成功"})
                else:
                    return JsonResponse({'error': 4006, 'msg': "项目不在回收站中"})
            else:
                return JsonResponse({'error': 4004, 'msg': "非团队成员，无权限删除"})
        else:
            return JsonResponse({'error': 4005, 'msg': "非本团队项目，无权限删除"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt
def view_Axure(request):
    if request.method == 'POST':
        axureID = request.POST.get('axureID')

        try:
            axure = PageInfo.objects.get(pageID=axureID)
        except:
            return JsonResponse({'error': 4001, 'msg': '未查找到原型！'})

        return JsonResponse({
            'error': 0,
            'msg': '查询成功',
            'axureID': axureID,
            'axureName': axure.pageName,
            'creatorID': axure.pageCreator.userID,
            'axureContent': axure.pageContent,
            'axureCreateTime': axure.pageCreateTime,
        })

    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


@csrf_exempt
def confirm_Authority(request):
    if request.method == 'POST':
        projectID = request.POST.get('projectID')
        userID = request.POST.get('userID')

        try:
            project = ProjectInfo.objects.get(projectID=projectID)
        except:
            return JsonResponse({'error': 4001, 'msg': '项目不存在!'})
        try:
            user = UserInfo.objects.get(userID=userID)
        except:
            return JsonResponse({'error': 4002, 'msg': '用户不存在!'})

        authority = False

        # 如果用户在团队中，则对该项目有编辑权限
        if GroupMember.objects.filter(group=project.projectTeam, user=user).exists():
            authority = True

        return JsonResponse({'error': 0, 'msg': '查询成功', 'authority': authority})
    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


@csrf_exempt
def view_recycle_project(request):
    if request.method == 'POST':
        group_id = request.POST.get('groupID')
        try:
            group = Group.objects.get(groupId=group_id)
        except:
            return JsonResponse({'error': 4001, 'msg': "团队不存在"})
        project_list = []
        for project in ProjectInfo.objects.filter(projectTeam=group, projectStatus=True):
            project_team = project.projectTeam
            project_name = project.projectName
            project_id = project.projectID
            project_creator = project.projectCreator
            project_intro = project.projectIntro
            # 日期保留到日
            project_create_time = project.projectCreateTime.strftime('%Y-%m-%d')
            project_doc_num = project.docNum
            project_page_num = project.pageNum
            user_list = []
            for user_info in GroupMember.objects.filter(group=project_team):
                user = user_info.user
                user_item = {
                    'username': user.username,
                    'isCreator': user_info.isCreator,
                    'isManager': user_info.isManager,
                }
                user_list.append(user_item)
            project_list.append({'projectName': project_name, 'projectID': project_id,
                                 'teamName': project_team.groupName, 'creator': project_creator.username,
                                 'projectIntro': project_intro, 'projectCreateTime': project_create_time,
                                 'docNum': project_doc_num, 'pageNum': project_page_num,
                                 'groupMember': user_list})
        return JsonResponse({'error': 0, 'msg': "查询成功", 'project_list': project_list})

    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})

#收藏项目
@csrf_exempt
def collect_project(request):
    if request.method == 'POST':
        project_id = request.POST.get('projectID')
        user_id = request.POST.get('userID')
        group_id = request.POST.get('projectTeamID')
        try:
            project = ProjectInfo.objects.get(projectID=project_id)
        except:
            return JsonResponse({'error': 4001, 'msg': "项目不存在"})
        try:
            user = UserInfo.objects.get(userID=user_id)
        except:
            return JsonResponse({'error': 4002, 'msg': "用户不存在"})
        try:
            group = Group.objects.get(groupId=group_id)
        except:
            return JsonResponse({'error': 4003, 'msg': "团队不存在"})
        #判断用户是否在团队中
        try:
            GroupMember.objects.get(group=group, user=user)
        except:
            return JsonResponse({'error': 4004, 'msg': "非团队成员，无权限操作"})
        #判断是否是本团队项目
        if project.projectTeam != group:
            return JsonResponse({'error': 4005, 'msg': "非本团队项目，无权限操作"})
        if ProjectCollect.objects.filter(project=project, user=user).exists():
            return JsonResponse({'error': 4003, 'msg': "已收藏"})
        else:
            ProjectCollect.objects.create(project=project, user=user, collectTime=datetime.now())
            return JsonResponse({'error': 0, 'msg': "收藏成功"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})
#取消收藏项目
@csrf_exempt
def cancel_collect_project(request):
    if request.method == 'POST':
        project_id = request.POST.get('projectID')
        user_id = request.POST.get('userID')
        group_id = request.POST.get('projectTeamID')
        try:
            project = ProjectInfo.objects.get(projectID=project_id)
        except:
            return JsonResponse({'error': 4001, 'msg': "项目不存在"})
        try:
            user = UserInfo.objects.get(userID=user_id)
        except:
            return JsonResponse({'error': 4002, 'msg': "用户不存在"})
        try:
            group = Group.objects.get(groupId=group_id)
        except:
            return JsonResponse({'error': 4003, 'msg': "团队不存在"})
        #判断用户是否在团队中
        try:
            GroupMember.objects.get(group=group, user=user)
        except:
            return JsonResponse({'error': 4004, 'msg': "非团队成员，无权限操作"})
        #判断是否是本团队项目
        if project.projectTeam != group:
            return JsonResponse({'error': 4005, 'msg': "非本团队项目，无权限操作"})
        if ProjectCollect.objects.filter(project=project, user=user).exists():
            ProjectCollect.objects.filter(project=project, user=user).delete()
            return JsonResponse({'error': 0, 'msg': "取消收藏成功"})
        else:
            return JsonResponse({'error': 4003, 'msg': "未收藏"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})
#查询收藏项目列表
@csrf_exempt
def get_collect_project_list(request):
    if request.method == 'POST':
        try:
            user= UserInfo.objects.get(userID=request.POST.get('userID'))
        except:
            return JsonResponse({'error': 4002, 'msg': "用户不存在"})
        project_list = []
        for project in ProjectCollect.objects.filter(user=user):
            project = project.project
            project_name = project.projectName
            project_id = project.projectID
            project_creator = project.projectCreator
            project_intro = project.projectIntro
            # 日期保留到日
            project_create_time = project.projectCreateTime.strftime('%Y-%m-%d')
            project_doc_num = project.docNum
            project_page_num = project.pageNum
            user_list = []
            for user_info in GroupMember.objects.filter(group=project.projectTeam):
                user = user_info.user
                user_item = {
                    'username': user.username,
                    'isCreator': user_info.isCreator,
                    'isManager': user_info.isManager,
                }
                user_list.append(user_item)
            project_list.append({'projectName': project_name, 'projectID': project_id,
                                 'teamName': project.projectTeam.groupName, 'creator': project_creator.username,
                                 'projectIntro': project_intro, 'projectCreateTime': project_create_time,
                                 'docNum': project_doc_num, 'pageNum': project_page_num,
                                 'groupMember': user_list})
        return JsonResponse({'error': 0, 'msg': "查询成功", 'project_list': project_list})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})

@csrf_exempt
def getRecentProject(request):
    if request.method == 'POST':
        user_id=request.POST.get('userID')
        try:
            user=UserInfo.objects.get(userID=user_id)
        except:
            return JsonResponse({'error': 4002, 'msg': "用户不存在"})
        pro_list=[]
        if user_id is not None:
            pro_user_list = ProjectUser.objects.filter(user=user).order_by('-last_watch')
            count = 0
            for c in pro_user_list:
                if count >= 10:
                    break
                project=c.project
                project_name = project.projectName
                project_id = project.projectID
                project_creator = project.projectCreator
                project_intro = project.projectIntro
                # 日期保留到日
                project_create_time = project.projectCreateTime.strftime('%Y-%m-%d')
                project_doc_num = project.docNum
                project_page_num = project.pageNum
                user_list = []
                for user_info in GroupMember.objects.filter(group=project.projectTeam):
                    user = user_info.user
                    user_item = {
                        'username': user.username,
                        'isCreator': user_info.isCreator,
                        'isManager': user_info.isManager,
                    }
                    user_list.append(user_item)
                pro_list.append({'projectName': project_name, 'projectID': project_id,
                                     'teamName': project.projectTeam.groupName, 'creator': project_creator.username,
                                     'projectIntro': project_intro, 'projectCreateTime': project_create_time,
                                     'docNum': project_doc_num, 'pageNum': project_page_num,
                                     'groupMember': user_list})

                count += 1
            return JsonResponse({'errno': 0, 'data': pro_list})
        else:
            return JsonResponse({'errno': 1002, 'msg': "用户未登录"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

@csrf_exempt
def click_project(request):
    if request.method == 'POST':
        user_id = request.POST.get('userID')
        project_id = request.POST.get('projectID')
        try:
            user = UserInfo.objects.get(userID=user_id)
        except:
            return JsonResponse({'error': 4002, 'msg': "用户不存在"})
        try:
            project = ProjectInfo.objects.get(projectID=project_id)
        except:
            return JsonResponse({'error': 4003, 'msg': "项目不存在"})
        ProjectUser.objects.create(project=project, user=user, last_watch=datetime.now())
        return JsonResponse({'error': 0, 'msg': "点击成功"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})
@csrf_exempt
def search_project(request):
    if request.method == 'POST':
        search_key = request.POST.get('key')
        if search_key:
            project_results = ProjectInfo.objects.filter(projectName__icontains=search_key, projectStatus=False)
            if not project_results:
                return JsonResponse({'error': 4001, 'msg': "没有搜索到项目"})
            else:
                project_list = []
                for project in project_results:
                    project_item = {
                        'projectID': project.projectID,
                        'projectName': project.projectName,
                        'projectTeam': project.projectTeam.groupName,
                        'projectIntro': project.projectIntro,
                        'projectCreator': project.projectCreator.username,
                        'projectCreateTime': project.projectCreateTime.strftime('%Y-%m-%d'),
                    }
                    project_list.append(project_item)
                return JsonResponse({'error': 0, 'projectList': json.dumps(project_list, ensure_ascii=False)})
        else:
            return JsonResponse({'error': 4002, 'msg': "搜索内容不能为空"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt
def order_project_by_time_up(request):
    if request.method == 'POST':
        teamID = request.POST.get('teamID')
        try:
            team = Group.objects.get(groupId=teamID)
        except:
            return JsonResponse({'error': 4001, 'msg': "团队不存在"})
        project_list_origin = ProjectInfo.objects.filter(projectTeam=team, projectStatus=False).order_by('projectCreateTime')
        if project_list_origin:
            #project_list_origin.order_by('projectCreateTime')
            project_list = []
            for project in project_list_origin:
                project_item = {
                    'projectID': project.projectID,
                    'projectName': project.projectName,
                    'projectTeam': project.projectTeam.groupName,
                    'projectIntro': project.projectIntro,
                    'projectCreator': project.projectCreator.username,
                    'projectCreateTime': project.projectCreateTime.strftime('%Y-%m-%d'),
                }
                project_list.append(project_item)
            return JsonResponse({'error': 0, '+projectListOrderByTime': json.dumps(project_list, ensure_ascii=False)})
        else:
            return JsonResponse({'error': 4002, 'msg': "团队无项目"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt
def order_project_by_time_down(request):
    if request.method == 'POST':
        teamID = request.POST.get('teamID')
        try:
            team = Group.objects.get(groupId=teamID)
        except:
            return JsonResponse({'error': 4001, 'msg': "团队不存在"})
        project_list_origin = ProjectInfo.objects.filter(projectTeam=team, projectStatus=False).order_by('-projectCreateTime')
        if project_list_origin:
            #project_list_origin.order_by('-projectCreateTime')
            project_list = []
            for project in project_list_origin:
                project_item = {
                    'projectID': project.projectID,
                    'projectName': project.projectName,
                    'projectTeam': project.projectTeam.groupName,
                    'projectIntro': project.projectIntro,
                    'projectCreator': project.projectCreator.username,
                    'projectCreateTime': project.projectCreateTime.strftime('%Y-%m-%d'),
                }
                project_list.append(project_item)
            return JsonResponse({'error': 0, '-projectListOrderByTime': json.dumps(project_list, ensure_ascii=False)})
        else:
            return JsonResponse({'error': 4002, 'msg': "团队无项目"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt
def order_project_by_name_up(request):
    if request.method == 'POST':
        teamID = request.POST.get('teamID')
        try:
            team = Group.objects.get(groupId=teamID)
        except:
            return JsonResponse({'error': 4001, 'msg': "团队不存在"})
        project_list_origin = ProjectInfo.objects.filter(projectTeam=team, projectStatus=False).order_by('projectName')
        if project_list_origin:
            #project_list_origin.order_by('projectName')
            project_list = []
            for project in project_list_origin:
                project_item = {
                    'projectID': project.projectID,
                    'projectName': project.projectName,
                    'projectTeam': project.projectTeam.groupName,
                    'projectIntro': project.projectIntro,
                    'projectCreator': project.projectCreator.username,
                    'projectCreateTime': project.projectCreateTime.strftime('%Y-%m-%d'),
                }
                project_list.append(project_item)
            return JsonResponse({'error': 0, '+projectListOrderByName': json.dumps(project_list, ensure_ascii=False)})
        else:
            return JsonResponse({'error': 4002, 'msg': "团队无项目"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt
def order_project_by_name_down(request):
    if request.method == 'POST':
        teamID = request.POST.get('teamID')
        try:
            team = Group.objects.get(groupId=teamID)
        except:
            return JsonResponse({'error': 4001, 'msg': "团队不存在"})
        project_list_origin = ProjectInfo.objects.filter(projectTeam=team, projectStatus=False).order_by('-projectName')
        if project_list_origin:
           # project_list_origin.order_by('-projectName')
            project_list = []
            for project in project_list_origin:
                project_item = {
                    'projectID': project.projectID,
                    'projectName': project.projectName,
                    'projectTeam': project.projectTeam.groupName,
                    'projectIntro': project.projectIntro,
                    'projectCreator': project.projectCreator.username,
                    'projectCreateTime': project.projectCreateTime.strftime('%Y-%m-%d'),
                }
                project_list.append(project_item)
            return JsonResponse({'error': 0, '-projectListOrderByName': json.dumps(project_list, ensure_ascii=False)})
        else:
            return JsonResponse({'error': 4002, 'msg': "团队无项目"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})