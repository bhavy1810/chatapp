from django.shortcuts import render, redirect
from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse

# Home page
def home(request):
    return render(request, 'home.html')

# Room view
def room(request, room):
    username = request.GET.get('username')
    try:
        room_details = Room.objects.get(name=room)
    except Room.DoesNotExist:
        room_details = None  # Room not found

    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

# Check if room exists, else create it
def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

# Send message
def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room_id=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

# Get messages
def getMessages(request, room):
    try:
        room_details = Room.objects.get(name=room)
        messages = Message.objects.filter(room=room_details.id)
        messages_list = list(messages.values())
    except Room.DoesNotExist:
        messages_list = []  # No messages if room doesn't exist

    return JsonResponse({"messages": messages_list})
