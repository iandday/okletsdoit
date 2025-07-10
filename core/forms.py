from django import forms
from .models import TaskList, Task
from users.models import User


class TaskImportForm(forms.Form):
    excel_file = forms.FileField()


class TaskListForm(forms.ModelForm):
    """Form for creating and editing task lists."""

    class Meta:
        model = TaskList
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "input input-bordered w-full", "maxlength": 60, "required": True})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = "Task List Name"


class TaskForm(forms.ModelForm):
    """Form for creating and editing tasks."""

    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "priority", "assigned_to", "completed"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "input input-bordered w-full", "maxlength": 250, "required": True}
            ),
            "description": forms.Textarea(attrs={"class": "textarea textarea-bordered w-full", "rows": 3}),
            "due_date": forms.DateInput(attrs={"class": "input input-bordered w-full", "type": "date"}),
            "priority": forms.NumberInput(attrs={"class": "input input-bordered w-full", "min": 1, "max": 5}),
            "assigned_to": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "completed": forms.CheckboxInput(attrs={"class": "checkbox checkbox-primary"}),
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
