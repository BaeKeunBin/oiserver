#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import UserInfo, UserRoom, UserImage, MultiPlayRoom, UserVideo
from django.core.exceptions import ObjectDoesNotExist #db 에 데이터 없음 예외
from django.shortcuts import redirect

from django.views.decorators.csrf import csrf_exempt	# 이하 ajax 사용시 사용됨
from django.http import HttpResponse
from .form import UserImageForm

import json
import string
# Create your views here.

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def index(request):
    if request.method == "POST":
        #userdb = UserInfo.objects.all();
        # form 으로부터 데이터를 얻어온다
        userID = request.POST.get('form_userId')            #구글 페이스북 에서 제공하는 자연수의 배열
        userName = request.POST.get('form_userName')        #사용자의 이름
        userPF = request.POST.get('form_userLoginPlatform') #사용자가 어떤 플랫봄으로 로그인 하였는지 저장
        dest = request.POST.get('form_dest')
        #세션에 사용자의 기본 정보를 저장한다
        request.session['userID'] = userID
        request.session['userName'] = userName
        request.session['userPF'] = userPF
        # UserInfo 객체를 만들어 둔다 
        userQset = UserInfo(userID=userID,userName=userName,userPF=userPF) #닉네임은 디폴트로 들어감
        
        # get 함수로 동일안 아이디가 있는지 얻어와본다
        try:
        	isUser = UserInfo.objects.get(userID=request.POST.get('form_userId'))
        except ObjectDoesNotExist: # 데이터가 없으면 발생하는 exception, (import 해야 사용가능)
        	userQset.save()        # 미리 저장해둔 객체를 저장한다(신규 유저인 경우)
        finally:
            if dest == 'myHome':
                return redirect('scene') # scene 페이지로 보낸다
            else:
                return redirect('VRScene') # vrscene 페이지로 보낸다
        
        #return redirect('scene', username = 'username')
        #                  or
        #return render(request,'oiserver/test.html',{
        #    'userName' : userName,
        #})
    return render(request,'oiserver/index.html',{})


def scene(request):
    userID = request.session['userID']
    planeRoom = UserRoom.objects.get(userID='master')
    nickNameSearch = UserInfo.objects.get(userID = userID)

    request.session['userNick'] = nickNameSearch.userNickName # 닉네임을 세션에 저장한다

    try:
        userQset = UserRoom.objects.get(userID = userID, isProfile = "True")  #유저의 프로필 룸을 얻어온다

    except ObjectDoesNotExist: # 정해둔 프로필룸이 없다면 디폴트 룸으로 로드한다.
        userQset = UserRoom.objects.get(userID='master',isProfile = "True")


    return render(request,'oiserver/test.html',{'nickName':nickNameSearch.userNickName,'profileRoom' : userQset.roomJson,'planeRoom':planeRoom.roomJson , 'myKey':userID})

def socket(request):
    return render(request,'oiserver/socket.io.js',{})
################################################{{이하 ajax}}########################################################
@csrf_exempt
def doSave(request):
    sceneData = request.POST.get('sceneData')       #ajax 를 통해 받아온 데이터
    userID = request.session['userID']              #session 에 저장되어있던 사용자의 id
    roomName = request.POST.get('roomName')
    userNickName = request.session['userNick']

    userQset = UserRoom(userID = userID,roomName = roomName, roomJson= sceneData, isProfile ='False', userNickName = userNickName) #얻어온 데이터로 쿼리셋 생성
    try:
        isUser = UserRoom.objects.get(userID=userID,roomName = roomName) #유저가 설정한 방 이름으로 데이터를 얻어온다
        isUser.roomJson = sceneData
        isUser.save()
    except ObjectDoesNotExist: # 데이터가 없으면 발생하는 exception, import 해야 사용가능
        userQset.save()        # 미리 저장해둔 객체를 저장한다



    context = None	# 서버에서 클라이언트로 보내줄 데이터를 넣는 곳
    return HttpResponse(json.dumps(context), "application/json")


@csrf_exempt
def doLoadSearch(request):  #닉네임을 받아서 해당 유저의 모든 방 이름을 반환하는 함수
    userID = request.session['userID'] #session 에 저장되어있던 사용자의 id
    roomJsonList = []   # 각 행의 방 이름만 받아올 배열

    try:
        userQset = UserRoom.objects.filter(userID = userID)
        userPFRoom = UserRoom.objects.get(userID = userID, isProfile="True")
    except ObjectDoesNotExist:
        userPFRoom = UserRoom(userID = request.session['userID'],roomName = 'default', roomJson= 'default', isProfile ='False');
        #userPFRoom 은 유저의 프로필 룸을 찾아서 알려주기 위함


    for item in userQset:
        roomJsonList.append(item.roomName)  
   
    context = {'roomName':roomJsonList,'PFRoomName': userPFRoom.roomName } # 서버에서 클라이언트로 보내줄 데이터를 넣는 곳
    
    return HttpResponse(json.dumps(context), "application/json")


@csrf_exempt
def doLoad(request):
    userID = request.session['userID']  #session 에 저장되어있던 사용자의 id
    selectedRoomName = request.POST.get('selectedRoomName')           

    userQset = UserRoom.objects.get(userID = userID,roomName=selectedRoomName) # 미리 걸러져온 데이터 이므로예외 없음

   
    context = {'roomdata': userQset.roomJson } # 검색된 json 을 반환
    return HttpResponse(json.dumps(context), "application/json")

@csrf_exempt
def doRename(request):
    userID = request.session['userID']
    newRoomName = request.POST.get('rename')
    oldRoomName = request.POST.get('oldName')


    userQset = UserRoom.objects.get(userID = userID,roomName=oldRoomName)
    userQset.roomName = newRoomName
    userQset.save()

   
    context = {} # 서버에서 클라이언트로 2보내줄 데이터를 넣는 곳
    return HttpResponse(json.dumps(context), "application/json")

@csrf_exempt
def doDelete(request):
    userID = request.session['userID']
    selectedRoomName = request.POST.get('roomName')           #session 에 저장되어있던 사용자의 id

    userQset = UserRoom.objects.get(userID = userID,roomName=selectedRoomName)
    userQset.delete()
   
    context = {} # 서버에서 클라이언트로 2보내줄 데이터를 넣는 곳
    return HttpResponse(json.dumps(context), "application/json")

@csrf_exempt
def doProfile(request):
    userID = request.session['userID']
    selectedRoomName = request.POST.get('roomName')           #session 에 저장되어있던 사용자의 id

    try:
        userQset = UserRoom.objects.get(userID = userID,isProfile="True")
        if userQset.roomName == selectedRoomName:
            userQset.isProfile = "False"
            userQset.save()
            context = {'returndata': 'change' }
        else:
            context = {'returndata': 'false' }

    except ObjectDoesNotExist:
        userQset = UserRoom.objects.get(userID = userID,roomName=selectedRoomName)
        userQset.isProfile = "True"
        userQset.save()
        context = {'returndata': 'success' }
    
    return HttpResponse(json.dumps(context), "application/json")

@csrf_exempt
def doLoadImage(request):

    #file = request.FILES['fileObj']
    userNick = request.session['userNick']

    file = request.FILES.getlist('fileObj')	#클라이언트에서 보내온 파일들의 리스트를 받는방법


    for i in file:							# 반복문을 통해 데이터를 만들고 삽입
        userQset = UserImage(userNickName = userNick, imageData = i)
        userQset.save()

    context = {}
    return HttpResponse(json.dumps(context), "application/json")

@csrf_exempt
def doLoadVideo(request):

    #file = request.FILES['fileObj']
    userNick = request.session['userNick']

    file = request.FILES.getlist('fileObj') #클라이언트에서 보내온 파일들의 리스트를 받는방법


    for i in file:                          # 반복문을 통해 데이터를 만들고 삽입
        i.name = unicode(i.name)
        userQset = UserVideo(userNickName = userNick, videoData = i)
        userQset.save()

    context = {}
    return HttpResponse(json.dumps(context), "application/json")


@csrf_exempt
def doImageSearch(request): #닉네임을 통해서 이미지를 검색한다 

    #file = request.FILES['fileObj']
    userNick = request.POST.get('mynick')

    userQset = UserImage.objects.filter(userNickName = userNick)

    filename =[]
    for i in userQset:
    	filename.append(i.imageData.name)

    context = {"filename" : filename}
    return HttpResponse(json.dumps(context), "application/json")

@csrf_exempt
def doVideoSearch(request): #닉네임을 통해서 이미지를 검색한다 

    #file = request.FILES['fileObj']
    userNick = request.POST.get('mynick')

    userQset = UserVideo.objects.filter(userNickName = userNick)

    filename =[]
    for i in userQset:
        filename.append(i.videoData.name)

    context = {"filename" : filename}
    return HttpResponse(json.dumps(context), "application/json")


@csrf_exempt
def doNicknameSave(request):

    userID = request.session['userID']
    userNickName = request.POST.get('nickname')
    
    try:
        isexistQset = UserInfo.objects.get(userNickName = userNickName) # 닉네임이 존재하는지 검사
        context = {"responseMsg" : "false"} # 존재하면 false 반환
    except ObjectDoesNotExist:
        userQset = UserInfo.objects.get(userID=userID) #없으면 userID 로 검색해서 닉네임을 세팅해준다
        userQset.userNickName = userNickName
        userQset.save()
        request.session['userNick'] = userNickName # 닉네임 저장에 성공한 후 세션에 닉네임을 저장 해 둔다

        context = {"responseMsg" : "success"}
    
    return HttpResponse(json.dumps(context), "application/json")

@csrf_exempt
def doUserRoomSearch(request):
    searchNick = request.POST.get("searchNick") #검색하려하는 유저의 닉네임
    
    searchedRoomList = [] #검색된 방의 이름을 담을 배열
    

    userQset = UserRoom.objects.filter(userNickName = searchNick)
    for item in userQset:
        searchedRoomList.append(item.roomName)

    if len(userQset) == 0:
    	context = {"responseMsg" : "false"} #검색하려는 유저의 방이 없으면 실패 메세지
    else:
    	context = {"searchedRoomList" : searchedRoomList, "responseMsg" : "success"} #검색된 유저의 방 리스트 설정


    return HttpResponse(json.dumps(context), "application/json")

@csrf_exempt
def doSearchLoad(request): #이름과 방 이름을 받아서 해당 방의 데이터를 반환하는 함수 
    searchingName = request.POST.get('searchingName')
    selectedRoomName = request.POST.get('selectedRoomName')

    userQset = UserRoom.objects.get(userNickName = searchingName,roomName=selectedRoomName) # 미리 걸러져온 데이터 이므로예외 없음

    searchNick = UserInfo.objects.get(userNickName = searchingName)
    

    context = {'roomdata': userQset.roomJson,"hostKey":searchNick.userID } # 검색된 json 을 반환
    return HttpResponse(json.dumps(context), "application/json")

@csrf_exempt
def doSearchAllImage(request):
    userNick = request.POST.get('userNick')	# 닉네임을 받아서 그 유저의 방을 모두 검색

    imageList=[]
    userQset = UserImage.objects.filter(userNickName = userNick)

    for i in userQset:
    	imageList.append(i.imageData.image_url.url)
   
    context = {'imageList': imageList } # 검색된 json 을 반환
    return HttpResponse(json.dumps(context), "application/json")

@csrf_exempt
def doInsertMulRoom(request):   #멀티플레이 방 '생성시' 새로운 데이터베이스에 관련 정보를 저장한다. 
    host = request.POST.get('host')
    roomName = request.POST.get('roomName')
    roomJson = request.POST.get('roomJson')

    mulRoomName = str(unicode(host)) + "_" + str(unicode(roomName))

    request.session['hostName'] = host
    request.session['joindeRoomName'] = mulRoomName

    insertData = MultiPlayRoom(host=host,mulRoomName=mulRoomName,roomJson=roomJson)
    insertData.save()

    context = {} # 검색된 json 을 반환
    return HttpResponse(json.dumps(context), "application/json")

@csrf_exempt
def doMulRoomAll(request):   #멀티 플레이 방 모두 출력. 
    room = MultiPlayRoom.objects.all()
    roomName=[]
    host=[]
    peopleNum=[]

    for item in room:
        host.append(item.host)
        roomName.append(item.mulRoomName)
        peopleNum.append(item.NumPeople)

    context = {"mulRoomList" : roomName,"mulRoomHost" : host,"NumOfPeople":peopleNum } 
    return HttpResponse(json.dumps(context), "application/json")

@csrf_exempt
def doMulSearchLoad(request): #멀티 플레이 방 '접속시' 호스트의 닉네임과 방 이름을 받아서 방 데이터를 반환
    searchingName = request.POST.get('searchingName')
    selectedRoomName = request.POST.get('selectedRoomName')

    request.session['hostName'] = searchingName
    request.session['joindeRoomName'] = selectedRoomName


    #선택된 방의 방데이터를 받아온다
    userQset = MultiPlayRoom.objects.get(host = searchingName,mulRoomName=selectedRoomName) # 미리 걸러져온 데이터 이므로예외 없음
    #인원수를 증가시킨다
    userQset.NumPeople +=1
    userQset.save()

    #호스트의 키 값을 받아온다
    searchNick = UserInfo.objects.get(userNickName = searchingName)
    

    context = {'roomdata': userQset.roomJson,"hostKey":searchNick.userID } # 검색된 json 을 반환
    return HttpResponse(json.dumps(context), "application/json")


@csrf_exempt
def doMulFrameUpdate(request): #멀티 플레이 시 호스트가 액자의 사진을 바꿨을 때 멀티 플레이 방 업데이트
    updateRoomJson = request.POST.get('sceneData')
    hostName = request.POST.get('hostName')

    userQset = MultiPlayRoom.objects.get(host = hostName)
    userQset.roomJson = updateRoomJson
    userQset.save()

    context = {}
    return HttpResponse(json.dumps(context), "application/json")



##################################################################test

def test(request):
    return render(request,'oiserver/Mytest.html',{})

##################VR scene
def VRScene(request):
    userQset = UserRoom.objects.get(userID='master',isProfile = "True")
    key = UserInfo.objects.get(userID=request.session['userID'])

    return render(request,'oiserver/VRScene.html',{'defaultRoom' : userQset.roomJson, 'nickName' : key.userNickName, 'myKey' : request.session['userID']})

##### SSL File access
def sslFileFunc(request):
    return render(request,'oiserver/BBokSPJG2C6lE10fqHJlYTJWgq8XXtlxCZ_cGe3MGzo',{})