This page lists features that have been deprecated. Those features will raise a deprecation warning when you use them, and will eventually be removed in a future release.

# Deprecated in 0.7 #

Two methods have changed names to comply with Django's code guidelines:

  * `MenuItem.hasSiblings()`
> You should use `MenuItem.has_siblings()` instead.
  * `MenuItem.hasChildren()`
> You should use `MenuItem.has_children()` instead.