from django.contrib import admin
from wai.scheduler.models import Group,Presenter,Room,Meeting,Presentation

class PresentationInline(admin.StackedInline):
	model = Presentation
	extra = 2
	max_num = 2

class GroupAdmin(admin.ModelAdmin):
	list_display = ['name', 'members_count']

class RoomAdmin(admin.ModelAdmin):
	list_display = ['name', 'note']

class PresenterAdmin(admin.ModelAdmin):
	fields = ['name', 'group', 'email', 'note', 'available']
	list_display = ['name', 'email', 'group', 'presentations_count', 'last_presentation', 'available', 'note']
	list_filter = ['group']

class PresentationAdmin(admin.ModelAdmin):
	list_display = ['meeting', 'presenter', 'title', 'abstract']

class MeetingAdmin(admin.ModelAdmin):
	list_display = ['date', 'location', 'presenters']
	list_filter = ['date']
	date_hierarchy = 'date'
	inlines = [PresentationInline]


# Register admin
admin.site.register(Group, GroupAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Presenter, PresenterAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Presentation, PresentationAdmin)

