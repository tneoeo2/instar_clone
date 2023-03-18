from django.db import models

# Create your models here.
class Feed(models.Model):
    content = models.TextField()        #글내용
    image = models.TextField()          #image(피드 사진)
    # profile_image = models.TextField()  #프로필 이미지
    # user_id = models.TextField()        #사용자ID   (글쓴이)  
    email = models.EmailField(default='')         #이메일로 저장하여 해당 이메일에서 아이디 닉네임등 끌어다쓰게 변경 -> 변경된 프로필등 반영가능
    

class Like(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')         
    is_like = models.BooleanField(default=True) #좋아요 여부 확인용(취소할때 컬럼삭제 안하고 업데이트 처리할 수 있다)
    

class Reply(models.Model):
    feed_id = models.IntegerField(default=0) #어떤 게시글의 댓글인지    #feed.id와 대응
    email = models.EmailField(default='')   #댓글단 계정 구분용
    reply_content = models.TextField()      #댓글 내용

class Bookmark(models.Model):
    feed_id = models.IntegerField(default=0) #어떤 게시글의 댓글인지
    email = models.EmailField(default='')   #댓글단 계정 구분용
    is_marked = models.BooleanField(default=True)   #북마크 여부
    
    
    