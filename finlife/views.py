from django.shortcuts import get_list_or_404, get_object_or_404
from .models import DepositProducts, DepositOptions
from django.http import JsonResponse
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from django.conf import settings 
from .serializers import DepositOptionsSerializer, DepositProductsSerializer, TopRateSerializer
import requests
from .models import DepositOptions, DepositProducts


@api_view(['GET'])
def save_deposit_products(request):
    api_key = settings.API_KEY
    url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'
    response = requests.get(url).json()
    baseLists = response.get('result').get('baseList')
    optionLists = response.get('result').get('optionList')
    # return Response(response)
    for baseList in baseLists:
        fin_prdt_cd = baseList.get('fin_prdt_cd')
        kor_co_nm = baseList.get('kor_co_nm')
        fin_prdt_nm = baseList.get('fin_prdt_nm')
        etc_note = baseList.get('etc_note')
        join_deny = baseList.get('join_deny')
        join_member = baseList.get('join_member')
        join_way = baseList.get('join_way')
        spcl_cnd = baseList.get('spcl_cnd')

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

        # return JsonResponse(save_data)
        serializer = DepositProductsSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    for optionList in optionLists :

        product_cd = optionList.get('fin_prdt_cd')
        product = DepositProducts.objects.get(fin_prdt_cd=product_cd)

        fin_prdt_cd = optionList.get('fin_prdt_cd')
        intr_rate_type_nm = optionList.get('intr_rate_type_nm')
        intr_rate = optionList.get('intr_rate') or -1
        intr_rate2 = optionList.get('intr_rate2')
        save_trm = optionList.get('save_trm')

        if DepositOptions.objects.filter(
            fin_prdt_cd=fin_prdt_cd, 
            intr_rate_type_nm=intr_rate_type_nm, 
            intr_rate=intr_rate, 
            intr_rate2=intr_rate2,
            save_trm=save_trm,
            ).exists():
            continue
    
        save_data = {
        'fin_prdt_cd' : fin_prdt_cd,
        'intr_rate_type_nm' : intr_rate_type_nm,
        'intr_rate' : intr_rate,
        'intr_rate2' : intr_rate2,
        'save_trm' : save_trm,
    }

        # return JsonResponse(save_data)
        serializer = DepositOptionsSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(product=product)
            
    return JsonResponse({ 'message' : 'Okay!'})

@api_view(['GET', 'POST'])
def deposit_products(request):
    if request.method == 'GET' :
        deposits = get_list_or_404(DepositProducts)
        serializer = DepositProductsSerializer(deposits, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST' :
        serializer = DepositProductsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@api_view(['GET'])
def deposit_product_options(request, fin_prdt_cd):
    deposit = get_object_or_404(DepositProducts, fin_prdt_cd=fin_prdt_cd)
    options = deposit.depositoptions_set.all()
    serializer = DepositOptionsSerializer(options, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def top_rate(request):
    top = DepositOptions.objects.all().order_by('-intr_rate2')[0]
    product = top.product

    result = {
        'deposit_product' : DepositProductsSerializer(product).data,
        'options' : DepositOptionsSerializer(product.depositoptions_set.all(), many=True).data,
    }
    return JsonResponse(result)

