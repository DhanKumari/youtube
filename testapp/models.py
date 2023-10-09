from django.db import models

# Create your models here.
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from datetime import datetime
import json

class task(models.Model):
    name=models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(max_length=200, null=True,blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class taskDate(models.Model):
    ttask = models.ForeignKey(task, on_delete = models.CASCADE)
    date= models.CharField(max_length=100)
    def __str__(self):
        return self.ttask

class history(models.Model):
    hist = models.TextField(default='{}')



#method2 using decorator 
@receiver(pre_save, sender=task)
def task_handler(sender, instance,**kwargs):
    print("method 2")
    #print(instance)
    #print(slugify(instance.name))
    instance.slug = (slugify(instance.name))

@receiver(post_save, sender=task)
def task_handler_post(sender, instance,**kwargs):
    taskDate.objects.create(ttask= instance, date=datetime.now())
    print("method 2")
    #print(instance)

@receiver(pre_delete, sender=task)
def task_handler_pre_delete(sender, instance,**kwargs):
    data={'ttask':instance.name,'disc':instance.description,'slug':instance.slug}
    history.objects.create(hist=json.dumps(data))
    #print("method 2")
    #print(instance)

  



#method 1

##pre save signal
# def task_handler(sender, instance,**kwargs):
#     print("hello")
#     print(instance)
#     print(instance.description)


# pre_save.connect(task_handler, sender= task)