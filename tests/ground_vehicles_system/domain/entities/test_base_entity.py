from ground_vehicles_system.domain.entities.base_entity import Entity


class DumbEntity(Entity[int]):
    """
    A simple implementation of the Entity class for testing purposes.
    This class is used to test the base entity functionality without additional complexity.
    """
    def __init__(self, entity_id: int):
        self._id = entity_id

class TestEntity:
    def test_entity_equality_with_same_id(self):
        entity1 = DumbEntity(1)
        entity2 = DumbEntity(1)

        assert entity1 == entity2

    def test_entity_inequality_with_different_id(self):
        entity1 = DumbEntity(1)
        entity2 = DumbEntity(2)

        assert entity1 != entity2

    def test_entity_hash_with_same_id(self):
        entity1 = DumbEntity(1)
        entity2 = DumbEntity(1)

        assert hash(entity1) == hash(entity2)

    def test_entity_hash_with_different_id(self):
        entity1 = DumbEntity(1)
        entity2 = DumbEntity(2)

        assert hash(entity1) != hash(entity2)

    def test_id_property(self):
        entity = DumbEntity(1)

        assert entity.id == 1
