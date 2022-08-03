from django.http import HttpResponse, JsonResponse
from django.utils.deprecation import MiddlewareMixin
import re

from utils.token import *


class MWare(MiddlewareMixin):

    def process_request(self, request):
        username = request.POST.get('username')
        token = request.POST.get('authorization')
        url = request.path_info
        # print(url)
        # print(re.findall(r'login/', url))
        # print(re.findall(r'register/', url))
        if re.findall(r'login/', url) or re.findall(r'register/', url):
            return

        if username and token:
            if check_token(username, token):
                return
            else:  # token验证失败
                return JsonResponse({'error': 4002, 'msg': '登陆信息过期，请重新登录'})
        else:
            return JsonResponse({'error': 4001, 'msg': '未携带认证信息！'})
