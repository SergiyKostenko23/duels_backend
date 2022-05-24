from django.contrib import admin

from .models import User, Duel, Item, Result, Progress, Message

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'nome', 'email', 'data_registo', 'tipo_user', 'criado_por', 'photo']
    readonly_fields = ('id', 'criado_por')

class DuelAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'desc', 'criador', 'feito', 'criado', 'slug']
    readonly_fields = ('id', "feito", 'criado')

class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'url', 'duel', 'popularidade']
    readonly_fields = ('id', 'popularidade')

class ResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'result', 'inicio', 'fim', 'users', 'duels']
    readonly_fields = ('id', 'result', 'inicio', 'fim', 'users', 'duels')

class ProgressAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'duel', 'chosen', 'not_chosen', 'iteration']

class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'message', 'time']

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Duel, DuelAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Progress, ProgressAdmin)
admin.site.register(Message, MessageAdmin)