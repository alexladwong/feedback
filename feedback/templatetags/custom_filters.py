from django import template

register = template.Library()

@register.filter(name="add_placeholder")
def add_placeholder(field, placeholder_text):
    """Ensure the filter works only on form fields and adds a placeholder."""
    if hasattr(field, "field"):  # Check if it's a form field
        field.field.widget.attrs["placeholder"] = placeholder_text
    return field
