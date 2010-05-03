from django import forms

from apps.distributed.models import Files, Video


class FilesForm(forms.ModelForm):

    class Meta:
        model = Files


class VideoForm(forms.ModelForm):
    supported_media = (
        ('video/x-msvideo')
    )
  
    def clean_file(self):
        data = self.cleaned_data['file']
        if data.content_type not in self.supported_media:
            raise forms.ValidationError("Invalid media-type. Supported media \
                                        types are %s" % self.supported_media)
        return data

    class Meta:
        model = Video
        exclude = ('converted', )
