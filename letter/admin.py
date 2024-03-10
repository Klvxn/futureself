from django.contrib import admin
from .models import Letter


# Register your models here.
@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'email_address', 'delivered', 'audience')
    list_filter = ('audience',)
    actions = ['mark_delivered', 'set_audience_public', 'set_audience_private']

    @admin.action(description='Mark as delivered')
    def mark_delivered(self, request, queryset):
        queryset.update(delivered=True)
        self.message_user(request, 'Marked as delivered')

    @admin.action(description='Set audience public')
    def set_audience_public(self, request, queryset):
        queryset.update(audience='public, but as anon')
        self.message_user(request, 'Marked as public') 
    
    @admin.action(description='Set audience private')
    def set_audience_private(self, request, queryset):
        queryset.update(audience='private')
        self.message_user(request, 'Marked as private')    
        