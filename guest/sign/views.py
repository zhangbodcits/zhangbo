from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404


# Create your views here.
def index(request):
    return render(request, 'index.html')


# 登陆模块
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            response = HttpResponsePermanentRedirect('/event_manage/')
            # response.set_cookie('user',username,3600)#添加浏览器cookie
            request.session['user'] = username
            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})


# 发布会列表
@login_required
def event_manage(request):
    if request.method == "POST":
        Event.objects.create(name=request.POST.get('name'), limit=request.POST.get('limit'),
                             status=request.POST.get('status'), address=request.POST.get('address'),
                             start_time=request.POST.get('start_time'))
        name = request.POST.get('name')
        limit = request.POST.get('limit')
        status = request.POST.get('status')
        address = request.POST.get('address')
        start_time = request.POST.get('start_time')
        if not name or not limit or not status or not address or not start_time:
            error = {"error": "输入框不能为空"}
            return render(request, 'new_event.html', error)
            # if not name:
            #     error = {"error": "name不能为空"}
            #     return render(request, 'new_event.html', error)

    # username = request.COOKIES.get('user','')#读取浏览器cooke

    event_list = Event.objects.all()
    username = request.session.get('user', '')  # 读取浏览器session
    print(event_list)
    return render(request, 'event_manage.html', {'user': username, 'events': event_list})  # 新建发布会


# 新建发布会
def new_event(request):
    return render(request, 'new_event.html')


# 新增嘉宾
def new_guest(request):
    return render(request, 'new_guest.html')


# 发布会名称搜索
@login_required()
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get('name', )
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, 'event_manage.html', {'user': username, 'events': event_list})


# 删除发布会
@login_required()
def delete_event(request):
    eid = request.GET.get("eid", 0)
    try:
        Event.objects.get(id=eid).delete()
    except Event.DoesNotExist:
        return render(request, 'event_manage.html', {'error': '删除发布会不存在'})
    return redirect("/event_manage/")


# 嘉宾列表
@login_required()
def guest_manage(request):
    if request.method == "POST":
        event = request.POST.get('eid')
        realname = request.POST.get('realname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        sign = request.POST.get('sign')
        print(event, realname, phone, email, sign)
        if not event or not realname or not phone or not email or not sign:
            error = {"error": "输入框不能为空"}
            return render(request, 'new_guest.html', error)
        Guest.objects.create(event_id=event, realname=realname, phone=phone, email=email, sign=sign)
    guest_list = Guest.objects.all()
    print(guest_list)
    username = request.session.get('user', '')
    paginator = Paginator(guest_list, 10)
    print(Paginator,11111111111111111111111111111)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
        print(contacts)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'guest_manage.html', {'user': username, 'guests': contacts})


# 删除嘉宾
@login_required()
def delete_guest(request):
    eid = request.GET.get("eid", 0)
    try:
        Guest.objects.get(id=eid).delete()
    except Event.DoesNotExist:
        return render(request, 'guest_manage.html', {'error': '删除嘉宾不存在'})
    return redirect("/guest_manage/")


# 编辑嘉宾
def edit_guest(request):
    if request.method == "GET":
        eid = request.GET.get("eid", 0)
        print(eid)
        try:
            guest_list = Guest.objects.get(id=eid)
        except Event.DoesNotExist:
            return render(request, 'edit_guest.html')
        return render(request, 'edit_guest.html', {"guest": guest_list, "eid": eid})
    elif request.method == "POST":
        event = request.POST.get('event')
        eid = request.POST.get('eid')
        realname = request.POST.get('realname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        sign = request.POST.get('sign')
        Guest.objects.filter(id=eid).update(event_id=event, realname=realname, phone=phone, email=email, sign=sign)
    guest_list = Guest.objects.all()
    username = request.session.get('user', '')
    return render(request, 'guest_manage.html', {'user': username, 'guests': guest_list})


# 编辑发布会
def edit_event(request):
    if request.method == "GET":
        event_id = request.GET.get("eid", 0)
        try:
            event_list = Event.objects.get(id=event_id)
            event_dict = model_to_dict(event_list)
            event_dict["start_time"] = event_dict["start_time"].strftime(r'%Y-%m-%d %H:%M:%S')
        except Event.DoesNotExist:
            return render(request, 'edit_event.html')
        return render(request, 'edit_event.html', {"event": event_dict, "eid": event_id})
    elif request.method == "POST":
        event_id = request.POST.get('event_id')
        # event_id = request.POST.get('id')
        name = request.POST.get('name')
        limit = request.POST.get('limit')
        address = request.POST.get('address')
        status = request.POST.get('status')

        start_time = request.POST.get('start_time')
        Event.objects.filter(id=event_id).update(name=name, limit=limit, address=address, status=status,
                                                 start_time=start_time)
    event_list = Event.objects.all()
    username = request.session.get('user', '')
    return render(request, 'event_manage.html', {'user': username, 'events': event_list})


# 签到页面
@login_required
def sign_index(request, eid):
    event = get_object_or_404(Event, id=eid)
    return render(request, 'sign_index.html', {'event': event})


# 签到动作
@login_required
def sign_index_action(request, eid):
    event = get_object_or_404(Event, id=eid)
    phone = request.POST.get('phone', '')
    print(phone)
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': '手机号码错误!'})
    result = Guest.objects.filter(phone=phone, event_id=eid)

    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': '手机号码或用户不存在!'})
    result = Guest.objects.filter(phone=phone, event_id=eid)
    print(type(result), result)
    result = Guest.objects.get(phone=phone, event_id=eid)
    print(type(result), result)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event, 'hint': '用户已经签到!'})
    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign='1')
        return render(request, 'sign_index.html', {'event': event, 'hint': '签到成功!', 'guest': result})

    # 退出
@login_required
def loginout(request):
    auth.logout(request)  # 退出系统
    response = HttpResponsePermanentRedirect('/index/')
    return response
