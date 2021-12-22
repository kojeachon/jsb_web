from django.db import models
from django.urls import reverse
from jsb_web.users import models as user_model

# Create your models here.
class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Room(TimeStampModel):
    author = models.ForeignKey(
            user_model.User, 
            null=True, 
            on_delete=models.CASCADE, 
            related_name='room_author'
        )
    roomnumber = models.CharField(blank=False, max_length=255)
    type1 = models.CharField(blank=False, max_length=255)
    type2 = models.CharField(blank=False, max_length=255)
    roompeople = models.IntegerField(blank=False)
    roommoney = models.IntegerField(blank=False)
    image = models.ImageField(blank=True)
    room_likes = models.ManyToManyField(
        user_model.User, 
        blank=True,
        related_name='room_likes'
        )

    def __str__(self):
        roommoney = "{:,}".format(self.roommoney)
        # return f"{self.roomnumber}, {self.type1}, {self.type2}, 수용인원:{self.roompeople}, 금액:{roommoney}"
        return f"{self.roomnumber}"

    def get_absolute_url(self):
        return reverse("leases:roomlist", args=[str(self.id)])

class Lease(TimeStampModel):
    STATE_CHOICES = [
        ('step1', '신청'),
        ('step2', '가계약'),
        ('step3', '예약완료'),
        ('step4', '취소'),
    ]
    author = models.ForeignKey(
            user_model.User, 
            null=True, 
            on_delete=models.CASCADE, 
            related_name='lease_author'
        )
    room = models.ForeignKey(
            Room, 
            null=True, 
            on_delete=models.CASCADE, 
            related_name='lease_room'
        )
    st_date = models.DateTimeField(blank=False)
    ed_date = models.DateTimeField(blank=False)
    usepeople = models.IntegerField(blank=False)
    leasename = models.CharField(blank=False, max_length=255)
    phonenumber = models.CharField(blank=False, max_length=255)
    contents = models.TextField(blank=True)
    state = models.CharField(blank=True, max_length=5,choices=STATE_CHOICES,default='step1')

    def __str__(self):
        # return f"{self.author},{self.contents}"
        return f"{self.st_date} ~ {self.ed_date}"