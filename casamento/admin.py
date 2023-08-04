from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

import casamento.models as models

class PhotoInline(admin.TabularInline):
    model = models.Photo
    extra = 0
    readonly_fields = ["image_link",]

    def image_link(self, obj):
        return format_html('<a href="{}">Open Image</a>', obj.image.url)
    image_link.short_description = 'Image Link'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(approved=True)


class PhotoAdmin(admin.ModelAdmin):
    list_display = ['image', 'approved']
    readonly_fields = ["image_link",]

    def image_link(self, obj):
        return format_html('<a href="{}">Open Image</a>', obj.image.url)
    image_link.short_description = 'Image Link'


class GalleryAdmin(admin.ModelAdmin):
    inlines = [PhotoInline]
    search_fields = ['name']
    list_display = ('name',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['photo', 'text']
    exclude = ['commented_by',]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'photo':
            kwargs['queryset'] = models.Photo.objects.filter(approved=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
        
    def save_model(self, request, obj, form, change):
        if not change:  
            obj.commented_by = request.user
        super().save_model(request, obj, form, change)
    

class LikeAdmin(admin.ModelAdmin):
    list_display = ['photo', 'liked_by']
    exclude = ['liked_by',]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'photo':
            kwargs['queryset'] = models.Photo.objects.filter(approved=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        if not change:  
            obj.liked_by = request.user
        super().save_model(request, obj, form, change)
    

admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.Gallery, GalleryAdmin)
admin.site.register(models.Like, LikeAdmin)
admin.site.register(models.Photo, PhotoAdmin) 
admin.site.register(models.UserUpload)
