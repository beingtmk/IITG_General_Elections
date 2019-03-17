from django import forms
from django.forms import ModelForm

from .models import VoterList,Contestants

class VolunteerForm(forms.Form):
	# All required by default
	first_name = forms.CharField(label='Volunteer First Name', max_length=100)
	last_name = forms.CharField(label='Volunteer Last Name', max_length=100)
	username = forms.CharField(label='Webmail_id', max_length=100)
	password = forms.CharField(label='Password', max_length=100)

# Check this https://stackoverflow.com/a/22749879
class VoterListForm(ModelForm):
	class Meta:
		model = VoterList
		fields = ['webmail_id', 'name', 'roll_no', 'gender', 'hostel', 'dept',
					'program', 'mobile_no', 'comments',]

class AddVoterForm(ModelForm):
	class Meta:
		model = VoterList
		fields = ['webmail_id', 'name', 'roll_no', 'gender', 'hostel',
					'dept', 'program', 'mobile_no', 'comments',]

class AddContestantForm(ModelForm):
    class Meta:
        model = Contestants
        fields = ['webmail_id', 'name', 'agenda1', 'agenda2', 'agenda3',
                    'image', 'post', 'mobile_no', 'eligible', 'comments',]

# Voting forms
class VoteVP(forms.Form):
    '''VoteVP'''
    __qualname__ = 'VoteVP'
    contestants = forms.ModelChoiceField(widget=forms.RadioSelect(), queryset=Contestants.objects.filter(post='VP').order_by('?'))

class VoteHAB(forms.Form):
    '''VoteHAB'''
    __qualname__ = 'VoteHAB'
    contestants = forms.ModelChoiceField(widget=forms.RadioSelect(), queryset=Contestants.objects.filter(post='HAB').order_by('?'))

class VoteTECH(forms.Form):
    '''VoteTECH'''
    __qualname__ = 'VoteTECH'
    contestants = forms.ModelChoiceField(widget=forms.RadioSelect(), queryset=Contestants.objects.filter(post='TECH').order_by('?'))


class VoteCULT(forms.Form):
    '''VoteCULT'''
    __qualname__ = 'VoteCULT'
    contestants = forms.ModelChoiceField(widget=forms.RadioSelect(), queryset=Contestants.objects.filter(post='CULT').order_by('?'))


class VoteWELFARE(forms.Form):
    '''VoteWELFARE'''
    __qualname__ = 'VoteWELFARE'
    contestants = forms.ModelChoiceField(widget=forms.RadioSelect(), queryset=Contestants.objects.filter(post='WELFARE').order_by('?'))


class VoteSPORTS(forms.Form):
    '''VoteSPORTS'''
    __qualname__ = 'VoteSPORTS'
    contestants = forms.ModelChoiceField(widget=forms.RadioSelect(), queryset=Contestants.objects.filter(post='SPORTS').order_by('?'))


class VoteSAIL(forms.Form):
    '''VoteSAIL'''
    __qualname__ = 'VoteSAIL'
    contestants = forms.ModelChoiceField(widget=forms.RadioSelect(), queryset=Contestants.objects.filter(post='SAIL').order_by('?'))

class VoteSWC(forms.Form):
     '''VoteSWC'''
     __qualname__ = 'VoteSWC'
     contestants = forms.ModelChoiceField(widget=forms.RadioSelect(), queryset=Contestants.objects.filter(post='SWC').order_by('?'))


class VoteUGS(forms.Form):
    '''VoteUGS'''
    __qualname__ = 'VoteUGS'
    contestants = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=Contestants.objects.filter(post='UGS').order_by('?'))


class VotePGS(forms.Form):
    '''VotePGS'''
    __qualname__ = 'VotePGS'
    contestants = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=Contestants.objects.filter(post='PGS').order_by('?'))

class VoteGS(forms.Form):
    '''VoteGS'''
    __qualname__ = 'VoteGS'
    contestants = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=Contestants.objects.filter(post='GS').order_by('?'))
