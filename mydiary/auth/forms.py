#-*- encoding: utf-8 -*-
'''
Created on 2012-11-28

@author: Neil
'''

from diary.mydiary.auth import authenticate
from diary.mydiary.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.template import Context, loader
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.http import int_to_base36
from diary.mydiary.models import User
from diary.mydiary.models import Invite_Code

class UserInfoEditForm(forms.ModelForm):
    '''
    用户修改个人信息的表单
    '''
    name = forms.RegexField(max_length=14, regex=r'^\S+$')
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        self.name_val_error = False
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = User
        fields = ("name",)
    
    def clean_name(self):
        name = self.cleaned_data["name"]
        try:
            User.objects.get(name=name)
        except User.DoesNotExist:
            return name

        self.name_val_error = True
        self.name_error = u'该名号已经被使用了'
        raise forms.ValidationError(_(u"该名号已经被使用了"))
    
    def save(self, commit=True):
        self.user.name = self.cleaned_data["name"]
        if commit:
            self.user.save()
        return self.user
    
class UserCreationForm(forms.ModelForm):
    """
    用户提交注册的表单，用来创建用户
    """
    email = forms.EmailField(label=_("email"))
    name = forms.RegexField(max_length=14, regex=r'^\S+$',
        help_text = _(u"中、英文均可，最长14个字符"),#前面必须加u表示unicode，django输出默认用unicode编码
        error_messages = {'invalid': _(u"仅可以使用中文或英文")})
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    invite_code = forms.CharField(max_length=24)
    
    def __init__(self, *args, **kwargs):
        self.name_val_error = False
        self.email_val_error = False
        self.password1_val_error = False
        self.password2_val_error = False
        self.inv_code_val_error = False
        
        super(forms.ModelForm, self).__init__(*args,**kwargs)#必须调用父类初始化其它数据
        
    class Meta:
        model = User
        fields = ("name", "email",)

    #clean函数会按顺序自动执行
    def clean_name(self):
        name = self.cleaned_data["name"]     
        try:
            User.objects.get(name=name)
        except User.DoesNotExist:
            return name
        
        self.name_val_error = True
        self.name_error = u'该名号已经被使用了'
        raise forms.ValidationError(_(u"该名号已经被使用了"))

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1", "")
        if len(password1) < 6:
            self.password1_val_error = True
            self.password1_error = u'密码长度过短'
            raise forms.ValidationError(_(u"密码长度过短"))

        return password1
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            self.password2_val_error = True
            self.password2_error = u'两次输入的密码不一致'
            raise forms.ValidationError(_(u"两次输入的密码不一致"))
        
        return password2
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        
        self.email_val_error = True
        self.email_error = u'该邮箱已经注册过了'
        raise forms.ValidationError(_(u"该邮箱已经注册过了"))
    
    def clean_invite_code(self):
        inv_code = self.cleaned_data["invite_code"]
        try:
            code = Invite_Code.objects.get(code=inv_code)
            if code.is_actived == True:
                return inv_code
        except Invite_Code.DoesNotExist:
            pass
        
        self.inv_code_val_error = True
        self.inv_code_error = u'邀请码无效'
        raise forms.ValidationError(_(u"邀请码无效"))
        
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    name = forms.RegexField(label=_("name"), max_length=14, regex=r'^\S+$',
        help_text = _("中、英文均可，最长14个字符"),
        error_messages = {'invalid': _("仅可以使用中文或英文")})
    email = forms.EmailField(label=_("email"))
    
    class Meta:
        model = User

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    email/password logins.
    """
    email = forms.EmailField(label=_("email"))
    password = forms.CharField(label=_("password"), widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(_("Please enter a correct username and password. Note that both fields are case-sensitive."))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_("This account is inactive."))

        # TODO: determine whether this should move to its own method.
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError(_("Your Web browser doesn't appear to have cookies enabled. Cookies are required for logging in."))

        return self.cleaned_data

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("E-mail"), max_length=75)

    def clean_email(self):
        """
        Validates that an active user exists with the given e-mail address.
        """
        email = self.cleaned_data["email"]
        self.users_cache = User.objects.filter(
                                email__iexact=email,
                                is_active=True
                            )
        if len(self.users_cache) == 0:
            raise forms.ValidationError(_("That e-mail address doesn't have an associated user account. Are you sure you've registered?"))
        return email

    def save(self, domain_override=None, email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator, request=None):
        """
        Generates a one-use only link for resetting password and sends to the user
        """
        from django.core.mail import send_mail
        for user in self.users_cache:
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            t = loader.get_template(email_template_name)
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': int_to_base36(user.id),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': use_https and 'https' or 'http',
            }
            send_mail(_("Password reset on %s") % site_name,
                t.render(Context(c)), None, [user.email])

class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set his/her password without
    entering the old password
    """
    new_password1 = forms.CharField(label=_("New password"), widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("New password confirmation"), widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        self.password1_val_error = False
        self.password2_val_error = False
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password1(self):
        password1 = self.cleaned_data.get("new_password1", "")
        if len(password1) < 6:
            self.password1_val_error = True
            self.password1_error = u'密码长度过短'
            raise forms.ValidationError(_(u"密码长度过短"))

        return password1
    
    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1", "")
        password2 = self.cleaned_data["new_password2"]
        if password1 != password2:
            self.password2_val_error = True
            self.password2_error = u'两次输入的密码不一致'
            raise forms.ValidationError(_(u"两次输入的密码不一致"))
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user

class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change his/her password by entering
    their old password.
    """
    old_password = forms.CharField(label=_("Old password"), widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.old_password_correct = False#旧密码是否正确的标记
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(_("Your old password was entered incorrectly. Please enter it again."))
        
        self.old_password_correct = True
        return old_password
    
PasswordChangeForm.base_fields.keyOrder = ['old_password', 'new_password1', 'new_password2']

