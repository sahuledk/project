from django.forms import ModelForm
from .models import Project,Review
from django import forms
class ProjectForm(ModelForm):

    class Meta:
        model = Project
        fields = ['title','featured_image','description', 'source_link', 'demo_link'] 

        widgets = {
            'tags' :forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['body', 'value']
        labels = {'body': 'Add your Review here', 'value': 'Place your vote here'}

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

