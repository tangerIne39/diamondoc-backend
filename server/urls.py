from django.urls import path

from .views import *

urlpatterns = [
    # ------------yxy------------
    path('login', login),
    path('get_user', get_user),
    path('get_user_byid', get_user_byid),
    path('logout', logout),
    path('regist', regist),
    path('getalluser', getalluser),
    path('modify_user_info', modify_user_info),
    path('creategroup', creategroup),
    path('modify_group_info', modify_group_info),
    path('mygroup', mygroup),
    path('groupiscreatedbyme', groupiscreatedbyme),
    path('search_group', search_group),
    path('group_created_byme', group_created_byme),
    path('addgroupmember', addgroupmember),
    path('refuse_groupmember', refuse_groupmember),
    path('queryuser', queryuser),
    path('invite_user', invite_user),
    path('apply_in_group', apply_in_group),
    path('accept_application_addgroupmember', accept_application_addgroupmember),
    path('refuse_application_addgroupmember', refuse_application_addgroupmember),
    path('get_user_bygroup', get_user_bygroup),
    path('delete_user', delete_user),
    path('quit_group', quit_group),
    path('delete_group', delete_group),
    path('create_personal_doc', create_personal_doc),
    path('create_group_doc', create_group_doc),
    path('my_docs', my_docs),
    path('my_created_docs', my_created_docs),
    path('my_deleted_docs', my_deleted_docs),
    path('tell_doc_right', tell_doc_right),
    path('tell_current_doc_right', tell_current_doc_right),
    path('', ),
    path('', ),
    path('', ),
    path('', ),
    path('', ),
    path('', ),
    path('', ),
    path('', ),
    path('', ),
    path('', ),
    path('', ),
    path('', ),
    path('', )
    # ------------wlc------------

    # ------------end------------
]
