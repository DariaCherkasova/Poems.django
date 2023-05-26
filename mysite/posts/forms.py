from django import forms
from .models import Post, User, Profile


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text',)


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email',)


'''class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('images',)'''