from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    根据字典的键获取对应的值
    :param dictionary: 字典对象
    :param key: 键
    :return:
    """
    return dictionary.get(key)

def split(value, key):
    """
        Returns the value turned into a list.
    """
    return value.split(key)


