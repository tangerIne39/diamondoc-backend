from django.db import models


# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    description = models.TextField()


class Group(models.Model):
    group_name = models.CharField(max_length=255)
    leader = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField()
    description = models.TextField()


class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Document(models.Model):
    title = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    content = models.TextField()

    modify_right = models.IntegerField()
    share_right = models.IntegerField()
    discuss_right = models.IntegerField()

    others_modify_right = models.IntegerField()
    others_share_right = models.IntegerField()
    others_discuss_right = models.IntegerField()

    recycled = models.IntegerField()
    is_occupied = models.IntegerField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class DocumentUser(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_watch = models.DateTimeField()
    favorite = models.IntegerField()
    modified_time = models.DateTimeField()
    type = models.IntegerField()


class Comment(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_time = models.DateTimeField()


class Notice(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='n_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='n_receiver')
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    send_time = models.DateTimeField()
    content = models.TextField()
    type = models.IntegerField()


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='m_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='m_receiver')
    send_time = models.DateTimeField()
    content = models.TextField()
