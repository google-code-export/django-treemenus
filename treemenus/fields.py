from django.forms import ChoiceField
from models import MenuItem

class MenuItemChoiceField(ChoiceField):
    ''' Custom field to display the list of items in a tree manner '''
    def clean(self, value):
        return MenuItem.objects.get(pk=value)
