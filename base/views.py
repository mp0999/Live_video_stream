from django.shortcuts import render
from django.http import JsonResponse
from agora_token_builder import RtcTokenBuilder
import random
import time

import json
from .models import RoomMember

from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def getToken(request):
    appId = 'ad67858a640b4a3c963d519b2be08604'
    appCertificate = '971a935fd48348ccb5e509d23d74a267'
    channelName = request.GET.get('channel')
    uid = random.randint(1,250)
    expirationTimeInSeconds = 3600 * 24
    currentTimeStamp = time.time()
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1
    
    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse({'token':token, 'uid':uid}, safe=False)

def homy(request):
    return render(request, "base/homy.html")

def room(request):
    return render(request, "base/room.html")

@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    
    member, create = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    return JsonResponse({'name':data['name']}, safe=False)

def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')
    
    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name
    )
    
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member was deleted', safe=False)
