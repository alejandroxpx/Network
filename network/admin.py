from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id","password","username")

class PostAdmin(admin.ModelAdmin):
    list_display = ("id","user","post","date","likes")

class CommentsAdmin(admin.ModelAdmin):
    list_display = ("id", "comment","user_commenting","user_being_commented","date","likes")

class ConnectionsAdmin(admin.ModelAdmin):
    list_display = ("follower_id", "following_id")

admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentsAdmin)
admin.site.register(Connection,ConnectionsAdmin)