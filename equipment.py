from dataclasses import dataclass
from typing import List
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    @property
    def damage(self):
        return uniform(self.max_damage, self.min_damage)


@dataclass
class EquipmentData:
    armors: List[Armor]
    weapons: List[Weapon]

    class Meta:
        unknown = marshmallow.EXCLUDE


class Equipment:

    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name) -> Weapon:
        return [i for i in self.equipment.weapons if weapon_name == i.name][0]

    def get_armor(self, armor_name) -> Armor:
        return [i for i in self.equipment.armors if armor_name == i.name][0]

    def get_weapons_names(self) -> list:
        return [i.name for i in self.equipment.weapons]

    def get_armors_names(self) -> list:
        return [i.name for i in self.equipment.armors]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        equipment_file = open("./data/equipment.json")
        data = json.load(equipment_file)
        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError
