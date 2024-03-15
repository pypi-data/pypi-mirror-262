"""Flag provides a strongly typed descriptor field for booleans."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from vistutils.fields import AbstractField
from vistutils.text import monoSpace


class Flag(AbstractField):
  """The IntField class provides a strongly typed descriptor containing
  integers."""

  __strictly_valued__ = True

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the descriptor."""
    self.__strictly_valued__ = kwargs.get('strict', True)
    kwargs = {}
    for (key, val) in kwargs.items():
      if key != 'strict':
        kwargs |= {key: val}
    AbstractField.__init__(self, *args, **kwargs)

  def _parseDefault(self, ) -> Any:
    """Parses the default value."""
    kVal = self._getKwargs()
    args = [*self.__positional_args__, kVal]
    for arg in args:
      if arg is True or arg is False:
        return arg
    if len(self.__positional_args__) > 1:
      return True
    if kVal is not None:
      return True if kVal else False
    if args:
      return True if args[0] else False
    return False

  def _typeGuard(self, value: Any, **kwargs) -> bool:
    """Guards the type."""
    if self.__strictly_valued__:
      if value is True or value is False:
        return True
      e = """This Flag instance is strictly valued, meaning that only True 
      and False are allowed. This may be relaxed by setting keyword 
      argument 'strict' to False, (default is True). In relaxed mode, 
      the boolean value replaces the given value making every object a 
      valid value. """
      raise TypeError(monoSpace(e))
    return True
