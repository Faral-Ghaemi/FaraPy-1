from django.urls import path
from . import views
urlpatterns = [


    path('', views.panel, name='panel'),
    path('gettask/', views.gettask, name='gettask'),
    path('taskstatus/<int:id>/', views.taskstatus, name='taskstatus'),
    path('posts/', views.pposts, name='posts'),
    path('ppostsUpdate/<int:pk>/', views.ppostsUpdate.as_view(), name='ppostsUpdate'),
    path('ppostsDelete/<int:pk>/', views.ppostsDelete.as_view(), name='ppostsDelete'),
    path('ppostsCreate/', views.ppostsCreate.as_view(), name='ppostsCreate'),

    path('category/', views.pcategory, name='category'),
    path('pcategoryUpdate/<int:pk>/', views.pcategoryUpdate.as_view(), name='pcategoryUpdate'),
    path('pcategoryDelete/<int:pk>/', views.pcategoryDelete.as_view(), name='pcategoryDelete'),
    path('pcategoryCreate/', views.pcategoryCreate.as_view(), name='pcategoryCreate'),

    path('slider/', views.pslider, name='slider'),
    path('psliderUpdate/<int:pk>/', views.psliderUpdate.as_view(), name='psliderUpdate'),
    path('psliderDelete/<int:pk>/', views.psliderDelete.as_view(), name='psliderDelete'),
    path('psliderCreate/', views.psliderCreate.as_view(), name='psliderCreate'),

    path('multimedia/', views.pmultimedia, name='multimedia'),
    path('pmultimediaUpdate/<int:pk>/', views.pmultimediaUpdate.as_view(), name='pmultimediaUpdate'),
    path('pmultimediaDelete/<int:pk>/', views.pmultimediaDelete.as_view(), name='pmultimediaDelete'),
    path('pmultimediaCreate/', views.pmultimediaCreate.as_view(), name='pmultimediaCreate'),

    path('ads/', views.pads, name='ads'),
    path('padsUpdate/<int:pk>/', views.padsUpdate.as_view(), name='padsUpdate'),
    path('padsDelete/<int:pk>/', views.padsDelete.as_view(), name='padsDelete'),
    path('padsCreate/', views.padsCreate.as_view(), name='padsCreate'),

    path('link/', views.plink, name='link'),
    path('plinkUpdate/<int:pk>/', views.plinkUpdate.as_view(), name='plinkUpdate'),
    path('plinkDelete/<int:pk>/', views.plinkDelete.as_view(), name='plinkDelete'),
    path('plinkCreate/', views.plinkCreate.as_view(), name='plinkCreate'),

    path('video/', views.pvideo, name='video'),
    path('pvideoUpdate/<int:pk>/', views.pvideoUpdate.as_view(), name='pvideoUpdate'),
    path('pvideoDelete/<int:pk>/', views.pvideoDelete.as_view(), name='pvideoDelete'),
    path('pvideoCreate/', views.pvideoCreate.as_view(), name='pvideoCreate'),

    path('form/', views.pform, name='form'),
    path('formUpdate/<int:pk>/', views.pformUpdate.as_view(), name='formUpdate'),
    path('formDelete/<int:pk>/', views.pformDelete.as_view(), name='formDelete'),

    path('addform/', views.addform, name='addform'),
    path('fields/<int:id>/', views.fields, name='fields'),
    path('addfield/<int:id>/', views.addfield, name='addfield'),
    path('addfieldt/<int:id>/', views.addfieldt, name='addfieldt'),
    path('df/<int:id>/', views.df, name='df'),
    path('da/<int:id>/', views.da, name='da'),
    path('dttf/<int:id>/', views.dtf, name='dtf'),
    path('answers/<int:id>/', views.panswers, name='panswers'),
    path('answer/<int:id>/', views.panswer, name='panswer'),
    path('setting/<int:pk>/', views.setting.as_view(), name='setting'),

    path('portable/', views.pportable, name='portable'),
    path('paycopen/', views.paycopen, name='paycopen'),

    path('Moshtarian/', views.Moshtarian, name='Moshtarian'),
    path('pMoshtariUpdate/<int:pk>/', views.pMoshtariUpdate.as_view(), name='pMoshtariUpdate'),
    path('pMoshtariDelete/<int:pk>/', views.pMoshtariDelete.as_view(), name='pMoshtariDelete'),
    path('pMoshtariCreate/', views.pMoshtariCreate.as_view(), name='pMoshtariCreate'),

    path('portableUpdate/<int:pk>/', views.portableUpdate.as_view(), name='portableUpdate'),
    path('portableDelete/<int:pk>/', views.portableDelete.as_view(), name='portableDelete'),
    path('portableCreate/', views.portableCreate, name='portableCreate'),

    path('Moshtariancopen/', views.Moshtariancopen, name='Moshtariancopen'),
    path('pmoshtaricopenDelete/<int:pk>/', views.pmoshtaricopenDelete.as_view(), name='pmoshtaricopenDelete'),
    path('pmoshtaricopenCreate/', views.pmoshtaricopenCreate.as_view(), name='pmoshtaricopenCreate'),

    path('safahat/', views.safahat, name='safahat'),
    path('psafahatUpdate/<int:pk>/', views.psafahatUpdate.as_view(), name='psafahatUpdate'),
    path('psafahatDelete/<int:pk>/', views.psafahatDelete.as_view(), name='psafahatDelete'),
    path('psafahatCreate/', views.psafahatCreate.as_view(), name='psafahatCreate'),

    path('task_manegar/', views.ptask_manegar, name='task_manegar'),
    path('time_cards/', views.time_cards, name='time_cards'),
    path('createtask/', views.createtask, name='createtask'),
    path('TimeUpdate/<int:pk>/', views.TimeUpdate.as_view(), name='TimeUpdate'),
    path('TimeDelete/<int:pk>/', views.TimeDelete.as_view(), name='TimeDelete'),
    path('TimeCreate/', views.TimeCreate.as_view(), name='TimeCreate'),
    path('req1/<int:id>/', views.req1, name='req1'),
    path('task_manegarUpdate/<int:pk>/', views.task_manegarUpdate.as_view(), name='task_manegarUpdate'),
    path('task_manegarDelete/<int:pk>/', views.task_manegarDelete.as_view(), name='task_manegarDelete'),
    path('task_manegarCreate/', views.task_manegarCreate, name='task_manegarCreate'),

    path('comment/', views.pcomment, name='comment'),
    path('req/<int:id>/', views.req, name='req'),
    path('commentDelete/<int:pk>/', views.commentDelete.as_view(), name='commentDelete'),

    path('menu/', views.menu, name='menu'),
    path('menus/<int:id>/', views.menus, name='menus'),
    path('dlmenu/<int:id>/', views.dlmenu, name='dlmenu'),
    path('sendcat/<int:id>/', views.sendcat, name='sendcat'),
    path('sendpage/<int:id>/', views.sendpage, name='sendpage'),
    path('sendlink/<int:id>/', views.sendlink, name='sendlink'),
    path('MenuUpdate/<int:pk>/', views.MenuUpdate.as_view(), name='MenuUpdate'),
    path('MenuDelete/<int:pk>/', views.MenuDelete.as_view(), name='MenuDelete'),

    path('themeeditor/', views.themeeditor, name='themeeditor'),
    path('themes/', views.themes, name='themes'),
    path('selecttheme/', views.selecttheme, name='selecttheme'),
    path('deltheme/', views.deltheme, name='deltheme'),
    path('newfile/', views.newfile, name='newfile'),
    path('newfolder/', views.newfolder, name='newfolder'),
    path('delfile/', views.delfile, name='delfile'),
    path('delfolder/', views.delfolder, name='delfolder'),
    path('upfile/', views.upfile, name='upfile'),
    path('tabupdate/', views.tabupdate, name='tabupdate'),
    path('commpresstheme/', views.commpresstheme, name='commpresstheme'),

    path('tickets/', views.tickets, name='tickets'),
    path('ticket/<int:id>/', views.ticket, name='ticket'),
    path('addticket/', views.addticket, name='addticket'),
    path('addsubticket/<int:id>/', views.addsubticket, name='addsubticket'),
    path('closeticket/<int:id>/', views.closeticket, name='closeticket'),
    path('TicketDelete/<int:pk>/', views.TicketDelete.as_view(), name='TicketDelete'),

]
