from django.contrib import admin

from core.models import Suspect


class SuspectAdmin(admin.ModelAdmin):
	list_display_links = ('first_name', 'last_name',)
	list_display = ('image_tag', 'first_name', 'last_name', 'gender', 
		'face_complexion', 'face_shape', 'hair', 'cheek', 'eyelashes', 
		'eyebrow', 'eyes', 'nose'
	)

	readonly_fields = ( 'image_tag', )

admin.site.register(Suspect, SuspectAdmin)