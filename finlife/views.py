from django.shortcuts import render
from .models import DepositProducts, DepositOptions
from django.http import JsonResponse
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from django.conf import settings 
from .serializers import DepositOptionsSerializer, DepositProductsSerializer
import requests

@api_view(['GET'])
def save_deposit_products(request):
    api_key = settings.API_KEY
    url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'
    response = requests.get(url).json()
    # return Response(response)
    for li in response.get('list'):
        fin_prdt_cd = li.get('fin_prdt_cd')
        kor_co_nm = li.get('kor_co_nm')
        fin_prdt_nm = li.get('fin_prdt_nm')
        etc_note = li.get('etc_note')
        join_deny = li.get('join_deny')
        join_member = li.get('join_member')
        join_way = li.get('join_way')
        spcl_cnd = li.get('spcl_cnd')

        if DepositProducts.objects.filter(fin_prdt_cd=fin_prdt_cd, kor_co_nm=kor_co_nm,fin_prdt_nm=fin_prdt_nm, etc_note=etc_note, join_deny=join_deny, join_member=join_member, join_way=join_way, spcl_cnd=spcl_cnd).exists():
            continue

        save_data = {
            'fin_prdt_cd' : fin_prdt_cd,
            'kor_co_nm' : kor_co_nm,
            'fin_prdt_nm' : fin_prdt_nm,
            'etc_note' : etc_note,
            'join_deny' : join_deny,
            'join_member' : join_member,
            'join_way' : join_way,
            'spcl_cnd' : spcl_cnd,
        }

        serializer = DepositProductsSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            
    return JsonResponse({ 'message' : 'Okay!'})

@api_view(['GET', 'POST'])
def deposit_products(request):
    # api_key = settings.API_KEY
    # url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'
    # response = requests.get(url).json()
    pass 


@api_view(['GET'])
def deposit_product_options(request):
    pass 

@api_view(['GET'])
def top_rate(request):
    pass 
