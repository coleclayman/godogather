import datetime
from location_picker import LocationPickerWidget

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm, UserChangeForm

from .models import Event, Group, Profile, FriendList

#Event forms

valid_time_formats = ['%I:%M %p', '%P', '%H:%M%A', '%H:%M %A', '%H:%M%a', '%H:%M %a']


class BasicEventCreate(forms.Form):
    summary = forms.CharField()
    date_happening = forms.DateField(initial=datetime.datetime.now())
    time_starting = forms.TimeField(input_formats=valid_time_formats)
    location = forms.CharField()
    test_location = forms.CharField()



class EventModelCreateForm(forms.ModelForm):
    date_happening = forms.DateField(initial=datetime.datetime.now())
    time_starting = forms.TimeField(input_formats=valid_time_formats)
    time_ending = forms.TimeField(input_formats=valid_time_formats)




    class Meta:
        model = Event
        exclude = ['date_posted', 'people_coming', 'people_not_coming']

    def __init__(self, *args, **kwargs):
        super(EventModelCreateForm, self).__init__(*args, **kwargs)
        self.fields["host"].widget = forms.CheckboxSelectMultiple()
        self.fields["groups"].widget = forms.CheckboxSelectMultiple()
        self.fields["test_location"].widget = LocationPickerWidget()
        self.fields["location"].required = True
        self.fields["name"].required = True
        self.fields["date_happening"].required = True
        self.fields["time_starting"].required = True
        self.fields["time_ending"].required = True
        self.fields["description"].required = False
        self.fields["description"].widget = forms.Textarea(attrs={'rows': '4'})


class EventModelUpdateForm(forms.ModelForm):  

    date_happening = forms.DateField()
    time_starting = forms.TimeField(input_formats=valid_time_formats)
    time_ending = forms.TimeField(input_formats=valid_time_formats)

    class Meta:
        model = Event
        exclude = ['date_posted', 'people_coming', 'people_not_coming']

    def __init__(self, *args, **kwargs):
        super(EventModelUpdateForm, self).__init__(*args, **kwargs)
        self.fields["host"].widget = forms.CheckboxSelectMultiple()
        self.fields["groups"].widget = forms.CheckboxSelectMultiple()
        self.fields["test_location"].widget = LocationPickerWidget()
        self.fields["location"].required = True
        self.fields["name"].required = True
        self.fields["date_happening"].required = True
        self.fields["time_starting"].required = True
        self.fields["time_ending"].required = True
        self.fields["description"].required = False
        self.fields["description"].widget = forms.Textarea(attrs={'rows': '4'})




#Group forms
class GroupModelCreateForm(forms.ModelForm):  
    class Meta:
        model = Group
        exclude = ['members', 'member_requests']

    def __init__(self, *args, **kwargs):
        super(GroupModelCreateForm, self).__init__(*args, **kwargs)
        self.fields["admin"].widget = forms.CheckboxSelectMultiple()        
        self.fields["name"].required = True
        self.fields["description"].required = True
        self.fields["description"].widget = forms.Textarea(attrs={'rows': '4'})



class GroupModelUpdateForm(forms.ModelForm):  
    class Meta:
        model = Group
        exclude = ['member_requests', 'admin']

    def __init__(self, *args, **kwargs):
        super(GroupModelUpdateForm, self).__init__(*args, **kwargs)
        self.fields["members"].widget = forms.CheckboxSelectMultiple()       
        self.fields["name"].required = True
        self.fields["description"].required = True
        self.fields["description"].widget = forms.Textarea(attrs={'rows': '4'})



#Profile / User forms
class SearchProfile(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'search', 'placeholder': 'Search for friends!', 'class': 'form-control'}))


class UserLogin(forms.Form):  
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())


class UserModelCreateForm(UserCreationForm):  
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        new_user = super(UserCreateForm, self).save(commit=False)
        new_user.email = self.cleaned_data["email"]
        new_profile = Profile.objects.create(user=new_user)
        new_profile.save()
        if commit:
            new_user.save()
        return user


class UserModelUpdateForm(UserChangeForm):  
    class Meta:
        model = User
        exclude = ['name']


class ProfileModelCreateForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    verification = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "What is 2+4?"}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': '5'}))
    class Meta:
        model = Profile
        exclude = ['user', 'new_user', 'friends', 'events_posted', 'shared_events', 'group_requests', 'friend_requests', 'past_events', 'followers']


class ProfileModelUpdateForm(forms.ModelForm):  
    class Meta:
        model = Profile
        exclude = ['user', 'past_events', 'friends', 'friend_requests', 'events_posted', 'shared_events', 'group_requests', 'followers']


class ContactForm(forms.Form):
    author = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'author', 'placeholder': 'Your name *', 'class': 'form-control'}))
    comment = forms.CharField(required=True, widget=forms.Textarea(attrs={'id': 'comment', 'placeholder': 'Your message *', 'class': 'form-control', 'rows': '4'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'id': 'email', 'placeholder': 'Your email *', 'class': 'form-control'}))


class CommentForm(forms.Form):
    message = forms.CharField(required=False, label="Enter your comment here!", widget=forms.Textarea(attrs={'id': 'comment_body', 'class': "form-control", 'placeholder':"Why I oughta..."}))


class FriendListCreate(forms.Form):
    name = forms.CharField(required=False, label="Enter the name of your new Friend List here!", widget=forms.TextInput(attrs={'id': 'comment_body', 'class': "form-control", 'placeholder':"Type the name here"}))


class ContactCreate(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'id': 'name-input', 'class': "form-control", 'placeholder':"Who is it?", 'style': 'width: 80%'}))
    contact_method = forms.CharField(widget=forms.TextInput(attrs={'id': 'method-input', 'class': "form-control", 'placeholder':"Email or phone #", 'style': 'width: 80%'}))
