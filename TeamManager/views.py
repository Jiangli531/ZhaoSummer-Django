import datetime

from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from Login.models import UserInfo
from ProjectManager.models import ProjectInfo
from TeamManager.models import *
from ZhaoSummer_Django.settings import EMAIL_FROM
from utils.send import *
from email.mime.text import MIMEText

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
        return JsonResponse({'error': 0, 'msg': "团队创建成功", 'groupID': new_group.groupId})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt
def add_member(request):
    if request.method == 'POST':
        hostID = request.POST.get('hostID')  # 邀请人ID
        username = request.POST.get('inviteName')
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

        if GroupMember.objects.filter(group=group, user=user).exists():
            return JsonResponse({'error': 4004, 'msg': '该用户已在团队中！'})
        new_member = GroupMember()
        new_member.group = group
        new_member.user = user
        new_member.save()
        group.memberNum += 1
        group.save()
        # 发送通知邮件
        note_email = user.useremail
        email_title = "团队邀请通知--《墨书》开发平台"

        email_body = """

            <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>

<body>
    <meta charset="utf-8">
    <table width="100%">
        <tr>
            <td style="width: 100%;">
                <center>
                    <table class="content-wrap" style="margin: 0px auto; width: 600px;">
                        <tr>
                            <td
                                style="margin: 0px auto; overflow: hidden; padding: 0px; border: 0px dotted rgb(238, 238, 238);">
                                <!---->
                                <div class="full" tindex="1" style="margin: 0px auto; max-width: 600px;">
                                    <table align="center" border="0" cellpadding="0" cellspacing="0" class="fullTable"
                                        style="width: 600px;">
                                        <tbody>
                                            <tr>
                                                <td class="fullTd"
                                                    style="direction: ltr; width: 600px; font-size: 0px; padding-bottom: 0px; text-align: center; vertical-align: top;">
                                                    <div
                                                        style="display: inline-block; vertical-align: top; width: 100%;">
                                                        <table border="0" cellpadding="0" cellspacing="0" width="100%"
                                                            style="vertical-align: top;">
                                                            <tr>
                                                                <td
                                                                    style="font-size: 0px; word-break: break-word; background-color: rgb(255, 255, 255); width: 278px; text-align: center; padding: 22px 161px;">
                                                                    <div><a href="https://voyorshop.com"
                                                                            style="font-size: 0px;"><img height="auto"
                                                                                alt="拖拽生成HTML邮件-拉易网-9" width="278"
                                                                                src="https://www.drageasy.com/75ae44e9862e5e69c1690395093747af.jpg?imageslim"
                                                                                style="box-sizing: border-box; border: 0px; display: inline-block; outline: none; text-decoration: none; height: auto; max-width: 100%; padding: 0px;"></a>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </div>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                                <div class="full" tindex="2" style="margin: 0px auto; max-width: 600px;">
                                    <table align="center" border="0" cellpadding="0" cellspacing="0" class="fullTable"
                                        style="width: 600px;">
                                        <tbody>
                                            <tr>
                                                <td class="fullTd"
                                                    style="direction: ltr; width: 600px; font-size: 0px; padding-bottom: 0px; text-align: center; vertical-align: top; background-color: rgb(255, 255, 255); background-image: url(&quot;&quot;); background-repeat: no-repeat; background-size: 100px; background-position: 10% 50%;">
                                                    <table border="0" cellpadding="0" cellspacing="0" width="100%"
                                                        style="vertical-align: top;">
                                                        <tr>
                                                            <td align="left" style="font-size: 0px; padding: 42px 4px;">
                                                                <div class="text"
                                                                    style="font-family: 微软雅黑, &quot;Microsoft YaHei&quot;; overflow-wrap: break-word; margin: 0px; text-align: center; line-height: 20px; color: rgb(0, 0, 0); font-size: 19px; font-weight: normal;">
                                                                    <div>
                                                                        <h2
                                                                            style="line-height: 36px; font-size: 1.5em; font-weight: bold; margin: 0px;">
                                                                            团队邀请</h2>
                                                                    </div>
                                                                </div>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                                <div class="full" tindex="3" style="margin: 0px auto; max-width: 600px;">
                                    <table align="center" border="0" cellpadding="0" cellspacing="0" class="fullTable"
                                        style="width: 600px;">
                                        <tbody>
                                            <tr>
                                                <td class="fullTd"
                                                    style="direction: ltr; width: 600px; font-size: 0px; padding-bottom: 0px; text-align: center; vertical-align: top; background-image: url(&quot;&quot;); background-repeat: no-repeat; background-size: 100px; background-position: 10% 50%;">
                                                    <table border="0" cellpadding="0" cellspacing="0" width="100%"
                                                        style="vertical-align: top;">
                                                        <tr>
                                                            <td align="left" style="font-size: 0px; padding: 25px 0px;">
                                                                <div class="text"
                                                                    style="font-family: 微软雅黑, &quot;Microsoft YaHei&quot;; overflow-wrap: break-word; margin: 0px; text-align: center; line-height: 22px; color: rgb(0, 0, 0); font-size: 18px; font-weight: normal;">
                                                                    <div>
                                                                        <h3 class="ql-align-center"
                                                                            style="line-height: 24px; font-size: 1.17em; font-weight: bold; margin: 0px;">
                                                                            Hi, {} 正在邀请你加入他的团队：</h3>
                                                                        <p class="ql-align-center"
                                                                            style="text-size-adjust: none; word-break: break-word; line-height: 22px; font-size: 18px; margin: 0px;">
                                                                            &nbsp;</p>
                                                                        <h3 class="ql-align-center"
                                                                            style="line-height: 24px; font-size: 1.17em; font-weight: bold; margin: 0px;">
                                                                            {}</h3>
                                                                        <p
                                                                            style="text-size-adjust: none; word-break: break-word; line-height: 22px; font-size: 18px; margin: 0px;">
                                                                            &nbsp;</p>
                                                                        <p
                                                                            style="text-size-adjust: none; word-break: break-word; line-height: 22px; font-size: 18px; margin: 0px;">
                                                                            &nbsp;</p>
                                                                        <p
                                                                            style="text-size-adjust: none; word-break: break-word; line-height: 22px; font-size: 18px; margin: 0px;">
                                                                            你可以 <a href="https://43.138.86.76"
                                                                                target="_blank" rel="noopener"
                                                                                style="text-decoration: underline; font-weight: normal;"><strong>点击这里</strong></a>&nbsp;来查看当前的团队信息
                                                                        </p>
                                                                        <h3 class="ql-align-center"
                                                                            style="line-height: 24px; font-size: 1.17em; font-weight: bold; margin: 0px;">
                                                                            &nbsp;</h3>
                                                                    </div>
                                                                </div>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                                <div class="full" tindex="4" style="margin: 0px auto; max-width: 600px;">
                                    <table align="center" border="0" cellpadding="0" cellspacing="0" class="fullTable"
                                        style="width: 600px;">
                                        <tbody>
                                            <tr>
                                                <td class="fullTd"
                                                    style="direction: ltr; width: 600px; font-size: 0px; padding-bottom: 0px; text-align: center; vertical-align: top; background-color: rgb(255, 255, 255); background-image: url(&quot;&quot;); background-repeat: no-repeat; background-size: 100px; background-position: 10% 50%;">
                                                    <table border="0" cellpadding="0" cellspacing="0" width="100%"
                                                        style="vertical-align: top;">
                                                        <tr>
                                                            <td align="left" style="font-size: 0px; padding: 20px;">
                                                                <div class="text"
                                                                    style="font-family: 微软雅黑, &quot;Microsoft YaHei&quot;; overflow-wrap: break-word; margin: 0px; text-align: left; line-height: 20px; font-size: 12px; font-weight: normal;">
                                                                    <div>
                                                                        <p
                                                                            style="text-size-adjust: none; word-break: break-word; line-height: 20px; font-size: 12px; margin: 0px;">
                                                                            &nbsp;</p>
                                                                        <p
                                                                            style="text-size-adjust: none; word-break: break-word; line-height: 20px; font-size: 12px; margin: 0px;">
                                                                            ———————————————————————————————————————————
                                                                        </p>
                                                                        <p
                                                                            style="text-size-adjust: none; word-break: break-word; line-height: 20px; font-size: 12px; margin: 0px;">
                                                                            ▶ 这里是《墨书》&nbsp; 一个专注于软&nbsp; 工团队协作与管理平台</p>
                                                                        <p
                                                                            style="text-size-adjust: none; word-break: break-word; line-height: 20px; font-size: 12px; margin: 0px;">
                                                                            坚持为校内外中小团队的项目协作开发提最优质的供管理服务！</p>
                                                                        <p
                                                                            style="text-size-adjust: none; word-break: break-word; line-height: 20px; font-size: 12px; margin: 0px;">
                                                                            感谢你的支持！</p>
                                                                        <p
                                                                            style="text-size-adjust: none; word-break: break-word; line-height: 20px; font-size: 12px; margin: 0px;">
                                                                            &nbsp;</p>
                                                                        <p
                                                                            style="text-size-adjust: none; word-break: break-word; line-height: 20px; font-size: 12px; margin: 0px;">
                                                                            ▶如需了解更多，请访问我们的网站 <a
                                                                                href="https://43.138.86.76"
                                                                                style="text-decoration: none; font-weight: normal;"><span
                                                                                    style="text-decoration: underline;"><span
                                                                                        style="color: #0047b2;">43.138.86.76</span></span></a>
                                                                        </p>
                                                                        <p
                                                                            style="text-size-adjust: none; word-break: break-word; line-height: 20px; font-size: 12px; margin: 0px;">
                                                                            期待与你相遇</p>
                                                                    </div>
                                                                </div>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </td>
                        </tr>
                    </table>
                </center>
            </td>
        </tr>
    </table>
    <!---->
</body>


</html>

            """.format(host.username, group.groupName)
        # email_body = MIMEText(main_content, "html", "utf-8").as_string()
        # email_body = "Hello!这里是《墨书》开发平台，用户：{0} 正在邀请你加入他的团队！\n团队名称：{0}".format(host.username, group.groupName)
        # send_status = send_mail(email_title, email_body, EMAIL_FROM, [note_email],html_message=True)
        send_status = send_email_note(note_email, email_body, email_title)
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
            if groupMember.isCreator:
                level='创建者'
            elif groupMember.isManager:
                level='管理员'
            else:
                level='普通成员'
            member_item = {
                'username': member.username,
                'realName': member.realName,
                'useremail': member.useremail,
                'isManager': groupMember.isManager,
                'isCreator': groupMember.isCreator,
                'level': level,
                'userID': member.userID,
            }
            member_list.append(member_item)
        return JsonResponse({'error': 0, 'member_list': member_list})
    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


@csrf_exempt
def get_group_info(request):
    if request.method == 'POST':
        userID = request.POST.get('userID')

        try:
            user = UserInfo.objects.get(userID=userID)
        except:
            return JsonResponse({'error': 4001, 'msg': "用户不存在"})

        group_list = []

        for groupMember in GroupMember.objects.filter(user=user):
            group = groupMember.group
            group_item = {
                'groupName': group.groupName,
                'groupID': group.groupId,
                'groupMemberNum:': group.memberNum,
                'isCreator': groupMember.isCreator,
                'isManager': groupMember.isManager,
                'groupDescription': group.description,
            }
            group_list.append(group_item)

        return JsonResponse({'error': 0, 'group_list': group_list})

    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})

@csrf_exempt
def group_view_project(request):
    if request.method == 'POST':
        group_id = request.POST.get('groupID')
        try:
            group = Group.objects.get(groupId=group_id)
        except:
            return JsonResponse({'error': 4001, 'msg': "团队不存在"})
        project_list = []
        for project in ProjectInfo.objects.filter(projectTeam=group, projectStatus=False):
            project_team = project.projectTeam
            project_name = project.projectName
            project_id = project.projectID
            project_creator = project.projectCreator
            project_intro = project.projectIntro
            project_create_time = project.projectCreateTime
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
            project_list.append({'projectName': project_name,'projectID': project_id,
                             'teamName': project_team.groupName, 'creator': project_creator.username,
                             'projectIntro': project_intro, 'projectCreateTime': project_create_time,'docNum':project_doc_num,'pageNum':project_page_num,
                             'groupMember': user_list})
        return JsonResponse({'error': 0, 'msg': "查询成功", 'project_list': project_list})

    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})

