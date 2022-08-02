import datetime

from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from Login.models import UserInfo
from TeamManager.models import *
from ZhaoSummer_Django.settings import EMAIL_FROM
from utils.send import *


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
        GroupMember.objects.create(group=new_group, user=creator, isCreator=True, isManager=True)
        return JsonResponse({'error': 0, 'msg': "团队创建成功"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt
def add_member(request):
    if request.method == 'POST':
        hostID = request.POST.get('hostID')  # 邀请人ID
        username = request.POST.get('username')
        groupID = request.POST.get('groupID')

        try:
            host = UserInfo.objects.get(userID=hostID)
            user = UserInfo.objects.get(username=username)
        except:
            return JsonResponse({'error': 4001, 'msg': "用户不存在"})
        try:
            group = Group.objects.get(groupId=groupID)
        except:
            return JsonResponse({'error': 4002, 'msg': '团队不存在'})

        if not GroupMember.objects.get(group=group, user=host).isManager:
            return JsonResponse({'error': 4003, 'msg': '无管理员权限！'})

        new_member = GroupMember()
        new_member.group = group
        new_member.user = user
        new_member.save()
        group.memberNum += 1
        group.save()
        # 发送通知邮件
        note_email = user.useremail
        email_title = "团队邀请通知--《墨书》开发平台"
        email_body = "Hello!这里是《墨书》开发平台，用户：{0} 正在邀请你加入他的团队！\n团队名称：{0}".format(host.username, group.groupName)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [note_email])
        if send_status:
            return JsonResponse({'error': 0, 'msg': '添加成员成功，已邮件通知'})
        else:
            return JsonResponse({'error': 4001, 'msg': '邮件发送失败'})


    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


@csrf_exempt
def delete_member(request):
    if request.method == 'POST':
        hostID = request.POST.get('hostID')  # 操作者ID
        userID = request.POST.get('userID')  # 被删除者ID
        groupID = request.POST.get('groupID')

        try:
            host = UserInfo.objects.filter(userID=hostID)
            user = UserInfo.objects.filter(userID=userID)
        except:
            return JsonResponse({'error': 4001, 'msg': "用户不存在"})
        try:
            group = Group.objects.get(groupId=groupID)
        except:
            return JsonResponse({'error': 4002, 'msg': '团队不存在'})

        try:
            groupHost = GroupMember.objects.get(group=group, user=host)
            groupUser = GroupMember.objects.get(group=group, user=user)
        except:
            return JsonResponse({'error': 4003, 'msg': '团队无操作者记录'})

        if groupHost.isCreator or not groupUser.isManager:
            # 删除
            groupUser.delete()
            group.memberNum -= 1
            group.save()
            return JsonResponse({'error': 0, 'msg': '删除成功！'})
        else:
            return JsonResponse({'error': 4004, 'msg': '你没有删除权限！'})
    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


@csrf_exempt
def add_manager(request):
    if request.method == 'POST':
        hostID = request.POST.get('hostID')  # 操作者ID
        userID = request.POST.get('userID')  # 被操作者ID
        groupID = request.POST.get('groupID')

        try:
            host = UserInfo.objects.filter(userID=hostID)
            user = UserInfo.objects.filter(userID=userID)
        except:
            return JsonResponse({'error': 4001, 'msg': "用户不存在"})
        try:
            group = Group.objects.filter(groupId=groupID)
        except:
            return JsonResponse({'error': 4002, 'msg': '团队不存在'})

        try:
            groupHost = GroupMember.objects.get(group=group, user=host)
            groupUser = GroupMember.objects.get(group=group, user=user)
        except:
            return JsonResponse({'error': 4003, 'msg': '团队无操作者记录'})

        if groupHost.isCreator:
            if groupUser.isManager:
                return JsonResponse({'error': 4005, 'msg': '该成员已经是管理员！'})
            else:
                # 添加管理员
                groupUser.isManager = True
                groupUser.save()
                return JsonResponse({'error': 0, 'msg': '添加管理员成功！'})
        else:
            return JsonResponse({'error': 4004, 'msg': '你没有操作权限！'})
    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})

@csrf_exempt
def delete_manger(request):
    if request.method == 'POST':
        hostID = request.POST.get('hostID')  # 操作者ID
        userID = request.POST.get('userID')  # 被操作者ID
        groupID = request.POST.get('groupID')

        try:
            host = UserInfo.objects.filter(userID=hostID)
            user = UserInfo.objects.filter(userID=userID)
        except:
            return JsonResponse({'error': 4001, 'msg': "用户不存在"})
        try:
            group = Group.objects.filter(groupId=groupID)
        except:
            return JsonResponse({'error': 4002, 'msg': '团队不存在'})

        try:
            groupHost = GroupMember.objects.get(group=group, user=host)
            groupUser = GroupMember.objects.get(group=group, user=user)
        except:
            return JsonResponse({'error': 4003, 'msg': '团队无操作者记录'})

        if groupHost.isCreator:
            if not groupUser.isManager:
                return JsonResponse({'error': 4005, 'msg': '该成员不是管理员！'})
            else:
                # 删除管理员
                groupUser.isManager = False
                groupUser.save()
                return JsonResponse({'error': 0, 'msg': '撤销管理员成功！'})
        else:
            return JsonResponse({'error': 4004, 'msg': '你没有操作权限！'})
    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


@csrf_exempt
def get_member_info(request):
    if request.method == 'POST':
        groupID = request.POST.get('groupID')

        try:
            group = Group.objects.get(groupId=groupID)
        except:
            return JsonResponse({'error': 4001, 'msg': '团队不存在!'})

        member_list = []
        for groupMember in GroupMember.objects.filter(group=group):
            member = groupMember.user
            member_item = {
                'username': member.username,
                'realName': member.realName,
                'useremail': member.useremail,
                'isManager': groupMember.isManager,
                'isCreator': groupMember.isCreator,
            }
            member_list.append(member_item)
        return JsonResponse({'error': 0, 'member_list': member_list})
    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})
