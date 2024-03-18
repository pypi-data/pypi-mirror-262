import builtins
import enum
import inspect
import types
import typing

from sp2.impl.__sp2typesimpl import _sp2typesimpl


class EnumMeta(_sp2typesimpl.PySp2EnumMeta):
    def __new__(cls, name, bases, dct):
        metadata = {}
        last_value = -1

        # Disallow subclassing an enum
        EnumMeta._check_for_existing_members(bases)

        for k, v in dct.items():
            # Allow methods and properties and hidden methods
            if (
                (k[0] == "_" and k[-1] == "_")
                or v is enum.auto
                or isinstance(v, (types.FunctionType, builtins.property, builtins.classmethod, builtins.staticmethod))
            ):
                continue

            if isinstance(v, enum.auto):
                v = last_value + 1

            if not isinstance(v, int):
                raise TypeError(f"sp2.Enum expected int enum value, got {type(v).__name__} for field {k}")

            metadata[k] = v
            last_value = v

        dct["__metadata__"] = metadata
        return super().__new__(cls, name, bases, dct)

    def __iter__(self):
        for k, v in self.__metadata__.items():
            yield self(k)

    @property
    def __members__(self):
        # For compatibility with python Enum
        return types.MappingProxyType(self.__metadata__)

    @staticmethod
    def _check_for_existing_members(bases):
        for base in bases:
            if isinstance(base, _sp2typesimpl.PySp2EnumMeta) and base.__members__:
                raise TypeError("Cannot extend sp2.Enum %r: inheriting from an Enum is prohibited" % base.__name__)


class Enum(_sp2typesimpl.PySp2Enum, metaclass=EnumMeta):
    auto = enum.auto

    def __reduce__(self):
        return type(self), (self.value,)

    def __repr__(self):
        return f"<{type(self).__name__}.{self.name}: {self.value}>"

    def __str__(self):
        return f"{type(self).__name__}.{self.name}"


def DynamicEnum(name: str, values: typing.Union[dict, list], start=0, module_name=None):
    """create a sp2.Enum type dynamically
    :param name: name of the class type
    :param values: either a dictionary of key : values or a list of enum names
    :param start: when providing a list of values, will start enumerating from start
    """

    if isinstance(values, list):
        values = {k: v + start for v, k in enumerate(values)}
    else:
        values = values.copy()

    if module_name is None:
        module_name = inspect.currentframe().f_back.f_globals["__name__"]
    values["__module__"] = module_name

    return EnumMeta(name, (Enum,), values)
