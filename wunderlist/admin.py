from django.contrib import admin
from wunderlist.models import Category, Item, Comment

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class CommentAdmin(admin.ModelAdmin):
    display_fields = ["post", "author", "created"]

admin.site.register(Comment, CommentAdmin)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Item)
# Register your models here.
