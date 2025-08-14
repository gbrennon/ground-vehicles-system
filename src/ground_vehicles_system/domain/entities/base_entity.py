from abc import ABC
from typing import Generic, TypeVar


IdType = TypeVar('IdType')

class Entity(ABC, Generic[IdType]):
    """
    Base class for all entities in the system.
    This class serves as a base for all domain entities, ensuring they can be identified and managed consistently.
    """
    _id: IdType

    def __eq__(self, other: object):
        return isinstance(other, Entity) and self._id == other._id

    def __hash__(self):
        return hash(self._id)

    @property
    def id(self) -> IdType:
        """
        Returns the unique identifier of the entity.
        This identifier is used to distinguish between different entities in the system.
        """
        return self._id
