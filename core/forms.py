from django import forms
from django.forms import ModelForm
from .models import TaskList, Task, Idea
from users.models import User


class TaskImportForm(forms.Form):
    excel_file = forms.FileField(
        widget=forms.FileInput(
            attrs={"class": "file-input file-input-bordered file-input-primary w-full", "accept": ".xlsx,.xls"}
        )
    )


class TaskListForm(ModelForm):
    """Form for creating and editing task lists."""

    class Meta:
        model = TaskList
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "input input-bordered w-full", "placeholder": "Enter task list name"}
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = "Task List Name"


class TaskForm(ModelForm):
    """Form for creating and editing tasks."""

    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "priority", "assigned_to", "completed"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "input input-bordered w-full", "placeholder": "Enter deadline title"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full",
                    "rows": 4,
                    "placeholder": "Enter Deadline description",
                }
            ),
            "due_date": forms.DateInput(attrs={"class": "input input-bordered w-full", "type": "date"}),
            "priority": forms.NumberInput(
                attrs={"class": "input input-bordered w-full", "placeholder": "Priority (1-5)"}
            ),
            "assigned_to": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "completed": forms.CheckboxInput(attrs={"class": "toggle toggle-primary"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].label = "Task Title"
        self.fields["description"].label = "Description"
        self.fields["description"].required = False
        self.fields["due_date"].label = "Due Date"
        self.fields["due_date"].required = False
        self.fields["priority"].label = "Priority"
        self.fields["priority"].required = False
        self.fields["assigned_to"].label = "Assigned To"
        self.fields["assigned_to"].required = False
        self.fields["assigned_to"].queryset = User.objects.all()
        self.fields["completed"].label = "Mark as completed"
        self.fields["completed"].required = False


class IdeaForm(ModelForm):
    """Form for creating and editing ideas."""

    class Meta:
        model = Idea
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "input input-bordered w-full", "placeholder": "Enter idea name"}),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full h-100",
                    "rows": 40,
                    "placeholder": "Enter idea description",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = "Idea Name"
        self.fields["description"].label = "Description"
        self.fields["description"].required = False


class IdeaImportForm(forms.Form):
    excel_file = forms.FileField(
        widget=forms.FileInput(
            attrs={"class": "file-input file-input-bordered file-input-primary w-full", "accept": ".xlsx,.xls"}
        )
    )
