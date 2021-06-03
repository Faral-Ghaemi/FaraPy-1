from __future__ import division, unicode_literals
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.files.storage import FileSystemStorage
from . import models
from django.template import loader
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from datetime import date, timedelta
from django.contrib.auth import authenticate, login, logout
from kavenegar import *
import datetime
from django.utils import autoreload
from django.core.paginator import Paginator
from itertools import chain
from os import listdir
from os.path import isfile, join, isdir
import os
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import zipfile
import shutil
import json
import sys
from .api import API as dcapi
SupportUrl='https://farapy.ir'

try:
    import json
except ImportError:
    import simplejson as json

today = date.today()
try:
    the = models.Setting.objects.last()
    theme = the.theme.name

    setting = models.Setting.objects.last()
    send = {
        'title': setting.title,
        'expdate': setting.expdate,
        'today': today,
        'email': setting.email,
        'posts': models.Post.objects.all().count()
    }
    data = urllib.parse.urlencode(send).encode()
    req = urllib.request.Request(SupportUrl+'/setin/', data=data)
    resp = urllib.request.urlopen(req)
    dom = resp.read()
    jdate = json.loads(dom)['expdate']
    jdate = jdate.split('-')
    data = datetime.date(int(jdate[0]), int(jdate[1]), int(jdate[2]))
    setting.expdate = data
    lin = data - today
    setting.save()
    edays = lin.days
except Exception as e:
    theme = 'install'

edays = 100

def install(request):
    if not models.Setting.objects.exists():
        if request.POST:
            form = request.POST
            title = form.get('title')
            email = form.get('email')
            introduction = form.get('introduction')
            city = form.get('city')
            formm = form.get('form')
            ads = form.get('ads')
            protable = form.get('protable')
            themeid = form.get('theme')
            username = form.get('username')
            password = form.get('password')
            today = date.today()
            ex = today + datetime.timedelta(days=365)
            theme = models.Theme.objects.get(id=themeid)
            settingg = models.Setting.objects.create(title=title, email=email, introduction=introduction,
                                                     city=city, createdate=today, expdate=ex,
                                                     form=formm, ads=ads, protable=protable,
                                                     theme=theme)
            u = User.objects.create_superuser(username, email, password)
            p = models.Portable.objects.create(full_name=username, user=u)
            return HttpResponseRedirect('/panel/')
        else:

            t = models.Theme.objects.get_or_create(name='default')
            themes = models.Theme.objects.all()

            context = {
                'themes': themes,

            }
            template = loader.get_template('panel/install.html')
            return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('/')


def access(request):
    Category = models.Category.objects.all()
    context = {
        'category': category,

    }
    template = loader.get_template('access.html')
    return HttpResponse(template.render(context, request))


def index(request):
    the = models.Setting.objects.last()
    theme = the.theme.name
    sliders = models.Slider.objects.all().order_by('-id')[:5]
    video = models.Video.objects.last()

    hotnews = models.Post.objects.all().order_by('-id')
    paginator = Paginator(hotnews, 5)  # Show 25 contacts per page.
    categor3 = models.Category.objects.all().order_by('-pcount')[:3]
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'categor3': categor3,
        'hotnewss': page_obj,
        'sliders': sliders,

        'video': video,

    }
    # template = 'themes/'+str(theme)+'/index.html'
    template = loader.get_template(str(theme) + '/index.html')
    return HttpResponse(template.render(context, request))


@csrf_exempt
def login_user(request):
    logout(request)
    username = password = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if edays > 0:
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/panel/')

    template = loader.get_template('login.html')
    context = {}
    return HttpResponse(template.render(context, request))


def category(request, id):
    the = models.Setting.objects.last()
    theme = the.theme.name
    c = models.Category.objects.get(id=id)
    natije = 0
    posts = c.post_set.all()
    try:
        for p in c.category.all():
            posts = list(chain(posts, p.post_set.all()))
    except Exception as e:
        natije = e
    popular = c.post_set.all().order_by('-view')
    hotnews = models.Post.objects.all().order_by('-id')
    paginator = Paginator(posts, 5)  # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'natije':natije,
        'p': c,
        'category_posts': page_obj,
        'popular': popular,

    }
    template = loader.get_template(str(theme) + '/' + str(c.html))
    return HttpResponse(template.render(context, request))


def post(request, id):
    the = models.Setting.objects.last()
    theme = the.theme.name
    try:
        p = models.Post.objects.get(id=int(id))
    except:
        p = models.Post.objects.get(slug=id)
    p.view += 1
    p.save()
    pop = models.Post.objects.all().order_by('-view')[:7]
    new = models.Post.objects.all().order_by('-id')[:7]
    sar = models.Post.objects.filter(sartitr=1)[:7]
    com = models.Comment.objects.filter(status=1, post=p)
    context = {
        'com': com,
        'p': p,
        'pop': pop,
        'sar': sar,
        'new': new,

    }
    template = loader.get_template(str(theme) + '/' + str(p.category.htmlpost))
    return HttpResponse(template.render(context, request))


def page(request, id):
    the = models.Setting.objects.last()
    theme = the.theme.name
    try:
        p = models.Safahat.objects.get(id=int(id))
    except:
        p = models.Safahat.objects.get(slug=id)
    p.view += 1
    p.save()
    pop = models.Post.objects.all().order_by('-view')[:7]
    new = models.Post.objects.all().order_by('-id')[:7]
    sar = models.Post.objects.filter(sartitr=1)[:7]

    context = {

        'p': p,
        'pop': pop,
        'sar': sar,
        'new': new,

    }
    template = loader.get_template(str(theme) + '/' + str(p.html))
    return HttpResponse(template.render(context, request))


def multi(request, id):
    the = models.Setting.objects.last()
    theme = the.theme.name
    p = models.Multimedia.objects.get(id=id)

    context = {
        'p': p,

    }
    template = loader.get_template(str(theme) + '/post.html')
    return HttpResponse(template.render(context, request))


def search(request):
    the = models.Setting.objects.last()
    theme = the.theme.name
    s = request.POST.get('s')
    c = models.Post.objects.filter(content__icontains=s, title__icontains=s)

    paginator = Paginator(c, 9)  # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        's': s,
        'posts': page_obj,
    }
    template = loader.get_template(str(theme) + '/search.html')
    return HttpResponse(template.render(context, request))


@csrf_exempt
def getmem(request):
    full_name = request.POST.get('full_name')
    phone = request.POST.get('phone')
    try:
        s = models.Moshtari.objects.get(phone=phone)
    except Exception as e:
        c = models.Moshtari.objects.create(phone=phone, full_name=full_name)

    return HttpResponseRedirect("/")


@csrf_exempt
def getcom(request, id):
    post = models.Post.objects.get(id=id)
    email = request.POST.get('email')
    name = request.POST.get('name')
    text = request.POST.get('text')
    c = models.Comment.objects.create(email=email, name=name, text=text, post=post, date=today)
    return HttpResponseRedirect("/post/" + str(post.id) + '/')


@csrf_exempt
def dc(request, id):
    com = models.Comment.objects.get(id=id)
    post = com.post
    com.delete()
    return HttpResponseRedirect('/post/'+post.slug+'/')


# ------------------------ panel codes

@login_required(login_url='/login/')
def panel(request):
    Media = []
    url = 'https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey=at_jVykwS1vykSwZK0ji9pWDi72ePaoJ&domainName='
    url += request.META['HTTP_HOST']
    try:
        natije = 0
        f = urllib.request.urlopen(url)
        dom = ET.parse(f)  # parse the data
        link = dom.getroot()
        cat = [items for items in link]
        for items in link:
            Media.append(items)
        time = 0
        try:

            for x in Media[3]:
                if x.tag == 'expiresDate':
                    time = x.text
            data = 0
            dominexpired = -1
            if time != 0:
                time = time.split('T')

                jdate = time[0]
                jdate = jdate.split('-')
                data = datetime.date(int(jdate[0]), int(jdate[1]), int(jdate[2]))
                dominexpired = data - date.today()
                dominexpired = dominexpired.days
        except Exception as e:
            natije = e
            dominexpired = 360

    except Exception as e:
        natije = e
        dominexpired = 360
    karbaran = models.Portable.objects.all().count()
    p = models.Post.objects.all().count()
    m = models.Multimedia.objects.all().count()
    categories = models.Category.objects.all().count()
    s = models.Safahat.objects.all().count()
    l = models.Links.objects.all().count()
    a = models.Ads.objects.all().count()
    comments = models.Comment.objects.filter(status=0)
    answers = models.Answer.objects.filter(date=date.today()).count()
    customer = models.Moshtari.objects.all().count()

    pp = models.Post.objects.filter(status=0).count()
    if p != 0:
        dpp = pp * 100 // p
    else:
        dpp = 0
    mp = models.Multimedia.objects.filter(status=0).count()
    if m != 0:
        dmp = mp * 100 // m
    else:
        dmp = 0

    today = date.today()
    adsExp = models.Ads.objects.filter(EXdate__gte=today).count()
    if a != 0:
        aa = adsExp * 100 // a
    else:
        aa = 0
    setting = models.Setting.objects.last()
    lin = setting.expdate - today
    days = lin.days
    to = today - timedelta(days=30)

    x = setting.expdate - setting.createdate
    y = x.days
    if y != 0:
        q = days * 100 // y
    else:
        q = 0
    posts = models.Post.objects.all()
    dp = []
    for x in range(1, 13):
        sum = 0
        #    ssum = 0
        for s in posts:
            if s.created_date.year == today.year:
                if s.created_date.month == x:
                    sum += 1
        #    ssum  = sum*100//p
        dp.append(sum)
    ww = models.Category.objects.all().order_by('-pcount')
    portable = models.Portable.objects.get(user=request.user)
    flag = 0
    times = models.Time.objects.filter(portable=portable)
    induty = 0
    if times.count() == 0:
        flag = 1
    else:
        t = models.Time.objects.filter(portable=portable).last()
        if t.status == 1:
            flag = 1
        else:
            induty = t
            flag = 0
    task_manegar = models.Task_manegar.objects.all()

    tt = models.Time.objects.all()
    inprogress = models.Task_manegar.objects.filter(status=1, portable=portable).order_by('-id')

    tasks = models.Task_manegar.objects.filter(status=0, portable=portable).order_by('-id')
    context = {
        'natije': natije,
        'inprogress':inprogress,
        'tasks': tasks,
        'categories': categories,
        'customer': customer,
        'answers': answers,
        'comments': comments,
        'induty': induty,
        'tt': tt,
        'flag': flag,
        'task_manegar': task_manegar,
        'dominexpired': dominexpired,
        'q': q,
        'dp': dp,
        'ww': ww,
        'x': x,
        'y': y,
        'days': days,
        'lin': lin,
        'karbaran': karbaran,
        'p': p,
        'm': m,
        'l': l,
        'a': a,
        'dpp': dpp,
        'dmp': dmp,
        'adsExp': adsExp,
        'aa': aa,
    }
    template = loader.get_template('panel/panel.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='/login/')
@csrf_exempt
def gettask(request):
    title = request.POST.get('title')
    portable = models.Portable.objects.get(user=request.user)
    t = models.Task_manegar.objects.create(title=title, portable=portable)
    return HttpResponseRedirect("/panel/")


@login_required(login_url='/login/')
@csrf_exempt
def taskstatus(request, id):
    portable = models.Portable.objects.get(user=request.user)
    t = models.Task_manegar.objects.get(id=id, portable=portable)
    t.status = 3
    t.save()
    return HttpResponseRedirect("/panel/")


@login_required(login_url='/login/')
def pposts(request):
    portable = models.Portable.objects.get(user=request.user)
    if portable.dpost == 1:
        posts = models.Post.objects.all().order_by('-id')

        context = {
            'posts': posts,

        }
        template = loader.get_template('panel/postlist.html')
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('/access/')


class ppostsUpdate(LoginRequiredMixin, generic.UpdateView):
    model = models.Post
    fields = ['title', 'demo', 'slug', 'content', 'category', 'sartitr', 'status', 'image', 'created_date', 'form',
              'barchasb', 'com']
    success_url = reverse_lazy('posts')


class ppostsDelete(LoginRequiredMixin, generic.DeleteView):
    model = models.Post
    success_url = reverse_lazy('posts')


class ppostsCreate(LoginRequiredMixin, generic.CreateView):
    model = models.Post
    success_url = reverse_lazy('posts')
    fields = ['title', 'demo', 'slug', 'content', 'category', 'sartitr', 'status', 'image', 'created_date', 'form',
              'barchasb', 'com']

    def form_valid(self, form):
        form.instance.author = models.Portable.objects.get(user=self.request.user)
        return super().form_valid(form)



@login_required(login_url='/login/')
def pcategory(request):
    portable = models.Portable.objects.get(user=request.user)
    if portable.dcategory == 1:
        category = models.Category.objects.all().order_by('-id')
        context = {
            'category': category,

        }
        template = loader.get_template('panel/category.html')
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('/access/')


class pcategoryCreate(LoginRequiredMixin, generic.CreateView):
    model = models.Category
    fields = ['pcategory', 'title', 'image', 'html', 'htmlpost']
    success_url = reverse_lazy('category')


class pcategoryUpdate(LoginRequiredMixin, generic.UpdateView):
    model = models.Category
    fields = ['pcategory', 'title', 'image', 'html', 'htmlpost']
    success_url = reverse_lazy('category')


class pcategoryDelete(LoginRequiredMixin, generic.DeleteView):
    model = models.Category
    success_url = reverse_lazy('category')


@login_required(login_url='/login/')
def pslider(request):
    portable = models.Portable.objects.get(user=request.user)
    if portable.dslider == 1:
        slider = models.Slider.objects.all().order_by('-id')
        context = {
            'slider': slider,

        }
        template = loader.get_template('panel/slider.html')
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('/access/')


class psliderUpdate(LoginRequiredMixin, generic.UpdateView):
    model = models.Slider
    fields = ['name', 'image', 'date']
    success_url = reverse_lazy('slider')


class psliderDelete(LoginRequiredMixin, generic.DeleteView):
    model = models.Slider
    success_url = reverse_lazy('slider')


class psliderCreate(LoginRequiredMixin, generic.CreateView):
    model = models.Slider
    fields = ['name', 'date', 'image']
    success_url = reverse_lazy('slider')


@login_required(login_url='/login/')
def pmultimedia(request):
    portable = models.Portable.objects.get(user=request.user)
    if portable.dmultimedia == 1:
        multimedia = models.Multimedia.objects.all().order_by('-id')
        context = {
            'multimedia': multimedia,

        }
        template = loader.get_template('panel/multimedia.html')
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('/access/')


class pmultimediaUpdate(LoginRequiredMixin, generic.UpdateView):
    model = models.Multimedia
    fields = ['title', 'slug', 'content', 'status', 'image']
    success_url = reverse_lazy('multimedia')


class pmultimediaDelete(LoginRequiredMixin, generic.DeleteView):
    model = models.Multimedia
    success_url = reverse_lazy('multimedia')


class pmultimediaCreate(LoginRequiredMixin, generic.CreateView):
    model = models.Multimedia
    fields = ['title', 'slug', 'author', 'created_date', 'status', 'image', 'content']
    success_url = reverse_lazy('multimedia')


@login_required(login_url='/login/')
def pform(request):
    portable = models.Portable.objects.get(user=request.user)
    if portable.dform == 1:
        setting = models.Setting.objects.last()
        if setting.form:
            form = models.Form.objects.all().order_by('-id')
            context = {
                'form': form,

            }
            template = loader.get_template('panel/form.html')
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponseRedirect('/access/')
    else:
        return HttpResponseRedirect('/access/')


class pformUpdate(LoginRequiredMixin, generic.UpdateView):
    model = models.Form
    fields = ['title']
    success_url = reverse_lazy('form')


class pformDelete(LoginRequiredMixin, generic.DeleteView):
    model = models.Form
    success_url = reverse_lazy('form')


@login_required(login_url='/login/')
def pads(request):
    portable = models.Portable.objects.get(user=request.user)
    if portable.dads == 1:
        setting = models.Setting.objects.last()
        if setting.ads:
            ads = models.Ads.objects.all().order_by('-id')
            context = {
                'ads': ads,

            }
            template = loader.get_template('panel/ads.html')
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponseRedirect('/access/')

    else:
        return HttpResponseRedirect('/access/')


class padsUpdate(LoginRequiredMixin, generic.UpdateView):
    model = models.Ads
    fields = ['title', 'image', 'url', 'date', 'EXdate']
    success_url = reverse_lazy('ads')


class padsDelete(LoginRequiredMixin, generic.DeleteView):
    model = models.Ads
    success_url = reverse_lazy('ads')


class padsCreate(LoginRequiredMixin, generic.CreateView):
    model = models.Ads
    fields = ['title', 'image', 'url', 'date', 'EXdate']
    success_url = reverse_lazy('ads')


@login_required(login_url='/login/')
def addform(request):
    portable = models.Portable.objects.get(user=request.user)
    if portable.dform == 1:
        setting = models.Setting.objects.last()
        if setting.form:
            if request.method == 'POST':
                form = request.POST
                title = form.get('title')
                form = models.Form.objects.create(title=title)
                return HttpResponseRedirect('/panel/fields/' + str(form.id) + '/')

            else:

                context = {

                }
                template = loader.get_template('panel/addform.html')
                return HttpResponse(template.render(context, request))
        else:
            return HttpResponseRedirect('/access/')
    else:
        return HttpResponseRedirect('/access/')


@login_required(login_url='/login/')
def fields(request, id):
    form = models.Form.objects.get(id=id)
    context = {
        'form': form,

    }
    template = loader.get_template('panel/fields.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='/login/')
@csrf_exempt
def addfield(request, id):
    if request.method == 'POST':
        form = request.POST
        title = form.get('title')
        type = form.get('type')
        form = models.Form.objects.get(id=id)
        field = models.Field.objects.create(title=title, form=form, type=type)
        return HttpResponse("1")


@login_required(login_url='/login/')
@csrf_exempt
def addfieldt(request, id):
    if request.method == 'POST':
        form = request.POST
        title = form.get('titlet')

        form = models.Form.objects.get(id=id)
        field = models.TextField.objects.create(title=title, form=form)
        return HttpResponse("1")


@login_required(login_url='/login/')
def df(request, id):
    form = models.Field.objects.get(id=id)
    idd = form.form.id
    form.delete()

    return HttpResponseRedirect("/panel/fields/" + str(idd) + "/")


@login_required(login_url='/login/')
def da(request, id):
    answer = models.Answer.objects.get(id=id)
    idd = answer.form.id
    for a in answer.answerfield_set.all():
        a.delete()

    for a in answer.answertextfield_set.all():
        a.delete()

    answer.delete()
    return HttpResponseRedirect("/panel/answers/" + str(idd) + "/")


@login_required(login_url='/login/')
def dtf(request, id):
    form = models.TextField.objects.get(id=id)
    idd = form.form.id
    form.delete()

    return HttpResponseRedirect("/panel/fields/" + str(idd) + "/")


@login_required(login_url='/login/')
def panswers(request, id):
    form = models.Form.objects.get(id=id)
    context = {
        'form': form,

    }
    template = loader.get_template('panel/answers.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='/login/')
def panswer(request, id):
    a = models.Answer.objects.get(id=id)
    context = {
        'a': a,

    }
    template = loader.get_template('panel/answer.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='/login/')
def getanswer(request, id):
    if request.method == 'POST':
        formm = request.POST
        form = request.POST
        form = models.Form.objects.get(id=id)
        answer = models.Answer.objects.create(date=today, form=form)
        for f in form.field_set.all():
            ff = f.id
            x = formm.get(str(ff))
            answerfield = models.AnswerField.objects.create(title=x, answer=answer, field=f)
        for f in form.textfield_set.all():
            ff = f.id
            x = formm.get(str(ff))
            answerfield = models.AnswerTextField.objects.create(title=x, answer=answer, field=f)

        return HttpResponseRedirect("/")


class setting(LoginRequiredMixin, generic.UpdateView):
    model = models.Setting
    fields = ['title', 'introduction', 'email', 'aboutus', 'address', 'logo', 'tel_no', 'api',
              'city', 'instagram', 'facebook', 'linkedin', 'twitter', 'whatsapp', 'telgram', ]
    success_url = reverse_lazy('panel')


@login_required(login_url='/login/')
def pportable(request):
    portable = models.Portable.objects.get(user=request.user)
    if portable.dkarbaran == 1:
        setting = models.Setting.objects.last()
        if setting.protable:
            portable = models.Portable.objects.all()

            context = {
                'portable': portable,
            }
            template = loader.get_template('panel/portable.html')
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponseRedirect('/access/')
    else:
        return HttpResponseRedirect('/access/')


class portableUpdate(LoginRequiredMixin, generic.UpdateView):
    model = models.Portable
    fields = ['full_name', 'sex', 'image', 'dthemeeditor',
              'dpost', 'dcomment', 'dmultimedia', 'dvideo', 'dcategory', 'dsafahat', 'dmenu', 'dslider',
              'dtaskmanager', 'dlink',
              'dads', 'dform', 'dhavadaran', 'dkarbaran', 'dsetting', ]
    success_url = reverse_lazy('portable')


class portableDelete(LoginRequiredMixin, generic.DeleteView):
    model = models.Portable
    success_url = reverse_lazy('portable')


@login_required(login_url='/login/')
@csrf_exempt
def portableCreate(request):
    if request.method == 'POST':
        form = request.POST
        full_name = form.get('full_name')
        username = form.get('username')
        password = form.get('password')
        email = form.get('email')

        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()

            if request.FILES:
                image = request.FILES['image']
                portabli = models.Portable.objects.create(full_name=full_name, user=user, image=image, )
                portabli.save()
            else:
                portabli = models.Portable.objects.create(full_name=full_name, user=user, )
                portabli.save()
            return HttpResponseRedirect('/panel/portable/')
        except Exception as e:
            natije = e
            context = {
                'natije': natije,
            }
            template = loader.get_template('panel/cportable.html')
            return HttpResponse(template.render(context, request))

    else:
        context = {

        }
        template = loader.get_template('panel/cportable.html')
        return HttpResponse(template.render(context, request))


@login_required(login_url='/login/')
def plink(request):
    portable = models.Portable.objects.get(user=request.user)
    if portable.dlink == 1:
        link = models.Links.objects.all().order_by('-id')

        context = {
            'link': link,
        }
        template = loader.get_template('panel/link.html')
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('/access/')


class plinkUpdate(LoginRequiredMixin, generic.UpdateView):
    model = models.Links
    fields = ['title', 'url']
    success_url = reverse_lazy('link')


class plinkDelete(LoginRequiredMixin, generic.DeleteView):
    model = models.Links
    success_url = reverse_lazy('link')


class plinkCreate(LoginRequiredMixin, generic.CreateView):
    model = models.Links
    fields = ['url', 'title']
    success_url = reverse_lazy('link')


@login_required(login_url='/login/')
def Moshtarian(request):
    portable = models.Portable.objects.get(user=request.user)
    if portable.dhavadaran == 1:
        setting = models.Setting.objects.last()
        if setting.moshtari:
            moshtari = models.Moshtari.objects.all().order_by('-id')
            setting = models.Setting.objects.last()

            natije = 0
            if request.POST:
                text = request.POST.get('text')
                phone = []
                for x in moshtari:
                    phone.append(x.phone)
                try:
                    api = KavenegarAPI(setting.api)
                    params = {
                        # 'sender': '10004346',
                        'receptor': phone,
                        'message': text,
                    }
                    response = api.sms_send(params)
                    print(str(response))
                except APIException as e:
                    print(str(e))
                except HTTPException as e:
                    print(str(e))

                natije = 'This Message Sent! '
            context = {

                'natije': natije,
                'moshtari': moshtari,

            }
            template = loader.get_template('panel/smslist.html')
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponseRedirect('/access/')
    else:
        return HttpResponseRedirect('/access/')


@login_required(login_url='/login/')
def Moshtariancopen(request):
    portable = models.Portable.objects.get(user=request.user)
    if portable.dhavadaran == 1:
        setting = models.Setting.objects.last()
        if setting.moshtari:
            moshtari = models.Moshtari.objects.all().order_by('-id')
            setting = models.Setting.objects.last()
            natije = 0
            if request.POST:
                text = request.POST.get('text')
                copen = request.POST.get('copen')
                phone = []
                for x in moshtari:
                    phone.append(x.phone)
                try:
                    api = KavenegarAPI(setting.api)
                    params = {
                        # 'sender': '10004346',
                        'receptor': phone,
                        'message': text,
                    }
                    response = api.sms_send(params)
                    print(str(response))
                    for x in moshtari:
                        c = models.Copen.objects.create(copeni=copen, moshtari=x)

                except APIException as e:
                    print(str(e))
                except HTTPException as e:
                    print(str(e))

                natije = 'This Message sent'
            copens = models.Copen.objects.all().order_by('-id')
            context = {
                'natije': natije,
                'moshtari': moshtari,
                'copens': copens,
            }
            template = loader.get_template('panel/copen.html')
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponseRedirect('/access/')
    else:
        return HttpResponseRedirect('/access/')


class pmoshtaricopenDelete(LoginRequiredMixin, generic.DeleteView):
    model = models.Copen
    success_url = reverse_lazy('Moshtariancopen')


class pmoshtaricopenCreate(LoginRequiredMixin, generic.CreateView):
    model = models.Copen
    fields = ['moshtari', 'copeni']
    success_url = reverse_lazy('Moshtariancopen')


class pMoshtariUpdate(LoginRequiredMixin, generic.UpdateView):
    model = models.Moshtari
    fields = ['full_name', 'email', 'phone', 'birthdate']
    success_url = reverse_lazy('Moshtarian')


class pMoshtariDelete(LoginRequiredMixin, generic.DeleteView):
    model = models.Moshtari
    success_url = reverse_lazy('Moshtarian')


class pMoshtariCreate(LoginRequiredMixin, generic.CreateView):
    model = models.Moshtari
    fields = ['full_name', 'email', 'phone', 'birthdate']
    success_url = reverse_lazy('Moshtarian')


@login_required(login_url='/login/')
def pvideo(request):
    portable = models.Portable.objects.get(user=request.user)
    if portable.dvideo == 1:
        setting = models.Setting.objects.last()
        if setting.video:
            video = models.Video.objects.all().order_by('-id')

            context = {
                'video': video,
            }
            template = loader.get_template('panel/video.html')
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponseRedirect('/access/')
    else:
        return HttpResponseRedirect('/access/')


class pvideoUpdate(LoginRequiredMixin, generic.UpdateView):
    model = models.Video
    fields = ['mozo', 'tozihat', 'video']
    success_url = reverse_lazy('video')


class pvideoDelete(LoginRequiredMixin, generic.DeleteView):
    model = models.Video
    success_url = reverse_lazy('video')


class pvideoCreate(LoginRequiredMixin, generic.CreateView):
    model = models.Video
    fields = ['mozo', 'tozihat', 'video']
    success_url = reverse_lazy('video')


@login_required(login_url='/login/')
def paycopen(request):
    portable = models.Portable.objects.get(user=request.user)
    if portable.dhavadaran == 1:
        setting = models.Setting.objects.last()
        if setting.moshtari:
            moshtari = models.Moshtari.objects.all().order_by('-id')
            copens = models.Copen.objects.all().order_by('-id')
            natije = 0
            if request.POST:
                phoneid = request.POST.get('phone')
                copens = models.Copen.objects.filter(moshtari__phone=phoneid)
                natije = 'Sent successfully'
            context = {
                'natije': natije,
                'moshtari': moshtari,
                'copens': copens,

            }
            template = loader.get_template('panel/paycopen.html')
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponseRedirect('/access/')
    else:
        return HttpResponseRedirect('/access/')


@login_required(login_url='/login/')
def safahat(request):
    portable = models.Portable.objects.get(user=request.user)
    if portable.dsafahat == 1:
        setting = models.Setting.objects.last()
        if setting.safahat:
            safe = models.Safahat.objects.all().order_by('-id')
            context = {
                'safe': safe,
            }
            template = loader.get_template('panel/safahatt.html')
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponseRedirect('/access/')
    else:
        return HttpResponseRedirect('/access/')


class psafahatUpdate(LoginRequiredMixin, generic.UpdateView):
    model = models.Safahat
    fields = ['title', 'slug', 'author', 'content', 'image', 'form', 'html', ]
    success_url = reverse_lazy('safahat')


class psafahatDelete(LoginRequiredMixin, generic.DeleteView):
    model = models.Safahat
    success_url = reverse_lazy('safahat')


class psafahatCreate(LoginRequiredMixin, generic.CreateView):
    model = models.Safahat
    fields = ['title', 'slug', 'author', 'content', 'created_date', 'image', 'form', 'html']
    success_url = reverse_lazy('safahat')


class task_manegarUpdate(LoginRequiredMixin, generic.UpdateView):
    model = models.Task_manegar
    fields = ['title', 'sharh', 'created_date', 'end_time', 'status']
    success_url = reverse_lazy('task_manegar')


class task_manegarDelete(LoginRequiredMixin, generic.DeleteView):
    model = models.Task_manegar
    success_url = reverse_lazy('task_manegar')


class TimeUpdate(LoginRequiredMixin, generic.UpdateView):
    model = models.Time
    fields = ['portable', 'status', 'in_time', 'in_date', 'out_time', 'out_date']
    success_url = reverse_lazy('task_manegar')


class TimeDelete(LoginRequiredMixin, generic.DeleteView):
    model = models.Time
    success_url = reverse_lazy('task_manegar')


class TimeCreate(LoginRequiredMixin, generic.CreateView):
    model = models.Time
    fields = ['portable', 'status', 'in_time', 'in_date', 'out_time', 'out_date']
    success_url = reverse_lazy('task_manegar')


@login_required(login_url='/login/')
@csrf_exempt
def task_manegarCreate(request):
    if request.method == 'POST':
        form = request.POST
        full_name = form.get('full_name')
        port = models.Portable.objects.create(full_name=full_name)
        port.save()
        title = form.get('title')
        sharh = form.get('sharh')
        created_date = form.get('created_date')
        end_time = form.get('end_time')
        status = form.get('status')
        task = models.Task_manegar.objects.create(port=port, title=title, sharh=sharh, created_date=created_date,
                                                  end_time=end_time, status=status, )
        task.save()
        return HttpResponseRedirect('/panel/task_manegar/')
    else:
        context = {

        }
        template = loader.get_template('panel/ctask_manegar.html')
        return HttpResponse(template.render(context, request))


@csrf_exempt
@login_required(login_url='/login/')
def ptask_manegar(request):
    portable = models.Portable.objects.get(user=request.user)
    if portable.dtaskmanager == 1:
        setting = models.Setting.objects.last()
        if setting.task_manegar:
            portable = models.Portable.objects.get(user=request.user)
            task_manegar = models.Task_manegar.objects.all().order_by('status')
            context = {
                'task_manegar': task_manegar,
            }
            template = loader.get_template('panel/task_manegar.html')
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponseRedirect('/access/')
    else:
        return HttpResponseRedirect('/access/')


@csrf_exempt
@login_required(login_url='/login/')
def time_cards(request):
    setting = models.Setting.objects.last()
    portable = models.Portable.objects.get(user=request.user)
    flag = 0
    times = models.Time.objects.filter(portable=portable)
    induty = 0
    if times.count() == 0:
        flag = 1
    else:
        t = models.Time.objects.filter(portable=portable).last()
        if t.status == 1:
            flag = 1
        else:
            induty = t
            flag = 0
    time_cards = models.Time.objects.all()

    ttt = models.Time.objects.filter(portable=portable, in_date__year=today.year)
    y = 0
    dp = []
    tt = models.Time.objects.filter(portable=portable, in_date__year=today.year, in_date__month=today.month)
    for m in range(1, 13):
        y = 0
        sum = 0
        for x in ttt:
            if x.status == 1:
                if x.in_date.month == m:
                    if y == 0:
                        sum = x.time()

                    else:
                        sum += x.time()
                    y += 1
        hours = sum // 3600
        dp.append(hours)
    context = {
        'dp': dp,
        'induty': induty,
        'tt': tt,
        'flag': flag,
        'time_cards': time_cards,
    }
    template = loader.get_template('panel/time_cards.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='/login/')
@csrf_exempt
def createtask(request):
    portable = models.Portable.objects.get(user=request.user)
    if request.POST:
        form = request.POST
        if form.get('flag') == '0':

            time = models.Time.objects.filter(portable=portable).last()
            time.out_date = date.today()
            time.out_time = datetime.datetime.now().strftime("%H:%M:%S")
            time.status = 1
            time.save()
        elif form.get('flag') == '1':
            now = datetime.datetime.now().strftime("%H:%M:%S")
            time = models.Time.objects.create(portable=portable, status=0, in_time=now, in_date=today)

    return HttpResponse("1")


@login_required(login_url='/login/')
def pcomment(request):
    portable = models.Portable.objects.get(user=request.user)
    if portable.dcomment == 1:
        comment = models.Comment.objects.all().order_by('-date')

        context = {
            'comment': comment,
        }
        template = loader.get_template('panel/comment.html')
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('/access/')


@login_required(login_url='/login/')
def req(request, id):
    req = models.Comment.objects.get(id=id)
    post = req.post.id
    req.status = 1
    req.save()
    return HttpResponseRedirect('/panel/comment/')


class commentDelete(LoginRequiredMixin, generic.DeleteView):
    model = models.Comment
    success_url = reverse_lazy('comment')


@login_required(login_url='/login/')
def req1(request, id):
    req = models.Task_manegar.objects.get(id=id)
    portable = req.portable.id
    req.status = 3
    req.save()
    return HttpResponseRedirect('/panel/task_manegar/')


@login_required(login_url='/login/')
def menu(request):
    portable = models.Portable.objects.get(user=request.user)
    if portable.dmenu == 1:
        m = models.Menu.objects.all()
        natije = 0
        if request.POST:
            title = request.POST.get('title')
            status = request.POST.get('status')
            s = models.Menu.objects.create(title=title, status=status)
            natije = 'Added successfully'
        context = {
            'm': m,
            'natije': natije,
        }
        template = loader.get_template('panel/menu.html')
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('/access/')


class MenuUpdate(LoginRequiredMixin, generic.UpdateView):
    model = models.Menu
    fields = ['title', 'status']
    success_url = reverse_lazy('menu')


class MenuDelete(LoginRequiredMixin, generic.DeleteView):
    model = models.Menu
    success_url = reverse_lazy('menu')


@login_required(login_url='/login/')
def menus(request, id):
    m = models.Menu.objects.get(id=id)
    natije = 0
    mom = models.SubMenu.objects.filter(menu=m, sub__isnull=True)
    categories = models.Category.objects.filter(pcategory__isnull=True).order_by('-id')
    pages = models.Safahat.objects.all()
    if request.POST:
        # title = request.POST.get('title')
        # status = request.POST.get('status')
        # s = models.Menu.objects.create(title=title,status=status)
        natije = 'Added successfully'
    context = {
        'mom': mom,
        'pages': pages,
        'm': m,
        'categories': categories,
        'natije': natije,
    }
    template = loader.get_template('panel/menus.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='/login/')
@csrf_exempt
def sendcat(request, id):
    menu = models.Menu.objects.get(id=id)
    portable = models.Portable.objects.get(user=request.user)
    if request.POST:
        form = request.POST
        id = form.get('id')

        cat = models.Category.objects.get(id=id)

        try:
            menuu = form.get('menu')
            sub = models.SubMenu.objects.get(id=menuu)
            m = models.SubCat.objects.create(title=cat.title, url=cat, menu=menu, pos=1, status=0, sub=sub)
        except Exception as e:
            m = models.SubCat.objects.create(title=cat.title, url=cat, menu=menu, pos=1, status=0)

    return HttpResponse("1")


@login_required(login_url='/login/')
@csrf_exempt
def sendpage(request, id):
    menu = models.Menu.objects.get(id=id)
    portable = models.Portable.objects.get(user=request.user)
    if request.POST:
        form = request.POST
        id = form.get('id')

        cat = models.Safahat.objects.get(id=id)

        try:
            menuu = form.get('menu')
            sub = models.SubMenu.objects.get(id=menuu)
            m = models.SubPage.objects.create(title=cat.title, url=cat, menu=menu, pos=1, status=2, sub=sub)
        except Exception as e:
            m = models.SubPage.objects.create(title=cat.title, url=cat, menu=menu, pos=1, status=2)

    return HttpResponse("1")


@login_required(login_url='/login/')
@csrf_exempt
def sendlink(request, id):
    menu = models.Menu.objects.get(id=id)
    portable = models.Portable.objects.get(user=request.user)
    if request.POST:
        form = request.POST
        title = form.get('title')
        url = form.get('url')

        try:
            menuu = form.get('menu')
            sub = models.SubMenu.objects.get(id=menuu)
            m = models.SubUrl.objects.create(title=title, url=url, menu=menu, pos=1, status=1, sub=sub)
        except Exception as e:
            m = models.SubUrl.objects.create(title=title, url=url, menu=menu, pos=1, status=1, )

    return HttpResponse("1")


@login_required(login_url='/login/')
@csrf_exempt
def dlmenu(request, id):
    menu = models.SubMenu.objects.get(id=id)
    m = menu.menu.id
    menu.delete()
    return HttpResponseRedirect("/panel/menus/" + str(m) + '/')


@login_required(login_url='/login/')
@csrf_exempt
def newfile(request):
    the = models.Setting.objects.last()
    theme = the.theme.name
    if request.POST:
        mypath = request.GET.get('folder')
        static = request.GET.get('folder')
        s = request.POST.get('name')
        codes = "{% extends '" + str(
            theme) + "/base.html' %} {% load thumbnail %} {% load farapy %} {% load static %}\n" \
                     "{% block title %}{{p.title}}{% endblock title %}\n" \
                     "{% block content %}\n" \
                     "\n" \
                     "{% endblock %}\n"

        filename, file_extension = os.path.splitext(str(s))
        url = str(static) + s
        if file_extension == '.html':
            ff = open(str(mypath) + str(s), 'w', encoding='utf-8')
            ff.write(str(codes))
            ff.close()
            return HttpResponseRedirect("/panel/themeeditor/?file=" + str(url) + '&folder=' + str(static))
        else:
            ff = open(str(static) + str(s), 'w', encoding='utf-8')
            ff.close()
            return HttpResponseRedirect("/panel/themeeditor/?file=" + str(url) + '&folder=' + str(static))


@login_required(login_url='/login/')
@csrf_exempt
def newfolder(request):
    the = models.Setting.objects.last()
    theme = the.theme.name
    if request.POST:
        folder = request.GET.get('folder')

        s = request.POST.get('name')
        os.mkdir(str(folder) + '/' + str(s))

        return HttpResponseRedirect("/panel/themeeditor/?folder=" + str(folder))


@login_required(login_url='/login/')
@csrf_exempt
def delfile(request):
    the = models.Setting.objects.last()
    theme = the.theme.name
    if request.GET:
        folder = request.GET.get('folder')

        s = request.GET.get('file')
        mypath = str('themes/' + str(theme) + '/')
        os.remove(str(s))
        return HttpResponseRedirect('/panel/themeeditor/' + '?folder=' + str(folder))


@login_required(login_url='/login/')
@csrf_exempt
def delfolder(request):
    the = models.Setting.objects.last()
    theme = the.theme.name
    if request.GET:
        folder = request.GET.get('folder')

        s = request.GET.get('file')
        mypath = str('themes/' + str(theme) + '/')
        shutil.rmtree(s)
        return HttpResponseRedirect("/panel/themeeditor/" + '?folder=' + str(folder))


@login_required(login_url='/login/')
@csrf_exempt
def upfile(request):
    the = models.Setting.objects.last()
    theme = the.theme.name
    if request.POST:
        s = request.FILES.get('file')
        folder = request.GET.get('folder')

        media = folder
        static = media
        filename, file_extension = os.path.splitext(str(s.name))
        fs = FileSystemStorage(location=static)  # defaults to   MEDIA_ROOT
        filename = fs.save(s.name, s)
        file_url = fs.url(filename)
        urll = str(s.name)
        return HttpResponseRedirect("/panel/themeeditor/?gg=1&g=" + str(urll) + "&folder=" + str(folder))


@login_required(login_url='/login/')
@csrf_exempt
def commpresstheme(request):
    the = models.Setting.objects.last()
    theme = the.theme.name
    if request.GET:
        folder = request.GET.get('folder')
        static = str('themes/' + str(theme) + '/')
        shutil.make_archive(static + theme + '_' + str(today), 'zip', static)
        return HttpResponseRedirect("/panel/themeeditor/" + '?folder=' + str(folder))


@login_required(login_url='/login/')
@csrf_exempt
def themeeditor(request):
    the = models.Setting.objects.last()
    theme = the.theme.name
    portable = models.Portable.objects.get(user=request.user)
    if portable.dthemeeditor == 1:
        natije = 0
        static = str('themes/' + str(theme) + '/')
        listOfFiles = [x[0] for x in os.walk(static)]  # for ui js

        folder = static
        if request.GET.get('folder'):
            folder = request.GET.get('folder')
        if len(folder) < 6:
            folder = static
        staticfiles = [os.path.join(folder, f) for f in listdir(folder) if isfile(join(folder, f))]
        folders = [os.path.join(folder, f) for f in listdir(folder) if isdir(join(folder, f))]
        for s in staticfiles:
            if isfile(s):
                ss = s.split('.')
                if ss[1] == 'html':
                    selected = s

                    file = open(s, 'r', encoding='utf-8')
                    break

        gg = request.GET.get('gg')  # 1 status
        if gg == '1':
            g = request.GET.get('g')  # 1 status

            natije = 'File Address  : ' + str(g)
        if request.GET.get('file'):
            s = request.GET.get('file')
            selected = s
            if request.POST:
                codes = request.POST.get('content')
                ff = open(str(s), 'w', encoding='utf-8')
                ff.write(str(codes))
                ff.close()
            try:
                file = open(str(s), 'r', encoding='utf-8')
            except:
                file = open(static + 'index.html', 'r', encoding='utf-8')
        else:
            selected = static + 'index.html'
            file = open(static + 'index.html', 'r', encoding='utf-8')
            s = selected

        try:
            tab = models.Tabs.objects.get(portable=portable)
        except:
            tab = models.Tabs.objects.create(portable=portable)

        t = file.read()
        file_extension = selected.split('.')
        context = {
            'tab': tab,
            'listOfFiles': listOfFiles,
            'pasvand': file_extension[-1],
            'folder': folder,
            'natije': natije,
            'folders': folders,
            'staticfiles': staticfiles,
            's': s,
            't': t,
        }
        template = loader.get_template('panel/theme.html')
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('/access/')


@login_required(login_url='/login/')
@csrf_exempt
def tabupdate(request):
    the = models.Setting.objects.last()
    theme = the.theme.name
    portable = models.Portable.objects.get(user=request.user)

    if request.POST:
        a = request.POST.get('autosave')
        f = request.POST.get('fontsize')
        try:
            tab = models.Tabs.objects.get(portable=portable)
        except:
            tab = models.Tabs.objects.create(portable=portable)

        tab.fontsize = f
        tab.autosave = a
        tab.save()
        return HttpResponse(1)


@login_required(login_url='/login/')
@csrf_exempt
def themes(request):
    the = models.Setting.objects.last()
    theme = the.theme.name
    portable = models.Portable.objects.get(user=request.user)
    if portable.dthemeeditor == 1:
        if request.FILES:
            s = request.FILES.get('file')
            media = str('themes/')
            static = media
            filename, file_extension = os.path.splitext(str(s.name))
            fs = FileSystemStorage(location=static)  # defaults to   MEDIA_ROOT
            filename = fs.save(s.name, s)
            file_url = fs.url(filename)
            path = static + filename
            with zipfile.ZipFile(path, 'r') as zip_ref:
                zip_ref.extractall(static)
        natije = 0
        static = str('themes/')
        list = [f for f in listdir(static) if not isfile(join(static, f))]
        themes = []
        for x in list:
            s = models.Theme.objects.get_or_create(name=x)
            s = models.Theme.objects.get(name=x)
            tt = {}
            tt['name'] = x
            tt['selected'] = 'N'
            if x == theme:
                tt['selected'] = 'Y'
            tt['index'] = 0
            tt['category'] = 0
            tt['base'] = 0
            tt['post'] = 0
            tt['page'] = 0
            tt['search'] = 0
            tt['vrify'] = 0
            tt['theme_pic'] = '/media/theme-default-thumb.png'
            dir = str('themes/' + x + '/')
            files = [f for f in listdir(dir) if isfile(join(dir, f))]
            for u in files:
                if u == 'index.html':
                    tt['index'] = 1
                elif u == 'category.html':
                    tt['category'] = 1
                elif u == 'base.html':
                    tt['base'] = 1
                elif u == 'post.html':
                    tt['post'] = 1
                elif u == 'page.html':
                    tt['page'] = 1
                elif u == 'search.html':
                    tt['search'] = 1
                im = u.split('.')
                if im[0] == 'theme_pic':
                    tt['theme_pic'] = '/' + u

            count_of_files = 0
            for value in tt:
                if tt[value] == 1:
                    count_of_files += 1
            if count_of_files == 6:
                tt['vrify'] = 1
            themes.append(tt)
        for x in models.Theme.objects.all():
            flag = 0
            for y in list:
                if x.name == y:
                    flag = 1
            if flag == 0:
                x.delete()
        if request.FILES:
            s = request.FILES.get('file')
            media = str('themes/')
            static = media
            filename, file_extension = os.path.splitext(str(s.name))
            fs = FileSystemStorage(location=static)  # defaults to   MEDIA_ROOT
            filename = fs.save(s.name, s)
            file_url = fs.url(filename)
            path = static + filename
            with zipfile.ZipFile(path, 'r') as zip_ref:
                zip_ref.extractall(static)

        context = {
            'list': themes,
        }
        template = loader.get_template('panel/themes.html')
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('/access/')


@login_required(login_url='/login/')
@csrf_exempt
def selecttheme(request):
    the = models.Setting.objects.last()
    theme = the.theme.name
    if request.GET:
        s = request.GET.get('theme')
        th = models.Theme.objects.get(name=s)
        t = models.Setting.objects.last()
        t.theme = th
        t.save()
	
        file = open('FaraPy/urls.py', 'a', encoding='utf-8')
        file.write('#')
        # urls.staticc = str('themes/' + str(theme))
        f = os.path.abspath(os.getcwd())
        f = str(f)
        f = f.split('/')
        os.system('cloudlinux-selector --json restart --interpreter=python --user=faral  --app-root='+str(f[-1]))

        return HttpResponseRedirect("/panel/themes/")


@login_required(login_url='/login/')
@csrf_exempt
def deltheme(request):
    the = models.Setting.objects.last()
    theme = the.theme.name
    if request.GET:
        s = request.GET.get('theme')
        th = models.Theme.objects.get(name=s)
        t = models.Setting.objects.last()
        dir = 'themes/' + s + '/'
        if t.theme != th:
            shutil.rmtree('themes/' + s + '/')

        return HttpResponseRedirect("/panel/themes/")


@login_required(login_url='/login/')
def tickets(request):
    portable = models.Portable.objects.get(user=request.user)

    tickets = models.Tickets.objects.all().order_by('-date')

    context = {
        'tickets': tickets,
    }
    template = loader.get_template('panel/tickets.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='/login/')
def ticket(request, id):
    portable = models.Portable.objects.get(user=request.user)

    tickets = models.Tickets.objects.get(id=id)

    context = {
        'tickets': tickets,
    }
    template = loader.get_template('panel/ticket.html')
    return HttpResponse(template.render(context, request))



@csrf_exempt
@login_required(login_url='/login/')
def addticket(request):
    portable = models.Portable.objects.get(user=request.user)
    title = request.POST.get('title')
    text = request.POST.get('text')
    tickets = models.Tickets.objects.create(user=portable, title=title, description=text)
    send = {
        'title': title,
        'text': text,
        'idticket':tickets.id,
        'user':portable.user,
        'edays':edays,
        'today':today,
        'key':tickets.id,
    }
    data = urllib.parse.urlencode(send).encode()
    req = urllib.request.Request(SupportUrl+'/manage_tickets/', data = data)
    resp = urllib.request.urlopen(req)
    dom = resp.read()
    tickets.key =  json.loads(dom)['key']
    tickets.save()
    return HttpResponse(1)


@csrf_exempt
@login_required(login_url='/login/')
def addsubticket(request,id):
    portable = models.Portable.objects.get(user=request.user)
    title = request.POST.get('title')
    text = request.POST.get('text')
    tickets = models.Tickets.objects.get(id=id)
    tickets.status = 1
    tickets.save()
    subticket = models.SubTickets.objects.create(description=text,ticket=tickets,user=portable,)
    send = {
        'text': text,
        'key':tickets.key,
        'user':portable.user,
        'edays':edays,
        'today':today,
    }
    data = urllib.parse.urlencode(send).encode()
    req = urllib.request.Request(SupportUrl+'/manage_subtickets/', data = data)
    resp = urllib.request.urlopen(req)
    dom = resp.read()

    return HttpResponseRedirect('/panel/ticket/'+str(tickets.id)+'/')


@csrf_exempt
def manage_subtickets(request):
    form = request.POST
    text = form.get('text')
    ticket = form.get('key')
    t = models.Tickets.objects.get(key=ticket)
    tickets = models.SubTickets.objects.create(ticket=t, description=text)
    return HttpResponse(1)

@csrf_exempt
def manage_tickets(request):
    form = request.POST
    title = form.get('title')
    key = form.get('key')
    url = request.META['REMOTE_ADDR']
    text = form.get('text')
    idticket = form.get('idticket')
    user = form.get('user')
    edays = form.get('edays')
    today = form.get('today')
    tickets = models.Tickets.objects.create(title=title, description=text,key = str(url)+'*'+str(key))

    return JsonResponse({'key':key,})


@csrf_exempt
def closeticket(request,id):

    tickets = models.Tickets.objects.get(id=id)
    tickets.status = 0
    tickets.save()

    return HttpResponseRedirect('/panel/tickets/')

class TicketDelete(LoginRequiredMixin, generic.DeleteView):

    model = models.Tickets
    success_url = reverse_lazy('tickets')










############### JUST IN FARAL WEBSITE /virtualenv/cms.zip




