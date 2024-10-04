# myapp/middleware.py
from django.conf import settings
from django.shortcuts import get_object_or_404, render,redirect,HttpResponse
from django.utils.deprecation import MiddlewareMixin
import requests
from dsaSLN.models import *

from dsaSLN.views import dsamanualId

# class AllowIframeMiddleware(MiddlewareMixin):
#     def process_response(self, request, response):
#         # Allow iframe embedding only for specific paths
#         if request.path.startswith('/allow-iframe/'):
#             response['X-Frame-Options'] = 'ALLOWALL'
#         return response


class AuthMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response
        # self.protected_paths = getattr(settings, 'PROTECTED_PATHS', [])

    def __call__(self, request):
        print(request.path) #dsa/allLoans
        print("Im Middleware")
        
        # response=requests.get(f'{settings.ACCOUNTS_SOURCE_URL}/getclaim/{dsamanualId(request)}')
        # res=None
        # if response.status_code==200:
        #  res=response.json()
        # #  print(res)
        #  com=DSA.objects.get(dsa_registerid=dsamanualId(request))
        #  newCom=com.comission.values('application_id').all()
        # #  print(comisons.values('application_id'))
        # #  newCom=comisons.values('application_id')
        #  print(newCom)
        #  oldrecords=[]
        #  newrecords=[]
         
        #  request.session['newrecord']='exist'
        #  for j in newCom:
        #      oldrecords.append(j.get('application_id'))
        #  print("Old : ",oldrecords)
        #  for i in res:
        #      print(i.get('application_id'))
        #      if i.get('application_id') not in oldrecords:
        #          request.session['newrecord']='notexist'
        #          break
     
        # #  del request.session['newrecord']
     
        #  if len(res)>0:
        #    request.session['recntComiLen']=len(res)
        
       
        
        
        
        if not request.session.get('verified') and request.path=='/dsa/dsaLogin' and request.method!='POST':
            print("1")
            request.session['indexPage']=True
            return render(request,'dsaLogin.html')

        if request.GET.get('id') and request.path.startswith('/dsa/AllLoans'):
            request.session['dsanologin']=True
           
            print(self.get_response(request))
            print("kkkk;p")
            return self.get_response(request)
        elif request.path.startswith('/dsa/api/'):
           return self.get_response(request)
        
       
       
        
        
        if (request.path.startswith('/dsa/') or request.path.startswith('/dsacomisions/')) and not request.session.get('verified') and request.path!='/dsa/dsaLogin':
           print(request.build_absolute_uri())
           request.session['pageurl']=request.build_absolute_uri()
           return render(request,'dsaLogin.html')
        else:
            print("else.....")
            response = self.get_response(request)
            print(request.build_absolute_uri())
            return response