from django.db import models
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from ckeditor_uploader.fields import RichTextUploadingField
import re
from datetime import datetime, date,timedelta



class Ads(models.Model):
    image = models.ImageField(upload_to="ads/",verbose_name="Image")
    url = models.URLField()
    date = models.DateField(verbose_name="Start Date")
    EXdate = models.DateField(verbose_name="Expiration Date")
    title = models.CharField(max_length=200, verbose_name="Title")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name  ="Ads"
        verbose_name_plural = "Ads"

class Category(models.Model):
    pcategory =models.ForeignKey('Category',on_delete=models.SET_NULL,null=True,blank=True,verbose_name='Mother Category',related_name='Category')
    title = models.CharField(max_length=200, unique=True, verbose_name="Title")
    image = models.ImageField(upload_to="category/", verbose_name="Image")
    pcount = models.IntegerField(default=0,verbose_name="Number of Posts")
    html = models.CharField(max_length=200,default="category.html",verbose_name="Category File Name")
    htmlpost = models.CharField(max_length=200,default="post.html",verbose_name="File Name Read More of This Ccategory")

    def posts(self):
        p = self.post_set.all().count()
        self.pcount = p
        self.save()
        return p

    def __str__(self):
        return self.title

    class Meta:
        verbose_name  ="Category"
        verbose_name_plural = "Categories"


class Links(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name="Title")
    url = models.URLField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name  ="Link"
        verbose_name_plural = "Links"

STATUSTICKET = (
    (0,"Closed"),
    (1,"Open")
)
class Tickets(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    key = models.CharField(max_length=200, verbose_name="Key")
    description = models.TextField(verbose_name="Content")
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey('Portable', on_delete= models.CASCADE, null=True,verbose_name="User",)
    status = models.IntegerField(choices=STATUSTICKET, default=1, verbose_name="Status ")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name  ="Ticket"
        verbose_name_plural = "Tickets"

class SubTickets(models.Model):
    description = models.TextField(verbose_name="Content")
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey('Portable', on_delete= models.CASCADE, verbose_name="User",null = True)
    ticket = models.ForeignKey('Tickets', on_delete= models.CASCADE, verbose_name="Ticket",)

    def __str__(self):
        return self.ticket.title

    class Meta:
        verbose_name  ="SubTicket"
        verbose_name_plural = "SubTickets"


STATUS = (
    (0,"Draft"),
    (1,"Publish")
)
class Post(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name="Title")
    slug = models.SlugField(max_length=200, unique=True)
    demo = models.TextField(blank=False,verbose_name="Short explanation")
    author = models.ForeignKey('Portable', on_delete= models.CASCADE,related_name='blog_posts', verbose_name="Author")
    content = RichTextUploadingField(verbose_name="Content")
    view = models.IntegerField(default=0, verbose_name="View")
    category = models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True,verbose_name="Category")
    sartitr = models.BooleanField(default=0, verbose_name="Triggear")
    com = models.BooleanField(default=0, verbose_name="Users Can Comment")
    created_date = models.DateField(verbose_name='Date', null=True)
    status = models.IntegerField(choices=STATUS, default=1, verbose_name="Status ")
    image = models.ImageField(upload_to="post/", verbose_name="Image")
    form = models.ForeignKey('Form', on_delete= models.CASCADE, verbose_name="Form",null=True,blank=True)
    barchasb = models.TextField(verbose_name="Tags",null=True,blank=True)
    class Meta:
        ordering = ['-created_date']
        verbose_name  ="Post"
        verbose_name_plural="Posts"
    def __str__(self):
        return self.title

    def bar(self):
        s = self.barchasb
        ss = re.split(', |، ',s)

        return ss

    def url(self):
        return '/post/'+self.slug+'/'

class Safahat(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name="Title")
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey('Portable', on_delete= models.CASCADE, verbose_name="Author")
    content = RichTextUploadingField(verbose_name="Content")
    view = models.IntegerField(default=0, verbose_name="View")
    created_date = models.DateField(verbose_name='Date', null=True)
    image = models.ImageField(upload_to="post/", verbose_name="Image")
    form = models.ForeignKey('Form', on_delete= models.CASCADE, verbose_name="Form",null=True)
    html = models.CharField(max_length=200,default="page.html",verbose_name="Format File Name")

    class Meta:
        ordering = ['-created_date']
        verbose_name  ="Pages"
        verbose_name_plural="Pages"
    def __str__(self):
        return self.title

    def url(self):
        return '/page/'+self.slug+'/'

class Slider(models.Model):
    name = models.CharField(max_length=200,verbose_name="Title")
    image = models.ImageField(upload_to="slider/", verbose_name="Image")
    date = models.DateField(verbose_name='Date', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name="Slider"
        verbose_name_plural="Sliders"

class Comment(models.Model):
    name = models.CharField(max_length=200,verbose_name="Name")
    email = models.EmailField( verbose_name="Email")
    text = models.TextField(blank=False,verbose_name="Text ")
    post = models.ForeignKey('Post', on_delete=models.CASCADE, verbose_name="Post")
    date = models.DateField(verbose_name='Date', null=True)
    STATUS ={
    (0,'Not confirmed'),
    (1,'Confirmed'),
    }
    status = models.IntegerField(choices=STATUS,default=0, verbose_name='Status')

    class Meta:
        ordering = ['-date']
        verbose_name="Comment"
        verbose_name_plural="Comments"

    def __str__(self):
        return self.name

class Multimedia(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name="Title")
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE, verbose_name="Author")
    updated_on = models.DateTimeField(auto_now= True, verbose_name="Update")
    content = RichTextUploadingField(verbose_name="Content")
    created_date = models.DateField(verbose_name='Date', null=True)
    status = models.IntegerField(choices=STATUS, default=0, verbose_name="Status")
    image = models.ImageField(upload_to="multi/", verbose_name="Image")

    class Meta:
        ordering = ['-created_date']
        verbose_name="Multimedia"
        verbose_name_plural="Multimedia"


    def __str__(self):
        return self.title
class Form(models.Model):
    title = models.CharField(max_length=200,  verbose_name="Title")

    def __str__(self):
        return self.title

Type = (
    ('email',"Email"),
    ('number',"Number"),
    ('password',"Password"),
    ('text',"Text"),
)
class Field(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    type = models.CharField(choices=Type, default='text', verbose_name="Type of Field",max_length=10)
    form = models.ForeignKey(Form, on_delete= models.CASCADE, verbose_name="Form")

    def __str__(self):
        return self.title

class TextField(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    form = models.ForeignKey(Form, on_delete= models.CASCADE, verbose_name="Form")

    def __str__(self):
        return self.title

class Answer(models.Model):
    date = models.DateField(verbose_name='Date', null=True)
    form = models.ForeignKey(Form, on_delete= models.CASCADE, verbose_name="Form")


class AnswerField(models.Model):
    title = models.TextField( verbose_name="Title")
    field = models.ForeignKey(Field, on_delete= models.CASCADE, verbose_name="Form")
    answer = models.ForeignKey(Answer, on_delete= models.CASCADE, verbose_name="Answer")

    def __str__(self):
        return self.title

class AnswerTextField(models.Model):
    title = models.TextField( verbose_name="Title")
    field = models.ForeignKey(TextField, on_delete= models.CASCADE, verbose_name="Form")
    answer = models.ForeignKey(Answer, on_delete= models.CASCADE, verbose_name="Answer")

    def __str__(self):
        return self.title

class Setting (models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    introduction = models.TextField(verbose_name="Short Introduction")
    email = models.EmailField(verbose_name='Email')
    instagram = models.URLField(null=True,blank=True,default='instagram.com/',verbose_name='Instagram')
    facebook = models.URLField(null=True,blank=True,default='facebook.com/',verbose_name='Face Book')
    linkedin = models.URLField(null=True,blank=True,default='linkedin.com/',verbose_name='Linkedin')
    twitter = models.URLField(null=True,blank=True,default='twitter.com/',verbose_name='Twitter')
    whatsapp = models.URLField(null=True,blank=True,verbose_name='Watsapp')
    telgram = models.URLField(null=True,blank=True,verbose_name='Telegram')
    aboutus = models.TextField(null=True,verbose_name='About us')
    address = models.CharField(max_length=200, verbose_name='Address',null=True)
    logo = models.FileField(upload_to="logo/",verbose_name="Logo",default='logo.jpg')
    city = models.CharField(max_length=200, verbose_name='City',default='tehran',null=True)
    tel_no = models.IntegerField(verbose_name='Tel',null=True)
    api = models.CharField(max_length= 200,verbose_name='Api kavenegar',null=True)
    createdate = models.DateField(verbose_name='License create date',null=True)
    expdate = models.DateField(verbose_name='License expiration date',null=True)
    form = models.BooleanField(default=1, verbose_name='Form')
    ads = models.BooleanField(default=1, verbose_name='Ads')
    protable = models.BooleanField(default=1, verbose_name='Users')
    moshtari = models.BooleanField(default=1, verbose_name='Customers Club')
    video = models.BooleanField(default=1, verbose_name='Video')
    safahat = models.BooleanField(default=1, verbose_name='Pages')
    task_manegar = models.BooleanField(default=1, verbose_name='Task manager')

    theme = models.ForeignKey('Theme',on_delete=models.SET_NULL,null=True,verbose_name='Format')

    def __str__(self):
        return self.title

class Portable(models.Model):
    full_name = models.CharField(max_length= 200,verbose_name='Full Name')
    SEX ={
    ( 0 , 'Female'),
    ( 1 , 'Male')
    }
    sex = models.IntegerField(choices=SEX,default=1,verbose_name='Sex')
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,verbose_name='Username',related_name='Userportable')
    image = models.ImageField(upload_to="images/",verbose_name='Picture',default='user.png')
    dpost = models.BooleanField(default=1,verbose_name='Access to Posts')
    dcomment = models.BooleanField(default=1,verbose_name='Access to Comments')
    dmultimedia = models.BooleanField(default=1,verbose_name='Access to Multimedia')
    dvideo = models.BooleanField(default=1,verbose_name='Access to Video')
    dcategory = models.BooleanField(default=1,verbose_name='Access to Categories')
    dsafahat = models.BooleanField(default=1,verbose_name='Access to Pages')
    dthemeeditor = models.BooleanField(default=1, verbose_name='Edit Format')
    dmenu = models.BooleanField(default=1,verbose_name='Access to MenuMaker')
    dslider = models.BooleanField(default=1,verbose_name='Access to Sliders')
    dtaskmanager = models.BooleanField(default=1,verbose_name='Access to TaskManager')
    dlink = models.BooleanField(default=1,verbose_name='Access to Links')
    dads = models.BooleanField(default=1,verbose_name='Access to Ads')
    dform = models.BooleanField(default=1,verbose_name='Access to FormMaker')
    dhavadaran = models.BooleanField(default=1,verbose_name='Access to Customers')
    dkarbaran = models.BooleanField(default=1,verbose_name='Access to Users')
    dsetting = models.BooleanField(default=1,verbose_name='Access to Setting')

    def __str__(self):
        return self.full_name

class Theme(models.Model):
    name = models.CharField(max_length= 200,verbose_name='Format Name')
    image = models.ImageField(upload_to="themes/", verbose_name='Picture', default='theme-default-thumb.png')


    def __str__(self):
            return self.name



class Video(models.Model):
    mozo = models.CharField(max_length= 200,verbose_name='Subject')
    tozihat = models.TextField(verbose_name='Text')
    video = models.FileField(upload_to="video/",verbose_name='Video')
    def __str__(self):
        return self.mozo


class Tabs(models.Model):
    fontsize = models.IntegerField(default=15, verbose_name='Fontsize')
    autosave = models.IntegerField(default=0, verbose_name='autosave')
    portable = models.ForeignKey(Portable, on_delete= models.CASCADE, verbose_name="Portable",null=True)

    def __str__(self):
        return str(self.fontsize)

class Moshtari(models.Model):
    full_name = models.CharField(max_length= 200,verbose_name='Full Name')
    email = models.EmailField(verbose_name='Email',null=True,blank=True)
    phone = models.CharField(max_length=100,verbose_name='Mobile Number')
    birthdate = models.DateField(verbose_name='Date of birth',null=True,blank=True)
    def __str__(self):
        return self.full_name


class Copen(models.Model):
    copeni = models.IntegerField(default=0, verbose_name='Percentage of Coupons')
    moshtari = models.ForeignKey(Moshtari, on_delete= models.CASCADE, verbose_name="Customer",null=True)
    def __str__(self):
        return self.moshtari.full_name

class Task_manegar(models.Model):
    title = models.CharField(max_length=200,  verbose_name="Title")
    sharh = models.TextField(verbose_name='Description',null=True,blank=True)
    created_time = models.DateField(verbose_name='Start date', null=True,default=datetime.today())
    end_time = models.DateField(verbose_name='Finish date', null=True,default=datetime.today())
    portable = models.ForeignKey('Portable', on_delete= models.CASCADE, verbose_name="Author")
    STATUS ={
    ( 0 , 'To Do'),
    ( 1 , 'In progress'),
    ( 3 , 'Done!')
    }
    status = models.IntegerField(choices=STATUS,default=0,verbose_name='Status')
    def __str__(self):
        return self.title


class Time(models.Model):

    in_date = models.DateField(verbose_name='Login Date',)
    out_date= models.DateField(null=True,verbose_name='Logout Date',)
    in_time = models.TimeField(verbose_name='Clock-in')
    out_time = models.TimeField(null=True,verbose_name='Clock-out')
    portable = models.ForeignKey('Portable', on_delete= models.CASCADE, verbose_name="Author")
    STATUS ={
    ( 0 , 'On Duty'),
    ( 1 , 'Out of Duty'),

    }
    status = models.IntegerField(choices=STATUS,default=0,verbose_name='Status')
    def __int__(self):
        return self.in_time

    def time(self):
        if self.status == 1 and self.in_date == self.out_date:

            hour= datetime.combine(date.today(), self.out_time) - datetime.combine(date.today(), self.in_time)
            return hour.seconds
        else:
            return 0

class Menu(models.Model):
    title = models.CharField(max_length=200,  verbose_name="Title")
    STATUS ={
    ( 0 , 'Primary Menu'),
    ( 1 , 'Secondry Menu')
    }
    status = models.IntegerField(choices=STATUS,default=0,verbose_name='Status')

class SubMenu(models.Model):
    title = models.TextField( verbose_name="Title")
    pos = models.IntegerField(default=1, verbose_name='Position')
    menu = models.ForeignKey(Menu, on_delete= models.CASCADE, verbose_name="Menu")
    sub = models.ForeignKey('SubMenu', on_delete= models.CASCADE, verbose_name="SubMenu",null=True,related_name='menuu')
    STATUS ={
    ( 0 , 'Category'),
    ( 1 , 'Address'),
    ( 2 , 'Page')
    }
    status = models.IntegerField(choices=STATUS,default=0,verbose_name='Status')
    def __str__(self):
        return self.title

    def ismom(self):
        if self.sub == None:
            return 1
        else :
            return 0

class SubCat(SubMenu):
    url = models.ForeignKey(Category,on_delete=models.CASCADE,verbose_name="Category")

    def furl(self):
        url = '/category/' + str(self.url.id) + '/'
        return url

class SubUrl(SubMenu):
    url = models.URLField(verbose_name='Url')

    def furl(self):
        return self.url


class SubPage(SubMenu):
    url = models.ForeignKey(Safahat,on_delete=models.CASCADE,verbose_name="Pages")

    def furl(self):
        url = '/page/' + str(self.url.id)  + '/'
        return url
