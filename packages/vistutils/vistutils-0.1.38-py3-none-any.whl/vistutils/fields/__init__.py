"""The fields module provides a collection of descriptor classes. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._abstract_field import AbstractField
from ._flag import Flag
from ._int_field import IntField
from ._float_field import FloatField
from ._complex_field import ComplexField
from ._text_field import TextField

#  lmao
from ._static_field import StaticField
from ._field_box import FieldBox
from ._break_point import BreakPoint

from ._unparse_args import unParseArgs
from ._core_descriptor import CoreDescriptor
from ._mutable_descriptor import MutableDescriptor
from ._immutable_decriptor import ImmutableDescriptor
from ._typed_field import TypedField
from ._wait import Wait
