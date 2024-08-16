from django import forms

from .fields import CommaSeparatedField

NUMBER_OF_WORDS = (
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)

class WordsForm(forms.Form):
    #letters = forms.CharField(help_text='Input letters (separate with commas): e.g "b,e,a,r,m"', widget=forms.HiddenInput())
    letter_list = CommaSeparatedField(help_text='Input letters (separate with commas): e.g "b,e,a,r,m"', label='Letters')
    no_of_letters = forms.ChoiceField(choices=NUMBER_OF_WORDS, widget=forms.RadioSelect(attrs={"id":"no-of-words"}))
