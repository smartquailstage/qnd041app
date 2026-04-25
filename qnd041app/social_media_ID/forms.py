from django import forms

class InstagramPostForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text="Selecciona una o varias categorías."
    )

    class Meta:
        model = InstagramPost
        fields = '__all__'