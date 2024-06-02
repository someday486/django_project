import os, re
from django.shortcuts import render, get_object_or_404, redirect
from review.models import Border, BorderImage
from trips.models import TripDetail, Trip
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage


# Create your views here.

def extract_hashtags(text):
    if text:
    # tripdetail 객체에서 해시태그 내용만 골라낸다
        return re.findall(r'#\w+', text);

def index(request):
    userId=request.user.id
    query=request.GET.get('topic','')
    trips = Trip.objects.all()
    imageList={}  # {trip1 : imgurl1, trip2: imgurl2, ...}
    # 각 trip에 맞는 이미지 리스트
    for trip in trips:
        tripDetails = TripDetail.objects.filter(trip_id=trip.id)
        for detail in tripDetails:
            try:
                imgs=[]
                border=Border.objects.get(trip_detail=detail)
                images=BorderImage.objects.filter(border_id=border.id)
                for img in images:
                    imgs.append(img.image.url)
                imageList[trip.id]=imgs
            except:
                imageList[trip.id]=[]

    if query:
        tripdetails=TripDetail.objects.filter(context__icontains=f'#{query}')
        content={
            'tripdetails':tripdetails,
            'userId':userId,
            'topic':query,
            'imageList':imageList,
        }
    else:
        trips=Trip.objects.all()  # 해시태그로 검색한거 아니면 일정 다 가져오기
        detailList=findTripDetails(trips);
        content={
            'trips':trips,
            'userId':userId,
            'detailList':detailList,
            'imageList':imageList,
        }
    return render(request,'review/index.html',content);

def detail(request, userId):  # tripdetailId를 넘겨줘야 한다.
    userName=request.user.username
    trips = Trip.objects.filter(user_id=userId)
    imageList={}  # {trip1 : imgurl1, trip2: imgurl2, ...}
    for trip in trips:
        tripDetails = TripDetail.objects.filter(trip_id=trip.id)
        for detail in tripDetails:
            try:
                imgs=[]
                border=Border.objects.get(trip_detail=detail)
                images=BorderImage.objects.filter(border_id=border.id)
                for img in images:
                    imgs.append(img.image.url)
                imageList[trip.id]=imgs
            except:
                imageList[trip.id]=[]
  
    
    content = {
        'trips': trips,
        'userId': userId,
        'userName':userName,
        'imageList':imageList,
    }
    return render(request, 'review/detail.html', content)

def findTripDetails(trips):
    detailList={}
    for t in trips:
        tripdetails=TripDetail.objects.filter(trip=t)
        detailList[t]=tripdetails   # trip에 대한 detail 객체들 저장
    return detailList;  # {trip1:tripdetail1 tripdetail2, trip2:....}


# 각 디테일과 일치하는 border 객체 반환
def findBorder(tripdetails, borders):
    borderList = []
    for tripdetail in tripdetails:
        try:
            border = borders.get(trip_detail=tripdetail)
            borderList.append(border)
        except Border.DoesNotExist:
            continue
    return borderList;


# 각 TripDetail에 해당하는 BorderImage URL 정보를 딕셔너리 형태로 반환
def findImage(tripdetails, borderList):
    images = {}
    for b in borderList:
        tripdetail = tripdetails.get(id=b.trip_detail.id) 
        imgs = BorderImage.objects.filter(border=b)  # border에 해당되는 borderImage 객체들만 필터링
        image_urls = [i.image.url for i in imgs]  # 이미지 객체의 URL 리스트 생성
        images[tripdetail.id] = image_urls  # tripdetail ID를 키로 사용하여 딕셔너리에 저장


    return images;

def tripDetail(request,tripId):
    userId=request.user.id
    trip=get_object_or_404(Trip,id=tripId) #tripId 가 동일한 글 불러오기
    tripdetails=TripDetail.objects.filter(trip=trip) # 현재 trip과 같은 객체를 가진 tripdetail들을 가져옴
    borders = Border.objects.filter(trip_detail__in=tripdetails) 
    borderList=findBorder(tripdetails, borders);  # 각 디테일과 일치하는 border 객체반환
    try:
        imageUrls= findImage(tripdetails, borderList);
        content = {
            'trip': trip,
            'tripdetails': tripdetails,
            'imageUrls': imageUrls,
            'borderList': borderList,
            # 'defaultImg_path': settings.DEFAULT_IMAGE_URL,  # 기본 이미지 경로 전달
        }
        print(imageUrls)
        return render(request,'review/tripDetail.html',content);
    except Exception as e:
        content = {
            'trip': trip,
            'tripdetails': tripdetails,
            'borderList': borderList,
            # 'defaultImg_path': settings.DEFAULT_IMAGE_URL,  # 기본 이미지 경로 전달
        }
        return render(request, 'review/tripDetail.html', content)


@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        try:
            trip_id = request.POST['trip_id']
            day = request.POST['day']
            file = request.FILES['file']  # 사용자가 업로드한 파일

            trip = Trip.objects.get(id=trip_id)
            trip_folder = os.path.join(settings.MEDIA_ROOT, str(trip_id))
            day_folder = os.path.join(trip_folder, f'day_{day}')
            os.makedirs(day_folder, exist_ok=True)  # 경로가 존재하지 않으면 새로운 폴더 생성

            file_path = os.path.join(day_folder, file.name)  # 파일 저장 경로 생성
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():  # 파일을 작은 조각으로 나누어 씀
                    destination.write(chunk)

            return JsonResponse({'status': 'success', 'file_path': file_path})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


def add(request, tripdetailId):
    tripdetail = get_object_or_404(TripDetail, id=tripdetailId)
    now = datetime.now()
    tripId = tripdetail.trip.id
    defaultImg_path = os.path.join(settings.MEDIA_URL, 'images', 'dog.jpg')

    is_owner = request.user == tripdetail.trip.user

    if request.method == "POST" and is_owner:
        # 기존 Border 객체를 가져오거나 없으면 새로 생성합니다.
        border, created = Border.objects.get_or_create(
            trip_detail=tripdetail,
            defaults={
                '제목': request.POST.get('title', ''),
                '작성일': now,
                '조회수': 0,
            }
        )
        
        # 만약 기존 Border 객체가 있다면 제목과 작성일을 업데이트합니다.
        if not created:
            border.제목 = request.POST.get('title', '')
            border.작성일 = now
            border.save()

        # tripdetail의 내용을 업데이트합니다.
        tripdetail.context = request.POST.get('form_context', '')
        tripdetail.save()

        # 이미지 파일이 존재하는 경우 BorderImage 객체를 생성합니다.
        images = request.FILES.getlist('images')
        if images:
            folder_path = os.path.join(settings.MEDIA_ROOT, 'images', str(tripdetail.id))
            os.makedirs(folder_path, exist_ok=True)  # 폴더가 존재하지 않으면 생성

            for image in images:
                image_path = os.path.join(folder_path, image.name)
                with open(image_path, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)
                BorderImage.objects.create(border=border, image=os.path.join('images', str(tripdetail.id), image.name))

        return redirect(f'/review/tripDetail/{tripId}/')

    # GET 요청 처리 또는 사용자가 소유자가 아닌 경우
    try:
        border = Border.objects.get(trip_detail=tripdetail)
    except Border.DoesNotExist:
        border = None

    if border:
        border_images = BorderImage.objects.filter(border=border)
        image_urls = [i.image.url for i in border_images]  # 이미지 객체의 URL 리스트 생성
    else:
        border_images = []
        image_urls = []

    content = {
        'border': border,
        'borderImages': border_images,  # border 이미지 객체 반환 쿼리셋
        'tripdetail': tripdetail,
        'now': now,
        'tripId': tripId,
        'userCheck': is_owner,
        'image_urls': image_urls,
    }
    return render(request, 'review/add.html', content)





    

    
     




