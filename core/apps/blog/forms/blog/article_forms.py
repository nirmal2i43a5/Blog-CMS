# Django imports
from django import forms
from django.forms import TextInput, Select, FileInput

# Third-party app imports
from ckeditor.widgets import CKEditorWidget

# Blog app imports
from core.apps.blog.models.article_models import Article
from core.apps.blog.models.category_models import Category


class ArticleCreateForm(forms.ModelForm):


    class Meta:

    

        model = Article
        fields = ["title", "category", "image", "image_credit", "body", "tags", "draft"]
        widgets = {
            'title': TextInput(attrs={
                                     'name': "article-title",
                                     'class': "form-control",
                                     'placeholder': "Enter Article Title",
                                     'id': "articleTitle"
                                     }),

            'image': FileInput(attrs={
                                        "class": "form-control clearablefileinput",
                                        "type": "file",
                                        "id": "articleImage",
                                        "name": "article-image"
                                      }

                               ),

            'image_credit': TextInput(attrs={
                'name': "image_credit",
                'class': "form-control",
                'placeholder': "Enter Url of your image",
                'id': "image_credit"
            }),

            'body': forms.CharField(widget=CKEditorWidget(config_name="default", attrs={
                       "rows": 5, "cols": 20,
                       'id': 'content',
                       'name': "article_content",
                       'class': "form-control",
                       })),

            'tags': TextInput(attrs={
                                     'name': "tags",
                                     'class': "form-control",
                                     'placeholder': "tag1, tag2, tag3",
                                     'id': "tags",
                                     'data-role': "tagsinput"
                                     }),

           
        }


class ArticleUpdateForm(forms.ModelForm):
    # category = forms.ModelChoiceField(queryset=Category.objects.filter(
    #                                   approved=True),
    #                                   empty_label="Select Category",
    #                                   widget=forms.Select(attrs=
    #                                                       {
    #                                                           "class": "form-control selectpicker",
    #                                                           "type": "text",
    #                                                           "name": "article-category",
    #                                                           "id": "articleCategory",
    #                                                           "data-live-search": "true"
    #                                                       }
    #                                   )
    #                                 )

    class Meta:
   

        model = Article
        fields = ["title", "category", "image", "image_credit", "body", "tags", "draft"]
        widgets = {
            'title': TextInput(attrs={
                'name': "article-title",
                'class': "form-control",
                'placeholder': "Enter Article Title",
                'id': "articleTitle"
            }),

            'image_credit': TextInput(attrs={
                'name': "image_credit",
                'class': "form-control",
                'placeholder': "Example: made4dev.com (Premium Programming T-shirts)",
                'id': "image_credit"
            }),

          
            'body': forms.CharField(widget=CKEditorWidget(config_name="default", attrs={
                       "rows": 5, "cols": 20,
                       'id': 'content',
                       'name': "article_content",
                       'class': "form-control",
                       })),

            'image': FileInput(attrs={
                "class": "form-control clearablefileinput",
                "type": "file",
                "id": "articleImage",
                "name": "article-image",
            }

            ),

        }
