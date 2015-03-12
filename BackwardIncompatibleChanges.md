# Changes made after 0.5 #

If you were not using the extension system, then the changes are pretty simple (see 1. and 2.). If you were, it's a little more complex but still easy to overcome (see 3.).

In any case, no change needs to be done in the database. Everything will work as before. The below changes only apply to your code.

## 1. Template directory ##

No need to declare the template directory any more, so remove it from your settings file:

```
TEMPLATE_DIRS = (
    ...
    '/home/Python/Lib/site-packages/treemenus/templates/', # Unnecessary: Remove this line!!
)
```

## 2. URLConf ##

No need to declare the admin url for the `treemenus` application, so remove it from your URLConf:

```
urlpatterns = patterns('',
    ...
    (r'^admin/treemenus/', include('treemenus.admin_urls')), # Unnecessary: Remove this line!!
    ...
)
```

## 3. Extension system ##

If you were not using the extension system, then you're done with the incompatible changes.

The extension system has changed quite a lot. Although your database will remain untouched, some changes need to be done.

### 3.a. Extension settings ###

You need to remove the following lines from your settings, as they're not used any more:

```
TREE_MENU_ITEM_EXTENSION_MODEL = 'menu_extension.models.MenuItemExtension'
TREE_MENU_ITEM_EXTENSION_FORM = 'menu_extension.forms.MenuItemExtensionForm'
```

### 3.b. Extension model definition ###

Instead of a `ForeignKey` you now need to use a `OneToOneField`:

```
Before:

class MenuItemExtension(models.Model):
    menu_item = models.ForeignKey(MenuItem, unique=True, editable=False)
    ...

After:

class MenuItemExtension(models.Model):
    menu_item = models.OneToOneField (MenuItem, related_name="extension")
    ...

Don't forget to set the `related_name` parameter, preferably to `"extension"`.
```

### 3.c. `get_extension` method ###

As a result of the model change above, the `get_extension` method does not exist any more. Instead use the attribute which is set in the `related_name` parameter, preferably to `"extension"`. For example, in you templates:

```
{% if menu_item.extension.published %}
    <li><a href="{{ menu_item.url }}">{{ menu_item.caption }}</a></li>
{% endif %}
```

### 3.d. Extension admin declaration ###

Now extension models are manage with inline forms. To declare your extension model in the admin, you therefore need to proceed as follows, in your project's main `admin.py`:

```
from treemenus.admin import MenuAdmin, MenuItemAdmin
from treemenus.admin import Menu

# Custom Menu Admin
class MenuItemExtensionInline(admin.StackedInline):
    model = MenuItemExtension
    max_num = 1

class CustomMenuItemAdmin(MenuItemAdmin):
    inlines = [MenuItemExtensionInline,]

class CustomMenuAdmin(MenuAdmin):
    menu_item_admin_class = CustomMenuItemAdmin

admin.site.unregister(Menu)
admin.site.register(Menu, CustomMenuAdmin)
```