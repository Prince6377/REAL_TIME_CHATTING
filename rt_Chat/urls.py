from django.urls import path
from .views import *

# Confirm URL loading
print("new_groupchat URL is loaded!")

urlpatterns = [
   path('', chat_view, name='chat'),
   path('chat/<username>/', get_or_create_chatroom, name='start-chat'),
   path('chat/room/<chatroom_name>/', chat_view, name='chatroom'),
   path('createnew_chat/', create_groupchat, name='new-groupchat'),
   path('chat/edit/<chatroom_name>', chatroom_edit_view , name= "edit-chatroom") ,
   path('chat/delete/<chatroom_name>', chatroom_delete_view , name = 'chatroom-delete' ),
   path('chat/leave/<chatroom_name>', chatroom_leave_view, name="chatroom-leave"),
   path('chat/fileupload/<chatroom_name>', chat_file_upload, name="chat-file-upload"),
]
