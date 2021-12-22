from django.urls import path
from . import views

app_name = "leases"
urlpatterns = [
    path('', views.index, name='index'),
    path('roomcreate/',views.room_create,name='room_create'),
    path('create/',views.lease_create,name='lease_create'),
    path('list/',views.lease_list,name='lease_list'),

    path("roomcreate2/", views.RoomCreate.as_view(), name="room_create2"),
    path("roomlist/", views.RoomList.as_view(), name="room_list"),
    path("room/<int:pk>", views.RoomDetailView.as_view(), name="room_detail"),
    path("room_edit/<int:pk>/edit", views.RoomUpdate.as_view(), name="room_edit"),

    path("leaselist/", views.LeaseList.as_view(), name="leaselist"),
    path("lease/<int:pk>", views.LeaseDetailView.as_view(), name="lease_detail"),

    # API Json Data 
    path('test/',views.test,name='test'),
    path('type1-json/',views.get_json_type1_data,name='type1-json'),
    path('type2-json/<str:type1>/', views.get_json_type2_data, name='type2-json'),
    # path('type2-json/', views.get_json_type2_data, name='type2-json'),
    path('roomnumber-json/<str:type2>/', views.get_json_roomnumber_data, name='roomnumber-json'),
    path('save-lease-create/', views.save_lease_create, name='save-lease-create'),

    path('leases-json/',views.get_json_leases_data,name='leases-json'),
    # path('<int:post_id>/update', views.post_update, name="post_update"),
    # path('<int:post_id>/comment_create', views.comment_create, name='comment_create'),
    # path('<int:comment_id>/comment_delete', views.comment_delete, name="comment_delete"),

    path("lease_edit/<int:pk>/edit", views.LeaseUpdate.as_view(), name="lease_edit"),
]