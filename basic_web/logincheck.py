from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from django.utils.deprecation import MiddlewareMixin

class UserLoginCheck(MiddlewareMixin):

    def process_request(self, request):
        path = ['/login/', '/logout/', '/','/favicon.ico'] # 不需要进行登录检测的url

        if request.path not in path:
            
             if not request.user.is_authenticated:
                # return redirect('home')
                print('>> 未登录URL拦截 >>: ', request.path)
                return HttpResponseRedirect('/login/')
                