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
            team = Group.objects.get(groupID=project_teamID)
        except:
            return JsonResponse({'error': 4002, 'msg': "团队不存在"})
        if GroupMember.objects.filter(group=team, user=creator).exists():
            ProjectInfo.objects.create(projectName=project_name, projectTeam=team, projectIntro=project_intro,
                                       projectCreator=creator)
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
            team = Group.objects.get(groupID=project_teamID)
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
        project_name = request.POST.get('projectName')
        try:
            project = ProjectInfo.objects.get(projectName=project_name)
        except:
            return JsonResponse({'error': 4001, 'msg': "项目不存在"})
        if project.projectStatus:
            return JsonResponse({'error': 4001, 'msg': "项目不存在"})
        project_team = project.projectTeam
        project_creator = project.projectCreator
        project_intro = project.projectIntro
        project_create_time = project.projectCreateTime
        user_list = []
        for user_info in GroupMember.objects.filter(group=project_team):
            user = user_info.user
            user_item = {
                'username': user.username,
                'isCreator': user_info.isCreator,
                'isManager': user_info.isManager,
            }
            user_list.append(user_item)
        return JsonResponse({'error': 0, 'msg': "查询成功", 'projectName': project_name,
                             'teamName': project_team.groupName, 'creator': project_creator.username,
                             'projectIntro': project_intro, 'projectCreateTime': project_create_time,
                             'groupMember': user_list})


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
            team = Group.objects.get(groupID=project_teamID)
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
                project.projectName = project_new_name
                project.save()
                return JsonResponse({'error': 0, 'msg': "重命名成功"})
            else:
                return JsonResponse({'error': 4004, 'msg': "非团队成员，无权限重命名"})
        else:
            return JsonResponse({'error': 4005, 'msg': "非本团队项目，无权限重命名"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})
