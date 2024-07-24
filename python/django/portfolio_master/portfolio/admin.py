from django.contrib import admin

from .models import Skill, Category, Work, Service, Item, Author, Message, Testimony


# Регистрация модели Skill в админке
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'level')
    search_fields = ('name',)


# Регистрация модели Category в админке
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('engname', 'rusname')
    search_fields = ('engname', 'rusname')


# Регистрация модели Work в админке
@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category')
    search_fields = ('title', 'category__rusname')
    prepopulated_fields = {'slug': ('title',)}


# Регистрация модели Service в админке
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)


# Регистрация модели Item в админке
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'service')
    search_fields = ('name', 'service__name')


# Регистрация модели Author в админке
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'lastname')
    search_fields = ('name', 'lastname')
    filter_horizontal = ('skills',)


# Регистрация модели Message в админке
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    readonly_fields = ('created_at',)


# Регистрация модели Testimony в админке
@admin.register(Testimony)
class TestimonyAdmin(admin.ModelAdmin):
    list_display = ('name', 'lastname')
    search_fields = ('name', 'lastname')

# Также можно использовать admin.site.register() для регистрации моделей, но использование @admin.register предпочтительнее.
# admin.site.register(Skill, SkillAdmin)
# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Work, WorkAdmin)
# admin.site.register(Service, ServiceAdmin)
# admin.site.register(Item, ItemAdmin)
# admin.site.register(Author, AuthorAdmin)
# admin.site.register(Message, MessageAdmin)
# admin.site.register(Testimony, TestimonyAdmin)
