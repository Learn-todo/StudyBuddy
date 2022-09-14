import imp
from django.shortcuts import HttpResponse
from django.shortcuts import render,redirect
from .models import Room
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def home(request):
    RoomObj=Room.objects.all()
    context = {'RoomObj':RoomObj}
    return render(request,'base/index.html',context)

def room(request, pk):
    RoomObj=Room.objects.get(id=pk)
    context = {'RoomObj':RoomObj}
    return render(request,"base/room.html",context=context)

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
    user =authenticate(request, username = username, password = password)
    if user is not None:
        login(request, user)
        return redirect('home')
    else:
        messages.error(request, 'Username does not exist')
    context = {}
    return render (request, 'base/login.html', context)