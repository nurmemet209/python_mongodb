from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^detail/(?P<make>\w+)/(?P<model>([^\s]+))/(?P<year>\d{4})/$',
        views.detail),
    #url(r'^find/(?P<bolt>([^\s]+))/(?P<rim_diameter>([-+]?[0-9]*\.?[0-9]+))/(?P<rim_width>([-+]?[0-9]*\.?[0-9]+))/(?P<offset>([-+]?[0-9]*\.?[0-9]+))/$', views.get_suite_car_by_rim),
    url('findByRim/', views.get_suite_car_by_rim, name="findByRim"),
    url(r'^articles/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d+)/$',
        views.test),
]

# 3.1 url函数的第二个参数，表示视图函数，它的名字不是随便取的，必须要在views.py中真实存在，项目的每个应用下都会有一个views.py文件。
# 3.2 views.py文件中的视图函数，其第一个参数必须是HttpRequest对象。
# 3.2 name的作用主要体现在一个视图函数对应多个url请求的场景中，name可以用来唯一标识一个url，所以它必须全局唯一。