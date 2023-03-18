from django.shortcuts import render
from rest_framework.views import APIView

class Sub(APIView):         #class형 뷰 -> dispatch()가 HTTP메소드 종류 확인하여 내부적으로 처리해준다
    def get(self, request): 
        print("get으로 호출")
        return render(request, "instar_clone/main.html")
    
    def post(self, request):
        print("post로 호출")
        return render(request, "instar_clone/main.html")