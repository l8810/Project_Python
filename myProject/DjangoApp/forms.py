from django import forms
from django.core.exceptions import ValidationError
from .models import Person, Task, User


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['team', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['team'].required = True
        self.fields['team'].widget.attrs.update({'required': 'required'})
        self.fields['team'].empty_label = "חובה לבחור צוות"



from django import forms
from .models import Task
from django.utils import timezone
from django.core.exceptions import ValidationError


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'date_end', 'Executor', 'status']

        labels = {
            'title': 'כותרת המשימה',
            'description': 'תיאור המשימה',
            'date_end': 'תאריך יעד לסיום',
            'Executor': 'מבצע המשימה',
            'status': 'סטטוס',
        }

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'הכנס כותרת ברורה...',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'פרט את שלבי המשימה...',
                'rows': 4,
                'class': 'form-control'
            }),
            'date_end': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'min': timezone.now().date().isoformat()  # חוסם תאריכים שעברו
                }),
            'Executor': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise ValidationError("הכותרת קצרה מדי. אנא תאר את המשימה ב-5 תווים לפחות.")
        return title


    class LoginForm(forms.Form):
        username = forms.CharField(
            label="שם משתמש",
            widget=forms.TextInput(attrs={'placeholder': 'הכנס שם משתמש...'})
        )
        password = forms.CharField(
            label="סיסמה",
            widget=forms.PasswordInput(attrs={'placeholder': 'הכנס סיסמה...'})
        )