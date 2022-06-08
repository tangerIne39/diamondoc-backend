import datetime
import time
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


# def document_to_content(document):
#     content = {
#         'id': document.id,
#         'title': document.title,
#         'creator_id': document.creator_id,
#         'created_time': document.created_time,
#         'modify_right': document.modify_right,
#         'share_right': document.share_right,
#         'discuss_right': document.discuss_right,
#         'recycled': document.recycled,
#         'is_occupied': document.is_occupied,  # 0: Not occupied, 1: Occupied
#         'group_id': document.group.id,
#         'modified_time': document.modified_time
#     }
#     return content

def document_to_content(document):
    if document.group is None:
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
            'group_id': 0,
            'modified_time': document.modified_time
        }
    if document.group is not None:
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
            'group_id': document.group.id,
            'modified_time': document.modified_time
        }
    return content


def toTF(num):
    if num == 1:
        return True
    return False


def get_user_indocument(documentID):
    document = Document.objects.get(id=documentID)
    all_DU = DocumentUser.objects.filter(document=document).all()
    all_user = []
    for du in all_DU:
        user = User.objects.filter(id=du.user.id).all()
        all_user += user
    return all_user


# def get_newid():
#     time_now = int(time.time())
#     # 转换成localtime
#     time_local = time.localtime(time_now)
#     # 转换成新的时间格式(2016-05-09 18:59:20)
#     dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
#     id = time.mktime(time.strptime(dt, "%Y-%m-%d %H:%M:%S"))
#     return id


def get_user_byusername(username):
    user = User.objects.get(username=username)
    return user


def get_user_bykeyword(keyword):
    all_user = User.objects.filter(username__contains='{keyword}'.format(keyword=keyword)).all()
    return all_user


def get_user_ingroup(groupid):
    group = Group.objects.get(id=groupid)
    all_GroupMember = GroupMember.objects.filter(group=group).all()
    all_user = []
    for groupmember in all_GroupMember:
        user = User.objects.filter(id=groupmember.user.id).all()
        all_user += user
    return all_user


def comment_to_content(comment, user):
    content = {
        'id': comment.id,
        'document_id': comment.document.id,
        'username': user.username,
        'content': comment.content,
        'datetime': comment.created_time
    }
    return content


def modifiedtime_to_content(du, user):
    content = {
        'document_id': du.document.id,
        'username': user.username,
        'datetime': du.modified_time,
        'content': '修改了文档'
    }
    return content


def created_info(document, user):
    content = {
        'document_id': document.id,
        'username': user.username,
        'datetime': document.created_time,
        'content': '创建了文档'
    }
    return content


def notice_to_content(notice):
    type = notice.type
    sender = User.objects.get(id=notice.sender.id)
    receiver = User.objects.get(id=notice.receiver.id)
    content = {}
    if type == 3 or type == 4:  # 关于文档
        document = notice.document
        content = {
            'id': notice.id,
            'sender_id': notice.sender.id,
            'sender_name': sender.username,
            'receiver_id': notice.receiver.id,
            'receiver_name': receiver.username,
            'group_id': "",
            'group_name': "",
            'document_id': notice.document.id,
            'document_title': document.title,
            'datetime': notice.send_time,
            'content': notice.content,
            'type': notice.type
        }
    elif type == 0 or type == 1 or type == 2 or type == 5 or type == 7 or type == 8 or type == 6 or type == 9:  # 关于小组
        group = notice.group
        content = {
            'id': notice.id,
            'sender_id': notice.sender.id,
            'sender_name': sender.username,
            'receiver_id': notice.receiver.id,
            'receiver_name': receiver.username,
            'group_id': notice.group.id,
            'group_name': group.group_name,
            'document_id': "",
            'document_title': "",
            'datetime': notice.send_time,
            'content': notice.content,
            'type': notice.type
        }
    return content


def del_notice(id):
    notice = Notice.objects.get(id=id)
    notice.delete()


def msg_to_content(sender, receiver, msg):
    content = {
        'id': msg.id,
        'sender_name': sender.username,
        'receiver_name': receiver.username,
        'content': msg.content,
        'send_time': msg.send_time
    }
    return content


@csrf_exempt
def queryuser(request):
    keyword = request.POST.get('keyword')
    groupid = request.POST.get('groupid')
    res = []
    all_user = get_user_bykeyword(keyword)
    all_group_user = get_user_ingroup(groupid)
    for user in all_user:
        check = 1
        for group_user in all_group_user:
            if group_user.id == user.id:
                check = 0
                continue
        if check == 1:
            content = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'description': user.description
            }
            res.append(content)
    return JsonResponse(res, safe=False)


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
    return JsonResponse(res, safe=False)


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
    group_members = GroupMember.objects.filter(user=user).all()
    res = []
    for group_member in group_members:
        group = Group.objects.get(id=group_member.group.id)
        if group.leader.id != user.id:
            res.append(group_to_content(group))
    return JsonResponse(res, safe=False)


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
    return JsonResponse(res, safe=False)


@csrf_exempt
def group_created_byme(request):
    user = User.objects.get(username=request.POST.get('username'))
    groups = Group.objects.filter(leader=user)
    res = []
    for group in groups:
        res.append(group_to_content(group))
    return JsonResponse(res, safe=False)


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
def objectsuser(request):
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
    return JsonResponse(res, safe=False)


@csrf_exempt
def invite_user(request):
    group = Group.objects.get(id=request.POST.get('groupid'))
    user = User.objects.get(id=request.POST.get('userid'))
    sender = User.objects.get(username=request.POST.get('leader_username'))
    try:
        notice = Notice.objects.get(group=group, sender=sender, receiver=user, type=2)
    except Notice.DoesNotExist:
        new_notice = Notice(content=sender.username + "邀请你加入团队(" + group.group_name + ")", sender=sender, receiver=user,
                            group=group, send_time=datetime.datetime.now(), type=2)
        new_notice.save()
        return sendmsg('success')
    if notice is not None:
        return sendmsg('success')


@csrf_exempt
def apply_in_group(request):
    user = User.objects.get(username=request.POST.get('username'))
    group = Group.objects.get(group_name=request.POST.get('groupname'))
    try:
        notice = Notice.objects.get(group=group, sender=user, type=6, receiver=group.leader)
    except Notice.DoesNotExist:
        new_notice = Notice(content=user.username + "申请加入团队(" + group.group_name + ")", sender=user,
                            receiver=group.leader,
                            group=group, send_time=datetime.datetime.now(), type=6)
        new_notice.save()
        return sendmsg('success')
    if notice is not None:
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
        new_document_user = DocumentUser(document=document, user=user, last_watch="1970-01-01 00:00:00",
                                         favorite=0, type=1, modified_time="1970-01-01 00:00:00")
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
    return JsonResponse(res, safe=False)


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
    GroupMember.objects.filter(group=Group.objects.get(id=request.POST.get('groupid'))).delete()
    documents = Document.objects.filter(group=Group.objects.get(id=request.POST.get('groupid')))
    for document in documents:
        DocumentUser.objects.filter(document=document).delete()
    Group.objects.get(id=request.POST.get('groupid')).delete()
    return sendmsg('success')


#
# @csrf_exempt
# def create_personal_doc(request):
#     user = User.objects.get(username=request.POST.get('username'))
#     new_document = Document(title=request.POST.get('title'), group=None, created_time=datetime.datetime.now(),
#                             modified_time=0, creator_id=user.id, modify_right=request.POST.get('modify_right'),
#                             share_right=request.POST.get('share_right'),
#                             discuss_right=request.POST.get('discuss_right'),
#                             others_modify_right=request.POST.get('modify_right'),
#                             others_share_right=request.POST.get('share_right'),
#                             others_discuss_right=request.POST.get('discuss_right'), content=request.POST.get('content'),
#                             recycled=0, is_occupied=0)
#     new_document.save()
#
#     new_document_user = DocumentUser(document=new_document, user=user, last_watch=0, favorite=0, modified_time=0,
#                                      type=0)
#     new_document_user.save()
#     return sendmsg('success')

@csrf_exempt
def create_personal_doc(request):
    msg = ''
    if request.method == 'POST':
        user = User.objects.get(username=request.POST.get('username'))
        msg = "success"
        new_document = Document(title=request.POST.get('title'), created_time=datetime.datetime.now(),
                                modified_time="1970-01-01 00:00:00", creator=user,
                                modify_right=request.POST.get('modify_right'),
                                share_right=request.POST.get('share_right'),
                                discuss_right=request.POST.get('discuss_right'),
                                others_modify_right=request.POST.get('modify_right'),
                                others_share_right=request.POST.get('share_right'),
                                others_discuss_right=request.POST.get('discuss_right'),
                                content=request.POST.get('content'),

                                recycled=0, is_occupied=0)
        new_document.save()

        new_document_user = DocumentUser(document=new_document, user=user, last_watch="1970-01-01 00:00:00",
                                         favorite=0, modified_time="1970-01-01 00:00:00",
                                         type=0)
        new_document_user.save()
    response = {
        'message': msg
    }
    return JsonResponse(response)


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
                            content=request.POST.get('content'), recycled=0, is_occupied=0,
                            modified_time="1970-01-01 00:00:00")
    new_document.save()

    members = GroupMember.objects.filter(group=Group.objects.get(id=request.POST.get('groupid')))
    for member in members:
        new_document_user = DocumentUser(document=new_document, user=member.user, last_watch="1970-01-01 00:00:00",
                                         favorite=0,
                                         modified_time="1970-01-01 00:00:00", type=1)
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
    return JsonResponse(doc_list, safe=False)


@csrf_exempt
def my_created_docs(request):
    user = User.objects.get(username=request.POST.get('username'))
    documents = Document.objects.filter(creator_id=user.id, recycled=0)
    res = []
    for document in documents:
        if document.recycled == 0:
            res.append(document_to_content(document))
    return JsonResponse(res, safe=False)


@csrf_exempt
def my_deleted_docs(request):
    user = User.objects.get(username=request.POST.get('username'))
    documents = Document.objects.filter(creator_id=user.id, recycled=1)
    res = []
    for document in documents:
        res.append(document_to_content(document))
    return JsonResponse(res, safe=False)


@csrf_exempt
def tell_doc_right(request):
    document = Document.objects.get(id=request.POST.get('documentID'))
    user = User.objects.get(username=request.POST.get('username'))
    try:
        document_user = DocumentUser.objects.get(document=document, user=user)
    except DocumentUser.DoesNotExist:
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
        return JsonResponse(response)
    if user.id == document.creator_id:
        if document.group is not None:
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
        if document.group is not None:
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
@csrf_exempt
def get_doccontent(request):
    msg = ''
    mcontent = ''
    mtime = datetime.datetime.now()
    if request.method == 'POST':
        document = Document.objects.get(id=request.POST.get('documentID'))
        user = User.objects.get(username=request.POST.get('username'))
        if (document is None) or (user is None):
            msg = "fail"
            mcontent = ""
            response = {
                'message': msg,
                'content': mcontent
            }
            return JsonResponse(response)
        document_user = DocumentUser.objects.get(document=document, user=user)
        if (document is not None) and (document_user is not None):
            msg = "success"
            mcontent = document.content
            now = datetime.datetime.now()
            mtime = now
            document_user.last_watch = now
            document_user.save()
        else:
            msg = "fail"
            mcontent = ""
    response = {
        'message': msg,
        'content': mcontent,
        'time': mtime
    }
    return JsonResponse(response)


@csrf_exempt
def get_doctitle(request):
    msg = ''
    mtitle = ''
    mtime = datetime.datetime.now()
    if request.method == 'POST':
        document = Document.objects.get(id=request.POST.get('documentID'))
        user = User.objects.get(username=request.POST.get('username'))
        if (document is None) or (user is None):
            msg = "fail"
            mtitle = ""
            response = {
                'message': msg,
                'title': mtitle
            }
            return JsonResponse(response)
        document_user = DocumentUser.objects.get(document=document, user=user)
        if (document is not None) and (document_user is not None):
            msg = "success"
            mtitle = document.title
            now = datetime.datetime.now()
            mtime = now
            document_user.last_watch = now
            document_user.save()
        else:
            msg = "fail"
            mtitle = ""
    response = {
        'message': msg,
        'title': mtitle,
        'time': mtime
    }
    return JsonResponse(response)


# 获取团队所有没有被删除的文档
@csrf_exempt
def get_group_docs(request):
    group = Group.objects.get(id=request.POST.get('groupid'))
    all_document = Document.objects.filter(group=group).all()
    res = []
    for document in all_document:
        res.append(document_to_content(document))
    return JsonResponse(res, safe=False)


@csrf_exempt
def modify_doc(request):
    msg = ''
    if request.method == 'POST':
        document = Document.objects.get(id=request.POST.get('documentID'))
        user = User.objects.get(username=request.POST.get('username'))
        msg = "success"
        now = datetime.datetime.now()
        content = request.POST.get('content')
        document.content = content
        document.modified_time = now
        document.save()
        document_user = DocumentUser.objects.get(document=document, user=user)
        document_user.modified_time = now
        document_user.save()
    response = {
        'message': msg
    }
    return JsonResponse(response)


@csrf_exempt
def query_notindoc_user(request):
    keyword = request.POST.get('keyword')
    # id = request.POST.get('documentID')
    res = []
    all_user = get_user_bykeyword(keyword)
    # all_document_user = get_user_indocument(id)
    for user in all_user:
        # if user not in all_document_user:
        content = {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
        res.append(content)
    return JsonResponse(res, safe=False)


@csrf_exempt
def personal_share_to(request):
    msg = ''
    if request.method == 'POST':
        document = Document.objects.get(id=request.POST.get('documentID'))
        user = User.objects.get(username=request.POST.get('username'))
        target_user = User.objects.get(id=request.POST.get('target_user_username'))
        newDU = DocumentUser(document=document,
                             user=target_user, last_watch="1970-01-01 00:00:00",
                             favorite=0, type=0, modified_time="1970-01-01 00:00:00")

        # 发送消息
        now = datetime.datetime.now()
        send_time = now.strftime('%Y-%m-%d')
        content = user.username + "分享给你了一个文档(" + document.title + ")"
        new_notice = Notice(sender=user, receiver=target_user, document=document,
                            send_time=now, content=content, type=4
                            )
        msg = 'success'
        new_notice.save()
        newDU.save()
    response = {
        'message': msg
    }
    return JsonResponse(response)


@csrf_exempt
def group_doc_share_to(request):
    msg = ''
    if request.method == 'POST':
        document = Document.objects.get(id=request.POST.get('documentID'))
        user = User.objects.get(username=request.POST.get('username'))
        target_user = User.objects.get(id=request.POST.get('target_user_username'))
        newDU = DocumentUser(document=document,
                             user=target_user, last_watch="1970-01-01 00:00:00",
                             favorite=0, type=2, modified_time="1970-01-01 00:00:00")

        # 发送消息
        now = datetime.datetime.now()
        send_time = now.strftime('%Y-%m-%d')
        content = user.username + "分享给你了一个文档(" + document.title + ")"
        new_notice = Notice(sender=user, receiver=target_user, document=document,
                            send_time=now, content=content, type=4
                            )
        msg = 'success'
        new_notice.save()
        newDU.save()
    response = {
        'message': msg
    }
    return JsonResponse(response)


@csrf_exempt
def favor_doc(request):
    msg = ''
    if request.method == 'POST':
        document = Document.objects.get(id=request.POST.get('documentID'))
        user = User.objects.get(username=request.POST.get('username'))
        document_user = DocumentUser.objects.get(document=document, user=user)
        if document is not None and document_user.favorite == 0:
            msg = 'success'
            document_user.favorite = 1
            document_user.save()
        else:
            msg = 'fail'
    response = {
        'message': msg
    }
    return JsonResponse(response)


@csrf_exempt
def cancel_favor_doc(request):
    msg = ''
    if request.method == 'POST':
        document = Document.objects.get(id=request.POST.get('documentID'))
        user = User.objects.get(username=request.POST.get('username'))
        document_user = DocumentUser.objects.get(document=document, user=user)
        if document is not None and document_user.favorite == 1:
            msg = 'success'
            document_user.favorite = 0
            document_user.save()
        else:
            msg = 'fail'
    response = {
        'message': msg
    }
    return JsonResponse(response)


# 查看我收藏的文档
# 收藏的，并且没删除的
@csrf_exempt
def my_favor_doc(request):
    user = User.objects.get(username=request.POST.get('username'))
    document_user = DocumentUser.objects.filter(favorite=1, user=user).all()
    res = []
    for users in document_user:
        document = Document.objects.get(id=users.document.id, recycled=0)
        if document:
            res.append(document_to_content(document))
    return JsonResponse(res, safe=False)


# 修改文档基本信息
@csrf_exempt
def modify_doc_basic(request):
    document = Document.objects.get(id=request.POST.get('documentID'))
    user = User.objects.get(username=request.POST.get('username'))
    if user.id == document.creator_id:
        document.title = request.POST.get('title')
        document.save()
        return sendmsg("success")
    return sendmsg("fail")


# 个人文档创建者将文档设置为私密文档（在点击该按钮时，显示提示信息，其他协作者将看不到该文档）
@csrf_exempt
def set_document_private(request):
    document = Document.objects.get(id=request.POST.get('documentID'))
    user = User.objects.get(username=request.POST.get('username'))
    if user.id == document.creator_id:
        document_users = DocumentUser.objects.filter(document=document).all()
        document_users = document_users.exclude(user=user)
        for users in document_users:
            users.delete()
            users.save()
        return sendmsg("success")
    return sendmsg("fail")


# 团队中的文档，文档创建者将其设置为私密文档（组内将删除该团队文档，转为该创建者的个人文档）
@csrf_exempt
def group_doc_to_personal(request):
    document = Document.objects.get(id=request.POST.get('documentID'))
    user = User.objects.get(username=request.POST.get('username'))
    if user.id == document.creator_id:
        document_users = Document.objects.filter(document=document)
        for document_user in document_users:
            if document_user.id != user.id:
                document_user.delete()
        document.group = None
        document.save()
        return sendmsg("success")
    return sendmsg("fail")


# 文档删除到回收站中
@csrf_exempt
def recycle_doc(request):
    msg = ''
    if request.method == 'POST':
        document = Document.objects.get(id=request.POST.get('documentID'))
        user = User.objects.get(username=request.POST.get('username'))
        if (document is not None) and (document.recycled == 0) and (document.creator.id == user.id):
            msg = 'success'
            document.recycled = 1
            document.save()
        else:
            msg = 'fail'
    response = {
        'message': msg
    }
    return JsonResponse(response)


@csrf_exempt
def recycle_doc_2(request):
    msg = ''
    if request.method == 'POST':
        document = Document.objects.get(id=request.POST.get('documentID'))
        if (document is not None) and (document.recycled == 0):
            msg = 'success'
            document.recycled = 1
            document.save()
        else:
            msg = 'fail'
    response = {
        'message': msg
    }
    return JsonResponse(response)


# 文件从回收站中删除变成二级删除状态
@csrf_exempt
def del_doc(request):
    msg = ''
    if request.method == 'POST':
        document = Document.objects.get(id=request.POST.get('documentID'))
        user = User.objects.get(username=request.POST.get('username'))
        if (document is not None) and (document.recycled == 1) and (document.creator.id == user.id):
            msg = 'success'
            document.recycled = 2
            document.save()
        else:
            msg = 'fail'
    response = {
        'message': msg
    }
    return JsonResponse(response)


# 文档从回收站中恢复
@csrf_exempt
def recover_doc(request):
    msg = ''
    if request.method == 'POST':
        document = Document.objects.get(id=request.POST.get('documentID'))
        user = User.objects.get(username=request.POST.get('username'))
        if (document is not None) and (document.recycled == 1) and (document.creator.id == user.id):
            msg = 'success'
            document.recycled = 0
            document.save()
        else:
            msg = 'fail'
    response = {
        'message': msg
    }
    return JsonResponse(response)


# 文档彻底删除操作
@csrf_exempt
def del_complete_doc(request):
    msg = ''
    if request.method == 'POST':
        document = Document.objects.get(id=request.POST.get('documentID'))
        user = User.objects.get(username=request.POST.get('username'))
        document_user = DocumentUser.objects.get(document=document, user=user)
        print(document is not None)
        print(document.recycled)
        print(document_user.delete_right)
        # if (document!=None) and (document.recycled==1) and (DUlink.delete_right==1):
        if (document is not None) and (document.recycled == 1) and (document.creator.id == user.id):
            msg = 'success'
            document_user.delete()
            comment = Comment.objects.filter(document=document).all()
            comment.delete()
            document.delete()
        else:
            msg = 'fail'
    response = {
        'message': msg
    }
    return JsonResponse(response)


# 显示最近使用文档
# @csrf_exempt
# def show_recent_doc(request):
#     res = []
#     user = get_user_byusername(request.POST.get('username'))
#     all_documentuser = DocumentUser.objects.filter(user=user).order_by('-last_watch').all()
#     all_documentuser = all_documentuser.exclude(last_watch=0).order_by('-last_watch').all()
#     for DU in all_documentuser:
#         document = Document.objects.get(id=DU.document.id)
#         if document is None:
#             continue
#         if document.recycled == 0:
#             res.append(document_to_content(document))
#     return JsonResponse(res, safe=False)


@csrf_exempt
def show_recent_doc(request):
    res = []
    user = get_user_byusername(request.POST.get('username'))
    all_documentuser = DocumentUser.objects.filter(user=user).all().order_by('-last_watch')
    all_documentuser_new = all_documentuser.exclude(last_watch="1970-01-01 00:00:00")
    for DU in all_documentuser_new:
        document = Document.objects.get(id=DU.document.id)
        if document is None:
            continue
        if document.recycled == 0:
            res.append(document_to_content(document))
    return JsonResponse(res, safe=False)


####################################
########## 权限 操作 ###############
####################################

# 1：有权限
# 0：无权限
# 创建者直接权限全给
# 只有创建者才有给别人授予权限的权利

# # 授予权限
# @app.route('/api/grant_right/', methods=['POST'])
# def grant_right():
#     msg=''
#     if request.method=='POST':
#         id=get_newid()
#         document = Document.objects.filter(Document.id == request.POST.get['DocumentID']).first()
#         user = User.objects.filter(User.username==request.POST.get['username']).first()
#         share_right=request.POST.get['share_right']
#         # watch_right=request.POST.get['watch_right']
#         modify_right=request.POST.get['modify_right']
#         # delete_right=request.POST.get['delete_right']
#         #delete_right=0
#         discuss_right=request.POST.get['discuss_right']
#         newDocumentUser=DocumentUser(id=id,document_id=document.id,user_id=user.id,
#             share_right=share_right,watch_right=watch_right,modify_right=modify_right,
#             delete_right=delete_right,discuss_right=discuss_right
#         )
#         db.session.add(newDocumentUser)
#         db.session.commit()
#         response={
#             'message':'grant right success'
#         }
#         return jsonify(response)

# 个人文档创建者修改权限
@csrf_exempt
def modify_personal_doc_right(request):
    msg = ''
    if request.method == 'POST':
        document = Document.objects.get(id=request.POST.get('documentID'))
        others_share_right = request.POST.get('others_share_right')
        # watch_right=request.POST.get['watch_right']
        others_modify_right = request.POST.get('others_modify_right')
        # delete_right=request.POST.get['delete_right']
        others_discuss_right = request.POST.get('others_discuss_right')
        document.others_share_right = others_share_right
        document.others_modify_right = others_modify_right
        document.others_discuss_right = others_discuss_right
        document.save()
        msg = "success"
        #     "watch_right":watch_right,"modify_right":modify_right,"delete_right":delete_right,"discuss_right":discuss_right})
        # db.session.objects(DocumentUser).filter(and_(DocumentUser.document_id==document.id,DocumentUser.user_id==user.id)).update({"share_right":share_right,
        #     "watch_right":watch_right,"modify_right":modify_right,"delete_right":delete_right,"discuss_right":discuss_right})
        # db.session.objects(DocumentUser).filter(and_(DocumentUser.document_id==document.id,DocumentUser.user_id==user.id)).update({"watch_right":watch_right})
        # db.session.objects(DocumentUser).filter(and_(DocumentUser.document_id==document.id,DocumentUser.user_id==user.id)).update({"modify_right":modify_right})
        # db.session.objects(DocumentUser).filter(and_(DocumentUser.document_id==document.id,DocumentUser.user_id==user.id)).update({"delete_right":delete_right})
        # db.session.objects(DocumentUser).filter(and_(DocumentUser.document_id==document.id,DocumentUser.user_id==user.id)).update({"discuss_right":discuss_right})
    response = {
        'message': msg
    }
    return JsonResponse(response)


# 团队文档创建者修改权限
@csrf_exempt
def modify_group_doc_right(request):
    msg = ''
    if request.method == 'POST':
        document = Document.objects.get(id=request.POST.get('DocumentID'))
        user = User.objects.get(username=request.POST.get('username'))
        share_right = request.POST.get('share_right')
        modify_right = request.POST.get('modify_right')
        discuss_right = request.POST.get('discuss_right')
        others_modify_right = request.POST.get('others_modify_right'),
        others_share_right = request.POST.get('others_share_right'),
        others_discuss_right = request.POST.get('others_discuss_right'),
        Document.objects.filter(id=document.id).update({"share_right": share_right,
                                                        "modify_right": modify_right,
                                                        "discuss_right": discuss_right,
                                                        "others_share_right": others_share_right,
                                                        "others_modify_right": others_modify_right,
                                                        "others_discuss_right": others_discuss_right})
        msg = "success"

    response = {
        'message': msg
    }
    return JsonResponse(response)


####################################
########## 评论 操作 ###############
####################################

# 创建评论
@csrf_exempt
def create_comment(request):
    msg = ''
    if request.method == 'POST':
        user = User.objects.get(username=request.POST.get('username'))
        creator_id = user.id
        document = Document.objects.get(id=request.POST.get('documentID'))
        now = datetime.datetime.now()
        content = request.POST.get('content')
        msg = "success"
        newComment = Comment(document=document, creator=user, content=content, created_time=now)
        newComment.save()

        # 发送消息
        send_time = now.strftime('%Y-%m-%d')
        content = user.username + "给你的文档(" + document.title + ")发了一条评论"
        new_notice = Notice(sender=user, receiver=document.creator, document=document,
                            send_time=now, content=content, type=3
                            )
        new_notice.save()
    response = {
        'message': msg
    }
    return JsonResponse(response)


# 获取文档的所有评论
@csrf_exempt
def get_all_comment(request):
    document = Document.objects.get(id=request.POST.get('documentID'))
    all_comment = Comment.objects.filter(document=document).all()
    res = []
    for comment in all_comment:
        user = User.objects.get(id=comment.creator.id)
        res.append(comment_to_content(comment, user))
    res.reverse()
    return JsonResponse(res, safe=False)


# 获取文档所有修改记录
@csrf_exempt
def get_all_modified_time(request):
    res = []
    document = Document.objects.get(id=request.POST.get('documentID'))
    all_modified_time = DocumentUser.objects.filter(document=document)
    all_modified_time = all_modified_time.exclude(modified_time="1970-01-01 00:00:00").order_by('-modified_time')
    for tmp in all_modified_time:
        user = User.objects.get(id=tmp.user.id)
        res.append(modifiedtime_to_content(tmp, user))
    document = Document.objects.get(id=request.POST.get('documentID'))
    user = User.objects.get(id=document.creator.id)
    res.append(created_info(document, user))
    return JsonResponse(res, safe=False)


####################################
########## 消息 操作 ###############
####################################

# 获取用户未读所有的消息
@csrf_exempt
def get_all_notice(request):
    receiver = User.objects.get(username=request.POST.get('receiver_username'))
    all_notice = Notice.objects.filter(receiver=receiver).all()
    res = []
    for notice in all_notice:
        res.append(notice_to_content(notice))
    return JsonResponse(res, safe=False)


# 未读转已读(直接从数据库中删除)
@csrf_exempt
def del_new_notice(request):
    new_notice_id = request.POST.get('new_notice_id')
    del_notice(new_notice_id)
    response = {
        'message': 'success'
    }
    return JsonResponse(response)


# 查看所有不需要确认的消息(type=0,1,3,4,5,7,8,9)
@csrf_exempt
def view_non_confirm_notice(request):
    receiver = User.objects.get(username=request.POST.get('receiver_username'))
    all_notice = Notice.objects.filter(receiver=receiver).all()
    res = []
    for notice in all_notice:
        stat = notice.type
        if stat == 0 or stat == 1 or stat == 3 or stat == 4 or stat == 5 or stat == 7 or stat == 8 or stat == 9:
            res.append(notice_to_content(notice))
    return JsonResponse(res, safe=False)


# 查看所有需要确认的消息(type=2) 需要有两个button，分别发出type=1、5的消息
@csrf_exempt
def view_confirm_notice(request):
    receiver = User.objects.get(username=request.POST.get('receiver_username'))
    all_notice = Notice.objects.filter(receiver=receiver, type=2).all()
    res = []
    for notice in all_notice:
        res.append(notice_to_content(notice))
    print(res)
    return JsonResponse(res, safe=False)


# 查看所有需要确认的消息(type=6) 需要有两个button，分别发出type=7、8的消息
@csrf_exempt
def view_confirm_apply_notice(request):
    receiver = User.objects.get(username=request.POST.get('receiver_username'))
    all_notice = Notice.objects.filter(receiver=receiver, type=6).all()
    res = []
    for notice in all_notice:
        res.append(notice_to_content(notice))
    print(res)
    return JsonResponse(res, safe=False)


# 查看某用户的总未读消息数量
@csrf_exempt
def num_of_notice(request):
    receiver = User.objects.get(username=request.POST.get('receiver_username'))
    all_notice = Notice.objects.filter(receiver=receiver).all()
    cnt = 0
    for notice in all_notice:
        cnt += 1
    content = {
        'notice_cnt': cnt
    }
    return JsonResponse(content)


# 查看用户各种消息类型分别的数量
@csrf_exempt
def all_sort_notice(request):
    receiver = User.objects.get(username=request.POST.get('receiver_username'))
    all_notice = Notice.objects.filter(receiver=receiver).all()
    cnt_normal = 0
    cnt_type2 = 0
    cnt_type6 = 0
    cnt_total = 0
    for notice in all_notice:
        stat = notice.type
        if stat == 2:
            cnt_type2 += 1
        elif stat == 6:
            cnt_type6 += 1
        else:
            cnt_normal += 1
        cnt_total = cnt_type2 + cnt_type6 + cnt_normal
    content = {
        'cnt_type2': cnt_type2,
        'cnt_type6': cnt_type6,
        'cnt_normal': cnt_normal,
        'cnt_total': cnt_total
    }
    return JsonResponse(content)


####################################
########## 私信 操作 ###############
####################################
@csrf_exempt
def sayhi(request):
    receiver = User.objects.get(username=request.POST.get('receiver_username'))
    sender = User.objects.get(username=request.POST.get('sender_username'))
    now = datetime.datetime.now()
    new_msg = Message(sender=sender, receiver=receiver, send_time=now, content='hi')
    new_msg.save()
    response = {
        'message': 'success'
    }
    return JsonResponse(response)


@csrf_exempt
def send_msg_to_sb(request):
    receiver = User.objects.get(username=request.POST.get('receiver_username'))
    sender = User.objects.get(username=request.POST.get('sender_username'))
    now = datetime.datetime.now()
    content = request.POST.get('content')
    new_msg = Message(sender=sender, receiver=receiver, send_time=now, content=content)
    new_msg.save()
    response = {
        'id': id,
        'receiver_name': receiver.username,
        'sender_name': sender.username,
        'send_time': now,
        'content': content
    }
    return JsonResponse(response)


@csrf_exempt
def who_send_msg(request):
    receiver = User.objects.get(username=request.POST.get('receiver_username'))
    all_my_msg = Message.objects.filter(receiver=receiver).all()
    res = []
    for msg in all_my_msg:
        sender = User.objects.get(id=msg.sender.id)
        res.append(msg_to_content(sender, receiver, msg))
    return JsonResponse(res, safe=False)


@csrf_exempt
def our_msg(request):
    receiver = User.objects.get(username=request.POST.get('receiver_username'))
    sender = User.objects.get(username=request.POST.get('sender_username'))
    all_our_msg = Message.objects.filter(receiver=receiver, sender=sender).union(Message.objects.filter(receiver=sender,
                                                                                                        sender=receiver))
    all_our_msg = all_our_msg.order_by('send_time')
    res = []
    for msg in all_our_msg:
        sender = User.objects.get(id=msg.sender.id)
        receiver = User.objects.get(id=msg.receiver.id)
        content = {
            'id': msg.id,
            'sender_name': sender.username,
            'receiver_name': receiver.username,
            'content': msg.content,
            'send_time': msg.send_time
        }
        res.append(content)
    return JsonResponse(res, safe=False)


@csrf_exempt
def send_msg_people(request):
    receiver = User.objects.get(username=request.POST.get('receiver_username'))
    all_my_msg = Message.objects.filter(receiver=receiver).union(Message.objects.filter(sender=receiver))
    res = []
    userlist = []
    for msg in all_my_msg:
        if msg.sender_id == receiver.id:
            sender = User.objects.get(id=msg.receiver.id)
            if sender.id not in userlist:
                userlist.append(sender.id)
                res.append(msg_to_content(sender, receiver, msg))
        else:
            sender = User.objects.get(id=msg.sender.id)
            if sender.id not in userlist:
                userlist.append(sender.id)
                res.append(msg_to_content(sender, receiver, msg))
    return JsonResponse(res, safe=False)
# ------------end------------
