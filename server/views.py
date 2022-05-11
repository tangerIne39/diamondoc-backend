from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
# ------------yxy------------
from .models import *


def sendmsg(message):
    return JsonResponse({'message': message})


def user_to_content(user):
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'password': user.password,
        'description': user.description
    }


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.get(username=username)
        if user.password != password:
            return sendmsg('fail')
        return JsonResponse(user_to_content(user))
    else:
        return sendmsg('fail')


@csrf_exempt
def get_user(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.POST.get('username'))
        return JsonResponse(user_to_content(user))
    else:
        return sendmsg('fail')


@csrf_exempt
def get_user_byid(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.POST.get('userid'))
        return JsonResponse(user_to_content(user))
    else:
        return sendmsg('fail')


@csrf_exempt
def logout(request):
    return sendmsg('success')


@csrf_exempt
def regist(request):
    if request.method == 'POST':
        user = User.objects.filter(username=request.POST.get('username'))
        email = User.objects.filter(email=request.POST.get('email'))
        if user.exists() or email.exists():
            return sendmsg('fail')
        else:
            new_user = User(username=request.POST.get('username'), password=request.POST.get('password'),
                            email=request.POST.get('email'))
            new_user.save()
            return sendmsg('success')
    else:
        return sendmsg('fail')


@csrf_exempt
def getalluser(request):
    users = User.objects.all()
    res = []
    for user in users:
        res.append(user_to_content(user))
    return JsonResponse(res)


@csrf_exempt
def modify_user_info(request):  # 存在没有校验new_password1和new_password2的bug
    user = User.objects.get(username=request.POST.get('username'))
    username = User.objects.filter(username=request.POST.get('new_username')).first()
    email = User.objects.filter(email=request.POST.get('new_email')).first()
    if username is not None:
        if username.id != user.id:
            return sendmsg('fail')
    if email:
        if email.id != user.id:
            return sendmsg('fail')

    user.username = request.POST.get('new_username')
    user.password = request.POST.get('new_password1')
    user.email = request.POST.get('new_email')
    user.description = request.POST.get('new_description')
    user.save()
    return sendmsg('success')

# ------------wlc------------


# ------------end------------
