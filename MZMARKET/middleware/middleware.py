from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from App.models import MZUser

REQUEST_LOGIN_JSON = [
    '/mz/addtocart/',
    "/mz/changecartstate/",
    "/mz/subfromcart/",
    "/mz/allselect/",
]

REQUEST_LOGIN = [
    '/mz/cart/',
]


class LoginMiddleware(MiddlewareMixin):
    '''if request from ajx'''

    def process_request(self, request):
        if request.path in REQUEST_LOGIN_JSON:
            print(request.path)
            user_id = request.session.get('user_id')

            if user_id:
                try:
                    user = MZUser.objects.get(pk=user_id)
                    request.user = user

                except:
                    data = {
                        "status": 302,
                        "msg": "user not available",
                    }
                    return JsonResponse(data=data)
            else:
                data = {
                    "status": 302,
                    "msg": "user not login",
                }
                return JsonResponse(data=data)
        '''if request from html'''
        if request.path in REQUEST_LOGIN:
            user_id = request.session.get('user_id')
            # 如果在session拿到了user_id
            if user_id:
                try:
                    user = MZUser.objects.get(pk=user_id)
                    request.user = user
                # 拿到user_id但是没有匹配到用户
                except:
                    return redirect(reverse('mz:login'))
            # 没有登录session
            else:
                return redirect(reverse('mz:login'))
