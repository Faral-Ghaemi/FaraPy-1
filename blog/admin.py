from django.contrib import admin
from . import models


class PostAdmin(admin.ModelAdmin):

    list_display = ('title', 'slug', 'status','category')
    list_filter = ("status","category")
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(models.Post, PostAdmin)


class MultimediaAdmin(admin.ModelAdmin):

    list_display = ('title', 'slug', 'status','image')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(models.Multimedia, MultimediaAdmin)

@admin.register(models.Time )
class TimeAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Tabs )
class TabsAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Tickets )
class stAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Task_manegar )
class Task_manegarAdmin(admin.ModelAdmin):
    list_display = ('title','end_time','status',)


@admin.register(models.Theme )
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(models.Safahat )
class SafahatAdmin(admin.ModelAdmin):
    list_display = ('title','author','created_date')

@admin.register(models.Ads )
class AdsAdmin(admin.ModelAdmin):
    list_display = ('url','date','EXdate')


@admin.register(models.Category )
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title','image')


@admin.register(models.Slider )
class SliderAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(models.Links )
class LinksAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(models.Setting)
class SettingAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Portable )
class PortableAdmin(admin.ModelAdmin):
    list_display = ('full_name',)


@admin.register(models.Comment )
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','text','post',)

@admin.register(models.SubPage )
class SubPageAdmin(admin.ModelAdmin):
    pass
