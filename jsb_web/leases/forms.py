from django import forms
from django.forms import fields, widgets
from .models import Lease, Room


class CreateRoomForm(forms.ModelForm):
    CHOICES = [('대관','대관'),('숙소','숙소')]
    type1 = forms.ChoiceField(choices=CHOICES,label="유형1")

    class Meta:
        model = Room
        # fields = ["roomnumber"]
        fields = ["roomnumber","type1","type2","roompeople","roommoney","image"]

        labels = {
            "roomnumber":"호실",
            "type1":"유형1",
            "type2":"유형2",
            "roompeople":"최대 수용인원",
            "roommoney":"금액",
            "image":"이미지"
        }

class CreateLeaseForm(forms.ModelForm):
    CHOICES = [('대관','대관'),('숙소','숙소')]
    type1 = forms.ChoiceField(choices=CHOICES,label="유형1")
    type2 = forms.ChoiceField(choices=CHOICES,label="유형2")

    class Meta:
        model = Lease
        fields = ["room","st_date","ed_date","type1","type2","usepeople","phonenumber","contents"]
        labels = {
            "room":"호실",
            "st_date":"시작일",
            "ed_date":"종료일",
            "type1":"유형1",
            "type2":"유형2",
            "usepeople":"사용자수",
            "phonenumber":"전화번호",
            "contents":"메모"
        }

class RoomCreateForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ("roomnumber","type1","type2","roompeople","roommoney","image")
        labels = {
            "roomnumber":"호실",
            "type1":"유형1",
            "type2":"유형2",
            "roompeople":"최대 수용인원",
            "roommoney":"금액",
            "image":"이미지"
        }

class LeaseForm(forms.ModelForm):

    # st_date = forms.DateField(widget=widgets.DateInput(format='%Y-%m-%d'), input_formats=['%Y-%m-%d'], required=False)
    # ed_date = forms.DateField(widget=widgets.DateInput(format='%Y-%m-%d'), input_formats=['%Y-%m-%d'], required=False)
        
    class Meta:
        model = Lease
        fields = ["room","st_date","ed_date","usepeople","phonenumber","contents","state"]
        labels = {
            "room":"호실",
            "st_date":"시작일",
            "ed_date":"종료일",
            "usepeople":"사용자수",
            "phonenumber":"전화번호",
            "contents":"메모",
            "state":"상태"
        }
