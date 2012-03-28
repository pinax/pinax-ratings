.. _templates:

Templates
=========

`agon_ratings` comes with one template that is a minimal snippet that gets rendered
from the template tags for displaying the rating form.


_widget.html
------------

This is a snippet that renders the basic HTML form that is used for voting. This works
with out JavaScript enabled, although it does tie in with the bundled jQuery plugin for
extended functionality.

_script.html
------------

This is a snippet that renders the jQuery JavaScript plugin script. It should only
be included once, where you include all the other JavaScript for your application.
This can be overridden and other JavaScript used, although you will have to modify
`_widget.html` as well to match.

_style.html
------------

This is a snippet that renders the provided CSS file for styling the widget. Developers
are encouraged to style the widget in their own way to suit their application. This
CSS file should be considered a starting point
