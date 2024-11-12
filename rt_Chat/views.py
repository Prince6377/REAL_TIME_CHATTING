from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.http import Http404
from django.contrib import messages
from channels.layers import get_channel_layer
from django.http import HttpResponse
from asgiref.sync import async_to_sync


@login_required
def chat_view(request, chatroom_name = 'Social'):
    chat_group = get_object_or_404(GroupName,group_name = chatroom_name)
    chat_message = chat_group.chat_messages.all()[:30]
    form = AddMessage()
    other_user = None
    if chat_group.is_private:
        if request.user not in chat_group.member.all():
            raise Http404()
        for member in chat_group.member.all():
            if member != request.user:
                other_user = member
                break
    
    if chat_group.groupchat_name:
        if request.user not in chat_group.member.all():
            if request.user.emailaddress_set.filter(verified = True).exists():  
                chat_group.member.add(request.user)
            else:
                messages.warning(request , 'You need to verify your email to join the chat!')
                return redirect('profile-settings')
    
    if request.htmx and request.method == "POST":
        form = AddMessage(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            context = {
                'message' : message,
                'user' : request.user
            }
            return render(request,'rt_chatting/partial/chat_message_p.html',context)
    
    context = {
        'messages' : chat_message,
        'form' : form,
        'other_user' : other_user,
        'chatroom_name' : chatroom_name,
        'chat_group' : chat_group,
    }
    return render(request,'rt_chatting/chat_view.html',context)

@login_required
def get_or_create_chatroom(request, username):
    
    
    if request.user.username == username:
        return redirect('chat')
    
    # Find the other user or return a 404 if not found
    other_user = get_object_or_404(User, username=username)
    
    # Check if any private chatroom exists with the other user
    my_chatrooms = request.user.chat_groups.filter(is_private=True)
    
    # Loop to find if the chatroom already exists
    for chatroom in my_chatrooms:
        if other_user in chatroom.member.all():
            # If chatroom found, redirect to it
            return redirect('chatroom', chatroom_name=chatroom.group_name)



    # If no chatroom exists, create a new one
    chatroom = GroupName.objects.create(is_private=True)
    chatroom.member.add(other_user, request.user)
    return redirect('chatroom', chatroom_name=chatroom.group_name)

@login_required
def create_groupchat(request):
    form = NewGroupForm()
    
    if request.method == 'POST':
        form = NewGroupForm(request.POST)
        if form.is_valid():
            new_groupchat = form.save(commit=False)
            new_groupchat.admin = request.user
            new_groupchat.save()
            new_groupchat.member.add(request.user)
            return redirect('chatroom', new_groupchat.group_name)
    
    context = {
        'form': form
    }
    return render(request, 'rt_chatting/create_groupchat.html', context)

@login_required
def chatroom_edit_view(request ,chatroom_name):
    chat_group = get_object_or_404(GroupName, group_name=chatroom_name)
    if request.user != chat_group.admin:
        raise Http404()
    form = ChatRoomEditForm(instance=chat_group)  
    if request.method == 'POST':
        form = ChatRoomEditForm(request.POST, instance=chat_group)
        if form.is_valid():
            form.save()
            remove_members = request.POST.getlist('remove_members')
            for member_id in remove_members:
                mem = User.objects.get(id=member_id)
                chat_group.member.remove(mem)  
                
            return redirect('chatroom', chatroom_name) 
    context = {
        'form' : form,
        'chat_group' : chat_group
    }   
    return render(request , 'rt_chatting/edit_chat.html',context)
     
@login_required
def chatroom_delete_view(request, chatroom_name):
    chat_group = get_object_or_404(GroupName, group_name=chatroom_name)
    if request.user != chat_group.admin:
        raise Http404()
    if request.method == "POST":
        chat_group.delete()
        messages.success(request, 'Chatroom deleted')
        return redirect('chat')
    return render(request, 'rt_chatting/chatroom_delete.html', {'chat_group':chat_group})

@login_required
def chatroom_leave_view(request, chatroom_name):
    chat_group = get_object_or_404(GroupName, group_name=chatroom_name)
    if request.user not in chat_group.members.all():
        raise Http404()
    
    if request.method == "POST":
        chat_group.members.remove(request.user)
        messages.success(request, 'You left the Chat')
        return redirect('chat')
    
    return render(request, 'rt_chatting/modal_chat_leave.html', {'chat_group': chat_group})

def chat_file_upload(request, chatroom_name):
    chat_group = get_object_or_404(GroupName, group_name=chatroom_name)
    
    if request.htmx and request.FILES:
        file = request.FILES['file']
        message = GroupMessages.objects.create(
            file = file,
            author = request.user, 
            group = chat_group,
        )
        channel_layer = get_channel_layer()
        event = {
            'type': 'message_handler',
            'message_id': message.id,
        }
        async_to_sync(channel_layer.group_send)(
            chatroom_name, event
        )
    return HttpResponse()
    