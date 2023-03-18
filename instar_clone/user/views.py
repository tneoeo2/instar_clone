import os
from uuid import uuid4
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from instar_clone.settings import MEDIA_ROOT, MEDIA_URL

from .models import User
from django.contrib.auth.hashers import make_password


# Create your views here.
class Join(APIView):
    print("Join : 회원가입함수 호출")
    def get(self, request):
        return render(request, "user/join.html")
    
    def post(self, request):
        # TODO 회원가입
        print("Join request.data : ", request.data)
        
        email = request.data.get('email', None)
        nickname = request.data.get('nickname', None)
        name = request.data.get('name', None)
        password = request.data.get('password', None)
        ##회원정보 생성
        '''
            비밀번호 암호화
        '''
        User.objects.create(email=email, 
                            nickname=nickname,
                            name=name,
                            password=make_password(password),
                            profile_image='default_profile.jpg')
        
        return Response(status=200)
    
class Login(APIView):
    def get(self, request):
        return render(request, "user/login.html")
    
    def post(self, request):
        # TODO 로그인
        
        print("Join request.data : ", request.data)
        email = request.data.get("email", None)
        password = request.data.get('password', None)
        
        # user_list = User.object.filter(email = email)   #DB에 email과 일치하는 값 반환(list)
        #email은 중복값이 없으므로 first로 가져와도 된다
        user = User.objects.filter(email = email).first()   #DB에 email과 일치하는 값 반환(하나만 반환)
        
        if user is None:        #?회원없음
            return Response(status=404, data=dict(message="회원정보가 잘못되었습니다."))
        
        if user.check_password(password):
            #TODO 로그인 완료 . 세션 or 쿠키 추가
            
            request.session['email'] = user.email   #? 비밀번호 일치시 -> session을 사용해 user.email(사용자 식별할 수 있는 값)넘김
            return Response(status=200)
        else:
            return Response(status=400, data=dict(message="회원정보가 잘못되었습니다."))
        
class LogOut(APIView):
    def get(self, request):
        request.session.flush()     #세션 정보 삭제
        return render(request, 'user/login.html')


class UploadProfile(APIView):
    def post(self, request):

        ##파일 불러오기
        file = request.FILES['file']
        email = request.data.get('email')
        
        uuid_name = uuid4().hex         #
        save_path=os.path.join(MEDIA_ROOT, uuid_name) ##~/media/uuid../
        with open(save_path, 'wb+') as dest:        #w+: 읽기모드.파일이 없으면 새로 만든다 B:바이너리모드로 파일을 연다
            for chunk in file.chunks(): #chunk 단위로 나누어 파일에 쓴다.
                dest.write(chunk)
        
        profile_image = uuid_name
        email = request.data.get('email')
        
        user = User.objects.filter(email=email).first()    #user  정보 검색
        
        user.profile_image = profile_image
        user.save()             #객체 불러와 수정할 때 사용
        
        return Response(status=200) # 200 : 통신 성공
