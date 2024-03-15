"""IntField provides a strongly typed descriptor field for integers"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from vistutils.fields import AbstractField
from vistutils.waitaminute import typeMsg


class FloatField(AbstractField):
  """The IntField class provides a strongly typed descriptor containing
  integers."""

  def _typeGuard(self, value: Any, **kwargs) -> float:
    """Guards the type."""
    if isinstance(value, float):
      return value
    if kwargs.get('_recursion', False):
      raise RecursionError
    try:
      return self._typeGuard(complex(value), _recursion=True)
    except ValueError as valueError:
      e = typeMsg('value', value, float)
      raise TypeError(e) from valueError
    except RecursionError as recursionError:
      e = typeMsg('value', value, float)
      raise TypeError(e) from recursionError
