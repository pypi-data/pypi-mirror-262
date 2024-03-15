"""The field box wraps the class in brackets."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Never


class FieldBox:
  """The field box wraps the class in brackets."""

  __positional_args__ = None
  __keyword_args__ = None
  __field_name__ = None
  __field_type__ = None
  __field_owner__ = None

  @classmethod
  def __class_getitem__(cls, innerCls: type) -> Any:
    """Returns a new Field with the inner class as the field type."""
    return cls(innerCls)

  def __init__(self, cls: type) -> None:
    """Initializes the field."""
    self.__field_type__ = cls

  def __call__(self, *args, **kwargs) -> Any:
    """Returns the field."""
    self.__positional_args__ = [*args, ]
    self.__keyword_args__ = {**kwargs, }
    return self

  def __set_name__(self, owner: type, name: str) -> None:
    """Sets the name of the field."""
    self.__field_name__ = name
    self.__field_owner__ = owner

  def _getFieldName(self, ) -> str:
    """Getter-function for private field name"""
    return self.__field_name__

  def _getPrivateFieldName(self, ) -> str:
    """Getter-function for private field name"""
    return '_%s' % self.__field_name__

  def _getArgs(self) -> list:
    """Getter-function for positional arguments"""
    return self.__positional_args__

  def _getKwargs(self) -> dict:
    """Getter-function for keyword arguments"""
    return self.__keyword_args__

  def _instantiate(self, instance: object, ) -> Any:
    """Instantiates the field."""
    pvtName = self._getPrivateFieldName()
    value = self.__field_type__(*self._getArgs(), **self._getKwargs())
    setattr(instance, pvtName, value)

  def __get__(self, instance: object, owner: type, **kwargs) -> Any:
    """Returns the field."""
    if instance is None:
      return self
    pvtName = self._getPrivateFieldName()
    if getattr(instance, pvtName, None) is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._instantiate(instance)
      return self.__get__(instance, owner, _recursion=True, )
    return getattr(instance, pvtName)

  def __set__(self, *_) -> Never:
    """Must be implemented in subclass"""
    e = """Instances of Field cannot be set. """
    raise TypeError(e)

  def __delete__(self, *_) -> Never:
    """Must be implemented in subclass"""
    e = """Instances of Field cannot be deleted. """
    raise TypeError(e)
