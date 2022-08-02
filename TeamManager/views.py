import datetime

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from Login.models import UserInfo
from TeamManager.models import *


@csrf_exempt
def group_build(request):
    if request.method == 'POST':
        creatorid = request.POST.get('creatorID')
        group_name = request.POST.get('groupName')
        description = request.POST.get('description')
        try:
            creator = UserInfo.objects.get(userID=creatorid)
        except:
            return JsonResponse({'error': 4001, 'msg': '用户不存在'})
        Group.objects.create(groupName=group_name, creator=creator, description=description)
        new_group = Group.objects.get(groupName=group_name, creator=creator, description=description)
        GroupMember.objects.create(group=new_group, user=creator, isCreator=True)
        return JsonResponse({'error': 0, 'msg': "团队创建成功"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt
def add_member(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        groupid = request.POST.get('groupID')

        try:
            user = UserInfo.objects.filter(username=username)
        except:
            return JsonResponse({'error': 2001, 'msg': "用户不存在"})
        try:
            group = Group.objects.filter(groupId=groupid)
        except:
            return JsonResponse({'error': 2002, 'msg': '团队不存在'})

        new_member = GroupMember()
        new_member.group = group
        new_member.user = user
        new_member.joinTime = datetime.time()
        new_member.save()
        return JsonResponse({'error': 0, 'msg': '添加成功'})