# remove_player.py
#Removing the member also from the channel layer group:
from .models import *
class UserChannel(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, null=True, blank=True)
    channel = models.CharField(max_length=300)

# link user with channel if it's a groupchat
# consumers.py
def connect(self): 
    if self.chatroom.groupchat_name:
        UserChannel.objects.get_or_create(
            member = self.user, 
            group = self.chatroom,
            channel = self.channel_name 
        )

# remove user_channel when disconnecting
# consumers.py
def disconnect(self, close_code):
    user_channel = UserChannel.objects.get(channel=self.channel_name )
    user_channel.delete()

# remove user_channel when admin removes member
# views.py
def chatroom_edit_view(request, chatroom_name):
           for member_id in remove_members:
            channel_layer = get_channel_layer()
            user_channels = UserChannel.objects.filter(member=member, group=chat_group)
            for user_channel in user_channels:async_to_sync(channel_layer.group_discard)(chatroom_name,user_channel.channel)user_channel.delete()