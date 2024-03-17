Django Semantic UI filter
------------------------

[Django Filter](https://github.com/carltongibson/django-filter) with [Semantic UI](https://semantic-ui.com/) style. Semantic UI filters may be used both with [django-semantic-admin](https://github.com/globophobe/django-semantic-admin), as well as outside the admin.


Why?
----

* JavaScript datepicker and timepicker components.
* JavaScript selects, including multiple selections, which integrate well with Django autocomplete fields.
* Semantic UI has libraries for [React](https://react.semantic-ui.com/) and [Vue](https://semantic-ui-vue.github.io/#/), in addition to jQuery. This means you can save time by using django-semantic-filter for simple filtering, and use React or Vue for more complicated use cases.


Install
-------

Install from PyPI:

```
pip install django-semantic-filter
```

Add to `settings.py`:

```python
INSTALLED_APPS = [
    "semantic_filter",
    ...
]
```

Please remember to run `python manage.py collectstatic` for production deployments.

This package use [Fomantic UI](https://fomantic-ui.com/) the official community fork of Semantic UI. Please add the Fomantic UI dependencies to your Django template.

For example:

```
<link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/fomantic-ui@2.8.8/dist/semantic.min.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/fomantic-ui@2.8.8/dist/semantic.min.js"></script>
```
