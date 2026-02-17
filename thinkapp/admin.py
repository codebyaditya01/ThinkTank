from django.contrib import admin
from .models import *


class QuestiondbaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at', 'views')
    search_fields = ('title', 'body', 'user__username')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


class AnswerdbaseAdmin(admin.ModelAdmin):
    list_display = ('question', 'user', 'created_at', 'updated_at')
    search_fields = ('body', 'user__username', 'question__title')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


class CommentdbaseAdmin(admin.ModelAdmin):
    list_display = ('answer', 'user', 'body', 'commented_at')
    search_fields = ('body', 'user__username', 'answer__body')
    list_filter = ('commented_at',)
    ordering = ('-commented_at',)


class VotingdbaseAdmin(admin.ModelAdmin):
    list_display = ('answer', 'user', 'value')
    search_fields = ('user__username', 'answer__body')
    list_filter = ('value',)


class ProfiledbaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email', 'prof', 'achievements', 'created_at')
    search_fields = ('user__username', 'name', 'email', 'prof', 'achievements')
    list_filter = ('created_at',)


admin.site.register(Questiondbase, QuestiondbaseAdmin)
admin.site.register(Answerdbase, AnswerdbaseAdmin)
admin.site.register(Commentdbase, CommentdbaseAdmin)
admin.site.register(Votingdbase, VotingdbaseAdmin)
admin.site.register(Profiledbase, ProfiledbaseAdmin)
