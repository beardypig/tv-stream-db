#!/usr/bin/env python
import logging

log = logging.getLogger(__name__)


class ValidationError(Exception):
    def __init__(self, message, path=None):
        self.message = message
        self.path = path

    def __str__(self):
        return "[{0}]: {1}".format(
            '->'.join(self.path) if self.path else "root",
            self.message
        )


class Optional(object):
    def __init__(self, key):
        self.key = key


class Schema(object):
    def __init__(self, schema):
        self.schema = schema

    def validate(self, value, path=None):
        return self.schema.validate(value, path or ["root"])


class Validator(object):
    def __init__(self, **kwargs):
        self.has_default = "default" in kwargs
        self.nullable = kwargs.pop("nullable", False)
        self._default = kwargs.pop("default", None)

    def default(self, path=None):
        if self.has_default:
            return self._default
        else:
            raise ValidationError("No default specified where default is required", path)

    def validate(self, value, path=None):
        return value

    def __repr__(self):
        return self.__class__.__name__


class Dict(Validator):
    def __init__(self, schema, **kwargs):
        super().__init__(**kwargs)
        self.schema = schema

    def validate(self, value, path=None):
        path = path or []
        log.debug("Validating Dict: {0}".format("->".join(path)))
        result = {}
        for skey, svalue in self.schema.items():
            if isinstance(skey, Optional):
                # skip missing optional keys
                if skey.key not in value:
                    continue
                skey = skey.key
                cvalue = value[skey]
            elif skey not in value and not svalue.has_default:
                raise ValidationError("Required key `{0}` missing".format(skey), path)
            elif skey not in value and svalue.has_default:
                cvalue = svalue.default(path)
            else:
                cvalue = value[skey]

            result[skey] = svalue.validate(cvalue, path + [skey])

        return result


class Repeating(Validator):
    def __init__(self, schema, **kwargs):
        super().__init__(**kwargs)
        self.schema = schema

    def validate(self, value, path=None):
        path = path or []
        result = []

        for i, item in enumerate(value):
            result.append(self.schema.validate(item, path=path + [str(i)]))

        return result


class TypeValidator(Validator):
    __type__ = None

    def validate(self, value, path=None):
        if self.__type__ is None:
            raise ValueError("TypeValidator.__type__ must be set")
        if not isinstance(value, self.__type__):
            raise ValidationError("`{0}` is not a {0}".format(value, self.__type__.__name__), path)
        return value


class Text(TypeValidator):
    __type__ = str


class Bool(TypeValidator):
    __type__ = bool


class Int(TypeValidator):
    __type__ = int


class Float(TypeValidator):
    __type__ = int


class OneOf(Validator):
    def __init__(self, items, **kwargs):
        super().__init__(**kwargs)
        self.items = items

    def validate(self, value, path=None):
        if value not in self.items:
            raise ValidationError("`{0}` is not one of the permitted values: {1}".format(value, self.items), path)
        return value


class AnyOf(Validator):
    def __init__(self, *subtypes, **kwargs):
        super().__init__(**kwargs)
        self.subtypes = subtypes

    def validate(self, value, path=None):
        for subtype in self.subtypes:
            try:
                return subtype.validate(value, path)
            except ValidationError:
                pass
        raise ValidationError("`{0}` is not one of the subtypes: {1}".format(value, self.subtypes), path)


class Null(Validator):
    def __init__(self, **kwargs):
        if "default" in kwargs:
            kwargs["default"] = None
        super().__init__(**kwargs)

    def validate(self, value, path=None):
        if value is not None:
            raise ValidationError("`{0}` is not None".format(value), path)


__all__ = [
    "Schema", "Dict", "Text", "Bool", "AnyOf", "OneOf", "Int", "Float", "Repeating", "Optional", "Null"
]