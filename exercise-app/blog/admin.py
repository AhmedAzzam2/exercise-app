from django.contrib import admin
from .models import Post,Category


# display the exercisename and hour of the post
class PostAdmin(admin.ModelAdmin):
    list_display = ( 'hour','date_posted')
    list_filter = ('date_Posted',)
    ordering = ('date_Posted',)
    date_hierarchy = 'date_Posted'
    list_per_page = 101

    def date_posted(self, obj):
        return obj.date_Posted.strftime('%b %d %Y')

    date_posted.admin_order_field = 'date_Posted'

# Add the PostAdmin to the admin site
admin.site.register(Post, PostAdmin)


admin.site.register(Category)