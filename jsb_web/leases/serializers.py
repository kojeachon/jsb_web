from rest_framework import serializers

from jsb_web.users.models import User as user_model
from . import models

class FeedAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_model
        fields = (
            "id", 
            "username",
            "bu_name",
            "level_name",
        )

class RoomSerializer(serializers.ModelSerializer):
    # author = FeedAuthorSerializer()

    class Meta:
        model = models.Room
        fields = (
            "id",
            "type1",
            "type2",
            "roomnumber",
            "roompeople",
            "roommoney",
            "image",
        )

class LeaseSerializer(serializers.ModelSerializer):
    author = FeedAuthorSerializer()
    room = RoomSerializer()
    st_date = serializers.DateTimeField(format="%Y-%m-%d")
    ed_date = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = models.Lease
        fields = (
            "id",
            "st_date",
            "ed_date",
            "usepeople",
            "leasename",
            "phonenumber",
            "contents",
            "room",
            "author",
        )