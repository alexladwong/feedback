# feedback/admin.py

from django.contrib import admin
from .models import *



class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'product_service', 'rating', 'created_at')
    search_fields = ('user_name', 'comment')
    list_filter = ('product_service', 'rating')

admin.site.register(ProductService)
admin.site.register(Feedback, FeedbackAdmin)



admin.site.register(Subscription)
