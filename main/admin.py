from django.contrib import admin

from main import models


admin.site.register(models.User)
admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.Tag)
