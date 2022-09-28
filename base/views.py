from email import message
import imp
from django.shortcuts import HttpResponse
from django.shortcuts import render,redirect
from .models import Room, Topic, Message
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import HttpResponseRedirect

# Create your views here.
# def home(request):
#     search_ = request.GET.get('search_') if request.GET.get('search_') is not None else ""
#     RoomObj=Room.objects.filter(Q(topic__name__icontains='search_') | Q(name__icontains='search_') | Q(host__username__icontains='search_'))
#     topics = Topic.objects.all()
#     context = {'RoomObj':RoomObj, 'topics':topics}
#     return render(request,'base/index.html',context)


def home(request):
    q = request.GET.get("q") if request.GET.get("q") is not None else ''
    rooms = Room.objects.filter(Q(name__icontains=q) | Q(topic__name=q) | Q(host__username__icontains=q))
    topics = Topic.objects.all()
    room_count = rooms.count()
    # message = Message.objects.filter(
    #     Q(room_name_contains=q) |
    #     Q(body__contains=q)
    # )
    context = {"room": rooms, "topic": topics, "count": room_count}
    return render(request, 'base/index.html', context)




def room(request, pk):
    RoomObj=Room.objects.get(id=pk)
    messages = RoomObj.message_set.all()
    if request.method == 'POST':
        messages = Message.objects.create(
            user = request.user,
            room = RoomObj,
            body = request.POST.get('body'),
        )
        return redirect(room,pk=RoomObj.id)
    context = {'room':RoomObj, 'messages': messages}
    return render(request,"base/room.html",context)

def createRoom(request):
    form = RoomForm
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'forms':form}
    return render (request,'base/SignUp.html',context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    
    form = RoomForm(instance=room) #prefilled form
    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'forms':form}
    return render (request,'base/SignUp.html',context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect ('home')
    context={'room':room}
    return render (request, 'base/delete.html',context)


def loginPage(request):
    # form =
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.object.get(username=username)
        except:
            messages.error(request, 'Invalid username or password')
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')
    context = {}
    return render (request, 'base/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('home')

def updateMessage(request, message):
    return render(request)

def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.method == 'POST':
        message.delete()
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return redirect('home')
    context={'message': message}
    return render (request, 'base/delete.html', context)

