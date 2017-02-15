from django import forms
from django.utils.translation import ugettext_lazy as _

from core.models import Suspect

class FacialFeaturesForm(forms.ModelForm):

	gender 			= forms.ChoiceField(choices=Suspect.GENDER_CHOICES, widget=forms.Select(), label=(""))
	face_complexion = forms.ChoiceField(choices=Suspect.FACE_COMPLEXION_CHOICES, widget=forms.Select(), label=(""))
	face_shape 		= forms.ChoiceField(choices=Suspect.FACE_SHAPE_CHOICES, widget=forms.Select(), label=(""))
	hair 			= forms.ChoiceField(choices=Suspect.HAIR_CHOICES, widget=forms.Select(), label=(""))
	cheek 			= forms.ChoiceField(choices=Suspect.CHEEK_CHOICES, widget=forms.Select(), label=(""))
	ear 			= forms.ChoiceField(choices=Suspect.EAR_CHOICES, widget=forms.Select(), label=(""))
	eyelashes 		= forms.ChoiceField(choices=Suspect.EYELASHES_CHOICES, widget=forms.Select(), label=(""))
	eyebrow 		= forms.ChoiceField(choices=Suspect.EYEBROW_CHOICES, widget=forms.Select(), label=(""))
	eyes 			= forms.ChoiceField(choices=Suspect.EYES_CHOICES, widget=forms.Select(), label=(""))
	nose 			= forms.ChoiceField(choices=Suspect.NOSE_CHOICES, widget=forms.Select(), label=(""))

	class Meta:
		model = Suspect
		fields = []
