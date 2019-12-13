from django.contrib import admin

# Register your models here.

from .models import DATASET_NLP, DATASET_ANSWER
admin.site.register(DATASET_NLP)
admin.site.register(DATASET_ANSWER)