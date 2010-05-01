from django.forms import ModelForm
from apps.distributed.models import Files, Video


class FilesForm(ModelForm):

    class Meta:
        model = Files


class VideoForm(ModelForm):

    class Meta:
        model = Video
        exclude = ('converted',)
