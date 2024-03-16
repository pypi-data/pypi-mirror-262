def _explode_tw2validationerror(exception):
    # Fetch all the children and grandchildren of a widget
    widget = exception.widget
    widget_children = _navigate_tw2form_children(widget.child)

    errors = dict((child.compound_key, child.error_msg) for child in widget_children)
    return {'errors': errors, 'values': widget.child.value}


def _navigate_tw2form_children(w):
    if getattr(w, 'compound_key', None):
        # If we have a compound_key it's a leaf widget with form values
        yield w
    else:
        child = getattr(w, 'child', None)
        if child:
            # Widgets with "child" don't have children, but their child has
            w = child

        for c in getattr(w, 'children', []):
            for cc in _navigate_tw2form_children(c):
                yield cc
