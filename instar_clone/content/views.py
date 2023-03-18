import os
from uuid import uuid4
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User
from .models import Bookmark, Feed, Reply, Like
from instar_clone.settings import MEDIA_ROOT, MEDIA_URL


class Main(APIView):
    def get(self, request): 
            email = request.session.get('email', None)      #없을 시 None 반환
                                                           
            
            if email is None:           #로그인 안된 상태
                return render(request, 'user/login.html')
            
            user = User.objects.filter(email=email).first()     #현재 로그인한 사용자 정보

            if user is None:    #일치하는 회원 없음
                return render(request, 'user/login.html')
        
            feed_object_list = Feed.objects.all().order_by('-id') #select * from content_feed;
                                                           #order_by('-id') : id 역순으로 데이터 가져오기
            feed_list = []
            
            for feed in feed_object_list:
                user = User.objects.filter(email=feed.email).first()        #변경된 데이터 반영하기 위해 이메일로 user데이터 가져온후 프로필, 닉네임 가져옴
                reply_object_list = Reply.objects.filter(feed_id=feed.id)
                reply_list = []
                for reply in reply_object_list:
                    user = User.objects.filter(email=reply.email).first()   # 댓글쓴 사용자 반환
                    reply_list.append(dict(feed_id=reply.feed_id, reply_content = reply.reply_content,
                                           nickname=user.nickname))
                
                like_count = Like.objects.filter(feed_id=feed.id, is_like=True).count()
                #현재 로그인한 사용자가 좋아요를 한 게시물이면 True 아니면 False 반환   
                is_liked = Like.objects.filter(feed_id=feed.id, email=email, is_like=True).exists()
                is_marked = Bookmark.objects.filter(feed_id=feed.id, email=email, is_marked=True).exists()
                feed_list.append(dict(
                                      id=feed.id,
                                      image=feed.image,
                                      content= feed.content,
                                      like_count=like_count,
                                      profile_image = user.profile_image,
                                      nickname = user.nickname,
                                      reply_list = reply_list,
                                      is_liked = is_liked,
                                      is_marked = is_marked,
                                      ))                                                           
                                                           
          
            
            return render(request, 'content/main.html', context=dict(feeds=feed_list, user=user))

class UploadFeed(APIView):
    def post(self, request):
        
        '''
        일반적으로 파일서버, 이미지 서버 따로 둔다
        '''
        print("MEDIA_URL: %s" % MEDIA_URL)
        print("MEDIA_ROOT: %s" % MEDIA_ROOT)
        ##파일 불러오기
        file = request.FILES['file']
        uuid_name = uuid4().hex         #
        save_path=os.path.join(MEDIA_ROOT, uuid_name) ##~/media/uuid../
        with open(save_path, 'wb+') as dest:        #w+: 읽기모드.파일이 없으면 새로 만든다 B:바이너리모드로 파일을 연다
            for chunk in file.chunks(): #chunk 단위로 나누어 파일에 쓴다.
                dest.write(chunk)
        
        image = uuid_name
        content = request.data.get('content')
        email = request.session.get('email',None)           #세션에 이메일 없으면 로그인X 상태 -> 세션에서 이메일 가져온다.
        # user_id = request.data.get('user_id')
        # profile_image = request.data.get('profile_image')
        
        Feed.objects.create(image=image,content=content, email=email)      #create ORM db에 피드 데이터 생성
        
        print("file : ", file) 
        print("image : ", image) 
        
        return Response(status=200) # 200 : 통신 성공

class Profile(APIView):
    def get(self, request):
        
        email = request.session.get('email', None)      #없을 시 None 반환
        
        if email is None:           #로그인 안된 상태
            return render(request, 'user/login.html')
        
        user = User.objects.filter(email=email).first()     #현재 로그인한 사용자 정보

        if user is None:    #일치하는 회원 없음
            return render(request, 'user/login.html')
        
        feed_list = Feed.objects.filter(email=email).all().order_by('-id')  ##내 게시글 리스트
        like_list = list(Like.objects.filter(email=email, is_like=True).values_list('feed_id', flat=True))    #내가 좋아요한 리스트의 feed_id반환
        print("like_list : ", like_list)
        like_feed_list = Feed.objects.filter(id__in=like_list)  #id__in로 지정한값 포함한 값만 검색 id값이 like_list안에서 검색
        
        bookmark_list = list(Bookmark.objects.filter(email=email, is_marked=True).values_list('feed_id', flat=True))
        bookmark_feed_list = Feed.objects.filter(id__in=bookmark_list)
        
    
        return render(request, 'content/profile.html', context=dict(user=user, 
                                                                    feed_list=feed_list,
                                                                    like_feed_list=like_feed_list,
                                                                    bookmark_feed_list=bookmark_feed_list))


class UploadReply(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        reply_content = request.data.get('reply_content', None)
        email = request.session.get('email', None)      ##로그인된 사용자만 댓글기능 사용가능

        Reply.objects.create(feed_id=feed_id, reply_content = reply_content,email=email)
        
        return Response(status=200)
        
class ToggleLike(APIView):          #좋아요 처리함수
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        favorite_text = request.data.get('favorite_text', True)
        
        if favorite_text == 'favorite' :    #좋아요X -> 좋아요O
            is_like = True              
        else:
            is_like = False

        email = request.session.get('email', None)
        
        like = Like.objects.filter(feed_id=feed_id, email=email).first()       #좋아요 기록 있는지 확인
        if like:
            like.is_like = is_like
            like.save()         #업데이트
        else:   #없으면 데이터 생성
            Like.objects.create(feed_id=feed_id, is_like = is_like,email=email)        
        
        return Response(status=200)
        
class ToggleBookmark(APIView):          #좋아요 처리함수
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        bookmark_text = request.data.get('bookmark_text', True)
        
        if bookmark_text == 'bookmark' :    #북마크X -> 북마크O
            is_marked = True              
        else:
            is_marked = False

        email = request.session.get('email', None)
        
        bookmark = Bookmark.objects.filter(feed_id=feed_id, email=email).first()       #좋아요 기록 있는지 확인
        if bookmark:
            bookmark.is_marked = is_marked
            bookmark.save()         #업데이트
        else:   #없으면 데이터 생성
            Bookmark.objects.create(feed_id=feed_id, is_marked = is_marked,email=email)        
        
        return Response(status=200)
        