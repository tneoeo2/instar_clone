from django.db import models

# Create your models here.
class Feed(models.Model):
    content = models.TextField()        #글내용
    image = models.TextField()          #image(피드 사진)
    profile_image = models.TextField()  #프로필 이미지
    user_id = models.TextField()        #사용자ID   (글쓴이)
    like_count = models.IntegerField()  #좋아요 수
    

