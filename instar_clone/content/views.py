from django.shortcuts import render
from rest_framework.views import APIView
from .models import Feed


class Main(APIView):
    def get(self, request): 
            feed_list = Feed.objects.all().order_by('-id') #select * from content_feed;
                                                           #order_by('-id') : id 역순으로 데이터 가져오기
            
            # for feed in feed_list:
                # print(feed.content)  #글내용 가져오기
            
            return render(request, 'instar_clone/main.html', context=dict(feeds=feed_list))
            
    