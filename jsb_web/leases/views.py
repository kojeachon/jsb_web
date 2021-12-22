from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django.http import request
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from jsb_web.leases import serializers
from jsb_web.users.models import User as user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views import generic
from . import models

from .forms import CreateLeaseForm, CreateRoomForm, RoomCreateForm
from jsb_web.leases import forms

# Create your views here.

def index(request,urlno='1'):
    if not request.user.is_authenticated:
        return redirect(reverse('users:main'))
    # return render(request,'leases/index.html')
    if request.method == "GET":
        if request.user.is_authenticated:
            lease_form = CreateLeaseForm()

            s_date = datetime.today() + timedelta(days=-30)
            e_date = datetime.today() + timedelta(days=60)
            s_date = datetime(int(s_date.strftime('%Y')), int(s_date.strftime('%m')), 1)
            e_date = datetime(int(e_date.strftime('%Y')), int(e_date.strftime('%m')), 1) + timedelta(days=-1)
            # print("now= ",s_date,e_date)

            # leases = models.Lease.objects.all()
            q = Q()
            q &= Q(st_date__range = [s_date,e_date]) | Q(ed_date__range = [s_date,e_date])

            leases = models.Lease.objects.filter(q)
            # print("leases= ",leases)

            serializer = serializers.LeaseSerializer(leases, many=True)
            # print("serializer= ", serializer.data)

            # leases = models.Lease.objects.filter(
            #     Q(room_id=1)
            # )
            # print("leases= ",leases)
            # serializer = serializers.RoomSerializer(rooms, many=True)
            # print("serializer= ", serializer.data)

            # user = get_object_or_404(user_model,pk=request.user.id)
            # following = user.following.all()
            # posts = models.Post.objects.filter(
            #     Q(author__in=following) | Q(author=user)
            # )
            # serializer = serializers.PostSerializer(posts, many=True)
            # print(serializer.data)
            # print('request.GET == ',request)
            # print("========== end ===== ")
            # return render(request, 
            # 'leases/index.html'
            # )

            # return render(request,'leases/index.html')

            return render(request, 
            'leases/index.html',
            {"posts":serializer.data, "comment_form": lease_form, "urlno":urlno}
            )

def lease_list(request,urlno='2'):
    if not request.user.is_authenticated:
        return redirect(reverse('users:main'))
    # return render(request,'leases/index.html')
    if request.method == "GET":
        if request.user.is_authenticated:
            leases = models.Lease.objects.all()
            # leases = leases.extra(select={'st_date':"DATE_FORMAT(st_date, '%Y-%m-%d')"})
            print("leases= ",leases)
            serializer = serializers.LeaseSerializer(leases, many=True)
            # print("serializer= ", serializer.data)

            return render(request, 
            'leases/list.html',
            {"posts":serializer.data, "urlno":urlno})

def lease_create(request,urlno='1'):
    if not request.user.is_authenticated:
        return redirect(reverse('users:main'))
    if request.method == 'GET':
        # print(request.user.is_staff,request.user.is_superuser,request.user.is_active)
        form = CreateLeaseForm()
        return render(request,'leases/lease_create.html',{"form":form, "urlno":urlno})

    # if request.method == 'GET':
    #     return render(request,'leases/main.html')

    # elif request.method == 'POST':
    #     if request.user.is_authenticated:
    #         return render(request,'leases/main.html')
    #     return render(request,'users/main.html')

def room_create(request,urlno='3'):
    # print("django path = ", django.__path__)
    if not request.user.is_authenticated:
        return redirect(reverse('users:main'))
    if request.method == 'GET':
        form = CreateRoomForm()
        return render(request,'leases/room_create.html',{"form":form,"urlno":urlno})

    elif request.method == 'POST':
        if request.user.is_authenticated:
            user = get_object_or_404(user_model, pk=request.user.id)
            # image = request.FILES['image']
            # caption = request.POST['caption']

            # new_post = models.Post.objects.create(
            #     author = user,
            #     image = image,
            #     caption = caption
            # )
            # new_post.save()

            form = CreateRoomForm(request.POST, request.FILES)
            if form.is_valid():
                room = form.save(commit=False)
                room.author = user
                room.save()
            else:
                print(form.errors)

            return render(request,'leases/room_create.html',{"form":form, "urlno":urlno})

        else:
            return redirect(reverse('users:main'))
    return render(request,'leases/room_create.html',{"urlno":urlno})

def get_json_type1_data(request):
    qs_val = list(models.Room.objects.values('type1').distinct())
    return JsonResponse({'data':qs_val})

def get_json_type2_data(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect(reverse('users:main'))
    if request.is_ajax():
        selected_type1 = kwargs.get('type1')
        # selected_type1 = request.GET.get('type1')
        # s_date = request.GET.get('st_date')
        # e_date = request.GET.get('ed_date')
        # print('selected_type1=',selected_type1,s_date,e_date)
        # q = ~Q(st_date__range = [s_date,e_date]) & ~Q(ed_date__range = [s_date,e_date])
        # if selected_type1 != '선택':
        #     q &= Q(type1=selected_type1)

        obj_type2 = list(models.Room.objects.filter(type1=selected_type1).values('type2').distinct())
        return JsonResponse({'data':obj_type2})

def get_json_roomnumber_data(request, *args, **kwargs):
    selected_type2 = kwargs.get('type2')
    # obj_roomnumber = list(models.Room.objects.filter(type2=selected_type2).values('roomnumber'))

    # test_lieases = list(models.Lease.objects.values('id'))
    # print(test_lieases)

    type1 = request.GET.get('type1')
    s_date = request.GET.get('st_date')
    e_date = request.GET.get('ed_date')
    print('selected_type2=',selected_type2,type1,s_date,e_date)
    q = Q(st_date__range = [s_date,e_date]) | Q(ed_date__range = [s_date,e_date])
    # if type1 != '선택':
    #     q &= Q(type1=type1)
    leases = models.Lease.objects.filter(q).values('room_id')
    print('leases===',leases)

    obj_roomnumber = list(models.Room.objects.filter(Q(type1=type1) & Q(type2=selected_type2)
    ,~Q(id__in=leases)).values('roomnumber','roommoney'))
    # print(obj_roomnumber)

    return JsonResponse({'data':obj_roomnumber})

def save_lease_create(request):
    if not request.user.is_authenticated:
        return redirect(reverse('users:main'))
    if request.is_ajax():
        st_date = request.POST.get('st_date')
        ed_date = request.POST.get('ed_date')
        type1 = request.POST.get('type1')
        type2 = request.POST.get('type2')
        roomnumber = request.POST.get('roomnumber')
        usepeople = request.POST.get('usepeople')
        leasename = request.POST.get('leasename')
        phonenumber = request.POST.get('phonenumber')
        contents = request.POST.get('contents')
        room_obj = models.Room.objects.get(roomnumber=roomnumber)
        author_obj = user_model.objects.get(pk=request.user.id)

        print(st_date,ed_date,type1,type2,roomnumber,usepeople,leasename,phonenumber,contents,room_obj,author_obj)
        # print(st_date,ed_date,type1,type2,roomnumber,usepeople,leasename,phonenumber,contents,room_obj)

        models.Lease.objects.create(st_date=st_date, ed_date=ed_date, usepeople=int(usepeople), leasename=leasename, phonenumber=phonenumber, contents=contents
        , room=room_obj, author=author_obj)
        return JsonResponse({'created': True})
    return JsonResponse({'created': False})

def get_json_leases_data(request):
    print('request===',request)
    # qs_val = list(models.Lease.objects.values('st_date','ed_date','room'))
    # print(qs_val)
    # return JsonResponse({'data':qs_val})
    if not request.user.is_authenticated:
        return redirect(reverse('users:main'))
    if request.is_ajax():

        datec = request.GET.get('datec')
        type1 = request.GET.get('type1')
        type2 = request.GET.get('type2')
        in_date = datetime.strptime(datec[4:15],'%b %d %Y')

        s_date = in_date + timedelta(days=-30)
        e_date = in_date + timedelta(days=60)
        s_date = datetime(int(s_date.strftime('%Y')), int(s_date.strftime('%m')), 1)
        e_date = datetime(int(e_date.strftime('%Y')), int(e_date.strftime('%m')), 1) + timedelta(days=-1)
        # print("now= ",s_date,e_date)

        # q = Q()
        q = Q(st_date__range = [s_date,e_date]) | Q(ed_date__range = [s_date,e_date])
        if type1 != '선택':
            q &= Q(room__type1 = type1)
        if type2 != '선택':
            q &= Q(room__type2 = type2)

        # leases = models.Lease.objects.all()
        leases = models.Lease.objects.filter(q)
        # print('in_date===',in_date)
        # print('datec===',datec[4:15])
        # print('type1===',type1)
        # print('type2===',type2)
        # print(leases)


        qs_val = serializers.LeaseSerializer(leases, many=True)
        return JsonResponse({'data':qs_val.data})
    return JsonResponse({'data': False})
def test(request):
    return render(request,'leases/test.html')


class RoomCreate(LoginRequiredMixin, CreateView):
    model = models.Room
    form_class = RoomCreateForm

class RoomList(LoginRequiredMixin, generic.ListView):
    paginate_by = 10
    model = models.Room

class RoomDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Room

class RoomUpdate(LoginRequiredMixin, generic.UpdateView):
    model = models.Room
    context_object_name = 'room'
    form_class = forms.RoomCreateForm
    template_name = "leases/room_edit.html"
    success_url = "/leases/roomlist/"

    def get_object(self):
        room = get_object_or_404(models.Room, pk=self.kwargs['pk'])
        return room    


class LeaseList(LoginRequiredMixin, generic.ListView):
    paginate_by = 5
    model = models.Lease

    def get_queryset(self):
        type1 = self.request.GET.get('type1', '선택')
        type2 = self.request.GET.get('type2', '선택')
        print("type1=",type1,"type2=",type2)
        q = Q()
        if len(type1)>0 and type1 != '선택':
            q &= Q(room__type1=type1)
        if len(type2)>0 and type2 != '선택':
            q &= Q(room__type2=type2)

        new_context = models.Lease.objects.filter(q)
        return new_context

class LeaseDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Lease

class LeaseUpdate(LoginRequiredMixin, generic.UpdateView):
    model = models.Lease
    context_object_name = 'lease'
    form_class = forms.LeaseForm
    template_name = "leases/lease_edit.html"
    success_url = "/leases/leaselist/"

    def get_object(self):
        lease = get_object_or_404(models.Lease, pk=self.kwargs['pk'])
        return lease    
