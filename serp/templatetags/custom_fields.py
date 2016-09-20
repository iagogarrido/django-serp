from django import template

register = template.Library()


@register.simple_tag
def render_field(field, **kwargs):
    return field.as_widget(attrs=kwargs)


@register.simple_tag
def render_field_label(field, **kwargs):
    return field.label_tag(attrs=kwargs)
