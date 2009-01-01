
from weakref import proxy
class WeakProperty(object):
    def __get__(self, instance, klass):
        return self.value
    def __set__(self, instance, value):
        if value is None:
            self.value = None
        else:
            self.value = proxy(value)
    def __delete__(self, instance):
        del self.value

