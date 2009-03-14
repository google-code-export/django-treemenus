from itertools import chain

from django.db import models
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _
from django.db.models.related import RelatedObject

class MenuItem(models.Model):
    parent = models.ForeignKey('self', verbose_name=_('Parent'), null=True, blank=True)
    caption = models.CharField(_('Caption'), max_length=50, help_text=_("The name of the menu item"))
    url_template = models.TextField(_('URL Template'), null=True, blank=True, help_text=_("Define your URL with the django template language, eg '{% url blog \"awesome\" %}'. Your links can be hardcoded, or calculated, or a combination thereof."))
    level = models.IntegerField(_('Level'), default=0, editable=False)
    rank = models.IntegerField(_('Rank'), default=0, editable=False)
    menu = models.ForeignKey('Menu', related_name='contained_items', verbose_name=_('Menu'), null=True, blank=True, editable=False)
    
    def as_subclass(self):
        """
        Looks through all related objects, and returns the first subclass it finds (on the assumption that there is only one)
        """
        related = self._meta.get_all_related_objects()
        
        for i in related:
            if issubclass(i.model, type(self)):
                if not i.model is type(self):
                    #it's a subclass
                    return getattr(self, i.get_accessor_name())
        #none found, just return self
        return self
    
    def __unicode__(self):
        return self.caption
        
    def save(self, *args, **kwargs):
        from treemenus.utils import clean_ranks

        # Calculate level
        old_level = self.level
        if self.parent:
            self.level = self.parent.level + 1
        else:
            self.level = 0
        
        if self.pk:
            new_parent = self.parent
            old_parent = MenuItem.objects.get(pk=self.pk).parent
            if old_parent != new_parent:
                #If so, we need to recalculate the new ranks for the item and its siblings (both old and new ones).
                if new_parent:
                    clean_ranks(new_parent.children()) # Clean ranks for new siblings
                    self.rank = new_parent.children().count()
                super(MenuItem, self).save(*args, **kwargs) # Save menu item in DB. It has now officially changed parent.
                if old_parent:
                    clean_ranks(old_parent.children()) # Clean ranks for old siblings
            else:
                super(MenuItem, self).save(*args, **kwargs) # Save menu item in DB
        
        else: # Saving the menu item for the first time (i.e creating the object)
            if not self.has_siblings():
                # No siblings - initial rank is 0.
                self.rank = 0
            else:
                # Has siblings - initial rank is highest sibling rank plus 1.
                siblings = self.siblings().order_by('-rank')
                self.rank = siblings[0].rank + 1
            super(MenuItem, self).save(*args, **kwargs)
       
        # If level has changed, force children to refresh their own level
        if old_level != self.level:
            for child in self.children():
                child.save() # Just saving is enough, it'll refresh its level correctly.
    
    def delete(self):
        from treemenus.utils import clean_ranks
        old_parent = self.parent
        super(MenuItem, self).delete()
        if old_parent:
            clean_ranks(old_parent.children())
            
    def caption_with_spacer(self): 
        spacer = u'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' * self.level
        if self.level > 0:
            spacer += u'&#x2517;&nbsp;' # tree symbol
        return spacer + self.caption
    
    def get_flattened(self):
        flat_structure = [self]
        for child in self.children():
            flat_structure = chain(flat_structure, child.get_flattened())
        return flat_structure
    
    def siblings(self):
        if not self.parent:
            return type(self).objects.none()
        else:
            if not self.pk: # If menu item not yet been saved in DB (i.e does not have a pk yet)
                return self.parent.children()
            else:
                return self.parent.children().exclude(pk=self.pk)
    
    def hasSiblings(self):
        import warnings
        warnings.warn('hasSiblings() is deprecated, use has_siblings() instead.', DeprecationWarning, stacklevel=2)
        return self.has_siblings()
    
    def has_siblings(self):
        return self.siblings().count() > 0
    
    def children(self):
        _children = type(self).objects.filter(parent=self).order_by('rank',)
        for child in _children:
            child.parent = self # Hack to avoid unnecessary DB queries further down the track.
        return _children
    
    def hasChildren(self):
        import warnings
        warnings.warn('hasChildren() is deprecated, use has_children() instead.', DeprecationWarning, stacklevel=2)
        return self.has_children()
    
    def has_children(self):
        return self.children().count() > 0


class Menu(models.Model):
    name = models.CharField(_('Name'), max_length=50)
    root_item = models.ForeignKey(MenuItem, related_name='is_root_item_of', verbose_name=_('Root Item'), null=True, blank=True, editable=False)

    def save(self, force_insert=False, force_update=False):
        if not self.root_item:
            root_item = MenuItem(caption=ugettext('Root')) #cannot be lazy
            if not self.pk: # If creating a new object (i.e does not have a pk yet)
                super(Menu, self).save(force_insert, force_update) # Save, so that it gets a pk
                force_insert = False
            root_item.menu = self
            root_item.save() # Save, so that it gets a pk
            self.root_item = root_item
        super(Menu, self).save(force_insert, force_update)

    def delete(self):
        if self.root_item is not None:
            self.root_item.delete()
        super(Menu, self).delete()
        
    def __unicode__(self):
        return self.name
    
    def root(self):
        return self.root_item.as_subclass()
    
    class Meta:
        verbose_name = _('Menu')
        verbose_name_plural = _('Menus')
