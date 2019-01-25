from .atom import StrConverter, IntConverter, FloatConverter, BoolConverter


DEFAULT_CONVERTERS = {
    str: StrConverter,
    bool: BoolConverter,
    int: IntConverter,
    float: FloatConverter,
}
