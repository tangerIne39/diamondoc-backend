import datetime

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


def group_to_content(group):
    return {
        'groupid': group.id,
        'groupname': group.group_name,
        'description': group.description,
        'createdtime': group.created_time
    }


def document_to_content(document):
    content = {
        'id': document.id,
        'title': document.title,
        'creator_id': document.creator_id,
        'created_time': document.created_time,
        'modify_right': document.modify_right,
        'share_right': document.share_right,
        'discuss_right': document.discuss_right,
        'recycled': document.recycled,
        'is_occupied': document.is_occupied,  # 0: Not occupied, 1: Occupied
        'group_id': document.group_id,
        'modified_time': document.modified_time
    }
    return content


def toTF(num):
    if num == 1:
        return True
    return False


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


@csrf_exempt
def creategroup(request):
    user = User.objects.get(username=request.POST.get('username'))
    new_group = Group(group_name=request.POST.get('groupname'), leader=user, created_time=datetime.datetime.now(),
                      description=request.POST.get('description'))
    new_group_memer = GroupMember(group=new_group, user=user)
    new_group.save()
    new_group_memer.save()
    return sendmsg('success')


@csrf_exempt
def modify_group_info(request):
    group = Group.objects.get(id=request.POST.get('groupid'))
    group.group_name = request.POST.get('groupname')
    group.description = request.POST.get('description')
    group.save()
    return sendmsg('success')


@csrf_exempt
def mygroup(request):
    user = User.objects.get(username=request.POST.get('username'))
    group_members = GroupMember.objects.filter(user=user)
    res = []
    for group_member in group_members:
        group = Group.objects.get(id=group_member.group.id)
        if group.leader.id != user.id:
            res.append(group_to_content(group))
    return JsonResponse(res)


@csrf_exempt
def groupiscreatedbyme(request):
    user = User.objects.get(username=request.POST.get('username'))
    if Group.objects.filter(leader=user, group=Group.objects.get(id=request.POST.get('groupid'))).exists():
        return sendmsg('yes')
    else:
        return sendmsg('no')


@csrf_exempt
def search_group(request):
    user = User.objects.get(username=request.POST.get('username'))
    keyword = request.POST.get('keyword')
    res = []
    groups = Group.objects.filter(group_name__contains=keyword)
    for group in groups:
        gm = GroupMember.objects.filter(group=group, user=user).first()
        if gm is not None:
            continue
        res.append(group_to_content(group))
    return JsonResponse(res)


@csrf_exempt
def group_created_byme(request):
    user = User.objects.get(username=request.POST.get('username'))
    groups = Group.objects.filter(leader=user)
    res = []
    for group in groups:
        res.append(group_to_content(group))
    return JsonResponse(res)


@csrf_exempt
def addgroupmember(request):
    user = User.objects.get(id=request.POST.get('userid'))
    group = Group.objects.get(id=request.POST.get('groupid'))
    new_group_member = GroupMember(group=group, user=user)
    new_group_member.save()

    content = user.username + "通过了你的邀请，加入团队(" + group.group_name + ")"
    new_notice = Notice(content=content, sender=user, receiver=group.leader, group=group,
                        send_time=datetime.datetime.now(), type=1)
    new_notice.save()

    documents = Document.objects.filter(group=group)
    for document in documents:
        new_document_user = DocumentUser(document=document, user=user, type=1, favorite=0)
        new_document_user.save()
    Notice.objects.get(id=request.POST.get('id')).delete()
    return sendmsg('success')


@csrf_exempt
def refuse_groupmember(request):
    user = User.objects.get(id=request.POST.get('userid'))
    group = Group.objects.get(id=request.POST.get('groupid'))
    new_notice = Notice(content=user.username + "拒绝了你的邀请，不加入团队(" + group.group_name + ")", sender=user,
                        receiver=group.leader, group=group, send_time=datetime.datetime.now(), type=5)
    new_notice.save()
    Notice.objects.get(id=request.POST.get('id')).delete()
    return sendmsg('success')


@csrf_exempt
def queryuser(request):
    keyword = request.POST.get('keyword')
    users = User.objects.filter(username__contains=keyword)
    group_members = GroupMember.objects.filter(group=Group.objects.get(id=request.POST.get('groupid')))
    group_users = []
    for group_member in group_members:
        group_users.append(group_member.user)
    res = []
    for user in users:
        check = 1
        for groupuser in group_users:
            if user.id == groupuser.id:
                check = 0
                continue
        if check == 1:
            res.append(user_to_content(user))
    return JsonResponse(res)


@csrf_exempt
def invite_user(request):
    group = Group.objects.get(id=request.POST.get('groupid'))
    user = User.objects.get(id=request.POST.get('userid'))
    sender = User.objects.get(username=request.POST.get('leader_username'))
    notice = Notice.objects.get(group=group, sender=sender, receiver=user, type=2)
    if notice is not None:
        return sendmsg('success')
    new_notice = Notice(content=sender.username + "邀请你加入团队(" + group.group_name + ")", sender=sender, receiver=user,
                        group=group, send_time=datetime.datetime.now(), type=2)
    new_notice.save()
    return sendmsg('success')


@csrf_exempt
def apply_in_group(request):
    user = User.objects.get(username=request.POST.get('username'))
    group = Group.objects.get(group_name=request.POST.get('groupname'))
    notice = Notice.objects.get(group=group, sender=user, type=6, receiver=group.leader)
    if notice is not None:
        return sendmsg('success')
    new_notice = Notice(content=user.username + "申请加入团队(" + group.group_name + ")", sender=user, receiver=group.leader,
                        group=group, send_time=datetime.datetime.now(), type=6)
    new_notice.save()
    return sendmsg('success')


@csrf_exempt
def accept_application_addgroupmember(request):
    user = User.objects.get(id=request.POST.get('userid'))
    group = Group.objects.get(id=request.POST.get('groupid'))
    leader = User.objects.get(id=group.leader.id)
    new_group_member = GroupMember(group=group, user=user)
    new_group_member.save()

    new_notice = Notice(content=leader.username + "通过了你的申请，你已加入团队(" + group.group_name + ")", sender=leader,
                        receiver=user, group=group, send_time=datetime.datetime.now(), type=7)
    new_notice.save()
    Notice.objects.get(id=request.POST.get('id')).delete()
    documents = Document.objects.filter(group=group)
    for document in documents:
        new_document_user = DocumentUser(document=document, user=user, last_watch=0,
                                         favorited=0, type=1, modified_time=0)
        new_document_user.save()
    return sendmsg('success')


@csrf_exempt
def refuse_application_addgroupmember(request):
    user = User.objects.get(id=request.POST.get('userid'))
    group = Group.objects.get(id=request.POST.get('groupid'))
    leader = User.objects.get(id=group.leader.id)

    new_notice = Notice(content=leader.username + "拒绝了你的申请，加入团队(" + group.group_name + "失败)", sender=leader,
                        receiver=user, group=group, send_time=datetime.datetime.now(), type=8)
    new_notice.save()
    Notice.objects.get(id=request.POST.get('id')).delete()
    return sendmsg('success')


@csrf_exempt
def get_user_bygroup(request):
    group_members = GroupMember.objects.filter(group=Group.objects.get(id=request.POST.get('groupid')))
    users = []
    for group_member in group_members:
        users.append(group_member.user)
    res = []
    for user in users:
        res.append(user_to_content(user))
    return JsonResponse(res)


@csrf_exempt
def delete_user(request):
    group = Group.objects.get(id=request.POST.get('groupid'))
    GroupMember.objects.filter(group=group, user=User.objects.get(id=request.POST.get('userid'))).delete()

    sender = User.objects.get(id=request.POST.get('leaderid'))
    receiver = User.objects.get(id=request.POST.get('userid'))
    new_notice = Notice(content=sender.username + "将你从团队(" + group.group_name + ")中移除", sender=sender,
                        receiver=receiver, group=group, send_time=datetime.datetime.now(), type=0)
    new_notice.save()

    documents = Document.objects.filter(group=group)
    for document in documents:
        DocumentUser.objects.filter(document=document, user=receiver).delete()
    return sendmsg('success')


@csrf_exempt
def quit_group(request):
    group = Group.objects.get(id=request.POST.get('groupid'))
    user = User.objects.get(id=request.POST.get('userid'))
    GroupMember.objects.filter(group=group, user=user).delete()

    receiver = User.objects.get(id=group.leader.id)
    new_notice = Notice(content=user.username + "退出了团队(" + group.group_name + ")", sender=user, receiver=receiver,
                        group=group, send_time=datetime.datetime.now(), type=9)
    new_notice.save()

    documents = Document.objects.filter(group=group)
    for document in documents:
        DocumentUser.objects.filter(document=document, user=user).delete()
    return sendmsg('success')


@csrf_exempt
def delete_group(request):
    Group.objects.get(id=request.POST.get('groupid')).delete()
    GroupMember.objects.filter(group=Group.objects.get(id=request.POST.get('groupid'))).delete()

    documents = Document.objects.filter(group=Group.objects.get(id=request.POST.get('groupid')))
    for document in documents:
        DocumentUser.objects.filter(document=document).delete()
    return sendmsg('success')


@csrf_exempt
def create_personal_doc(request):
    user = User.objects.get(username=request.POST.get('username'))
    new_document = Document(title=request.POST.get('title'), group=None, created_time=datetime.datetime.now(),
                            modified_time=0, creator_id=user.id, modify_right=request.POST.get('modify_right'),
                            share_right=request.POST.get('share_right'),
                            discuss_right=request.POST.get('discuss_right'),
                            others_modify_right=request.POST.get('modify_right'),
                            others_share_right=request.POST.get('share_right'),
                            others_discuss_right=request.POST.get('discuss_right'), content=request.POST.get('content'),
                            recycled=0, is_occupied=0)
    new_document.save()

    new_document_user = DocumentUser(document=new_document, user=user, last_watch=0, favorite=0, modified_time=0,
                                     type=0)
    new_document_user.save()
    return sendmsg('success')


@csrf_exempt
def create_group_doc(request):
    user = User.objects.get(username=request.POST.get('username'))
    creator_id = user.id
    new_document = Document(title=request.POST.get('title'), creator_id=creator_id,
                            group=Group.objects.get(id=request.POST.get('groupid')),
                            created_time=datetime.datetime.now(), modify_right=request.POST.get('modify_right'),
                            share_right=request.POST.get('share_right'),
                            discuss_right=request.POST.get('discuss_right'),
                            others_modify_right=request.POST.get('others_modify_right'),
                            others_share_right=request.POST.get('others_share_right'),
                            others_discuss_right=request.POST.get('others_discuss_right'),
                            content=request.POST.get('content'), recycled=0, is_occupied=0, modified_time=0)
    new_document.save()

    members = GroupMember.objects.filter(group=Group.objects.get(id=request.POST.get('groupid')))
    for member in members:
        new_document_user = DocumentUser(document=new_document, user=member.user, last_watch=0, favorite=0,
                                         modified_time=0, type=1)
        new_document_user.save()
    return sendmsg('success')


@csrf_exempt
def my_docs(request):
    user = User.objects.get(username=request.POST.get('username'))
    documents = DocumentUser.objects.filter(user=user)
    doc_list = []
    for document in documents:
        doc = Document.objects.get(id=document.document.id)
        if doc.recycled == 0 and document.type != 1:
            doc_list.append(doc)
    return JsonResponse(doc_list)


@csrf_exempt
def my_created_docs(request):
    user = User.objects.get(username=request.POST.get('username'))
    documents = Document.objects.filter(creator_id=user.id, recycled=0)
    res = []
    for document in documents:
        if document.recycled == 0:
            res.append(document_to_content(document))
    return JsonResponse(res)


@csrf_exempt
def my_deleted_docs(request):
    user = User.objects.get(username=request.POST.get('username'))
    documents = Document.objects.filter(creator_id=user.id, recycled=1)
    res = []
    for document in documents:
        res.append(document_to_content(document))
    return JsonResponse(res)


@csrf_exempt
def tell_doc_right(request):
    document = Document.objects.get(id=request.POST.get('documentID'))
    user = User.objects.get(username=request.POST.get('username'))
    document_user = DocumentUser.objects.get(document=document, user=user)
    if document_user == None:
        response = {
            'watch_right': False,
            'modify_right': False,
            'share_right': False,
            'discuss_right': False,
            'others_modify_right': False,
            'others_share_right': False,
            'others_discuss_right': False,
            'others_watch_right': False,
            'doctype': -1,
            'usertype': -1,
            'isleader': False
        }
    elif user.id == document.creator_id:
        if document.group.id != 0:
            type = 0
        else:
            type = 1
        response = {
            'watch_right': True,
            'modify_right': True,
            'share_right': True,
            'discuss_right': True,
            'others_modify_right': True,
            'others_share_right': True,
            'others_discuss_right': True,
            'others_watch_right': True,
            'doctype': type,
            'usertype': document_user.type,
            'isleader': True
        }
    else:
        if document.group.id != 0:
            type = 0
        else:
            type = 1

        modify_right = toTF(document.modify_right)
        share_right = toTF(document.share_right)
        discuss_right = toTF(document.discuss_right)

        others_modify_right = toTF(document.others_modify_right)
        others_share_right = toTF(document.others_share_right)
        others_discuss_right = toTF(document.others_discuss_right)
        response = {
            'watch_right': True,
            'modify_right': modify_right,
            'share_right': share_right,
            'discuss_right': discuss_right,
            'others_modify_right': others_modify_right,
            'others_share_right': others_share_right,
            'others_discuss_right': others_discuss_right,
            'others_watch_right': True,
            'doctype': type,
            'usertype': document_user.type,
            'isleader': False
        }
    return JsonResponse(response)


@csrf_exempt
def tell_current_doc_right(request):
    document = Document.objects.get(id=request.POST.get('documentID'))
    response = {
        'modify_right': document.modify_right,
        'share_right': document.share_right,
        'discuss_right': document.discuss_right,
        'others_modify_right': document.others_modify_right,
        'others_share_right': document.others_share_right,
        'others_discuss_right': document.others_discuss_right,
    }
    return JsonResponse(response)
# ------------wlc------------


# ------------end------------
