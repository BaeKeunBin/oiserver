# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class UserInfo(models.Model):
    userID = models.CharField(max_length=200)
    userName = models.CharField(max_length=200)
    userPF = models.CharField(max_length=200)
    userNickName = models.CharField(max_length=200,default="default")
    def __unicode__(self):
        return self.userName

class UserRoom(models.Model):
	#userID = models.ForeignKey(UserInfo, on_delete=models.CASCADE) #userId 를 외래키로 바꾸는 방법 대신 assign 방법을 찾아야 사용 가능
	userID = models.CharField(max_length=200)
	userNickName = models.CharField(max_length=200,default = "default")
	roomName = models.CharField(max_length=100,default = "default")
	roomJson = models.TextField()
	isProfile = models.CharField(max_length=50)

	def __unicode__(self):
		return self.userNickName

class UserImage(models.Model):
	userNickName = models.CharField(max_length=200,default = "default")
	imageData = models.ImageField(upload_to="image/")

	def filename(self):
		return os.path.basename(self.imageData.name)
		
	def __unicode__(self):
		return self.userNickName

class UserVideo(models.Model):
	userNickName = models.CharField(max_length=200,default = "default")
	videoData = models.FileField(upload_to="video/")

	def filename(self):
		return os.path.basename(self.videoData.name)
		
	def __unicode__(self):
		return self.userNickName

class MultiPlayRoom(models.Model):
	host = models.CharField(max_length=200,default = "default")
	mulRoomName = models.CharField(max_length=200,default = "default")
	roomJson = models.TextField(default = "default")
	NumPeople = models.IntegerField(default = "1")

	def __unicode__(self):
		return self.mulRoomName