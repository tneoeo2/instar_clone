from django.contrib.auth.models  import AbstractBaseUser
from django.db import migrations,models

# Create your models here.
class User(AbstractBaseUser):
    '''
        유저 프로필 사진
        유저 닉네임        --> 화면에 표기되는 이름
        유저 이름          -->  실제 사용자 이름
        유저 이메일 주소 --> 회원가입시 사용하는 아이디
        유저 비밀번호   --> 디폴트
        
        
    '''
    
    migrations.Migration.atomic = False 
    
    profile_image = models.TextField()      #프로필 이미지
    nickname = models.CharField(max_length=24, unique=True) 
    name = models.CharField(max_length=24)
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'nickname'             #고유 식별자로 지정
    
    class Meta:             #테이블 이름 설정시 사용
        db_table = "User"   
    