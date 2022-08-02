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
