from Entity_Class import Entity
import Global_Elements as gl
    

class Game_Master():
    def __init__(self) -> None:
        """The mediator between entities within a conflict
        
        Current properties (and build patterns) include:
        - active_entities
        
        Current methods include:
        - clash_stats: settles a conflict between two attributes of two entities
        """
        self.active_entities = {}

    def add_entities(self, ent_list: tuple):
        "Builder pattern for active_entities"
        for entity in ent_list:
            if type(entity) is not Entity:  # Error Handling
                raise TypeError('Entity list contains non-entity elements')
            
            battle_stats = entity.battle_stats()
            self.active_entities[battle_stats[0]] = [battle_stats[1]]
        
        return self
    
    def delta_HP(self, entity, value):
        "Facade for altering HP value. Adds given value to an active entity"

        if entity not in self.active_entities.keys():  # Error Handling
            raise TypeError('Given object doesn\'t allign with active entities')

        self.active_entities[entity][0] += value


    @classmethod
    def clash_stats(cls, entity_1: Entity, stat_1:str, entity_2:Entity, stat_2:str):
        "Stat conflict settler. calls for stat rolls, returning the index of the winner and the roll result."
        if type(entity_1) is not Entity or type(entity_2) is not Entity:  # Error Handling
            raise TypeError('Non-entity element passed as entity')

        roll_1 = Entity.roll_stat(entity_1, stat_1)
        roll_2 = Entity.roll_stat(entity_2, stat_2)

        if roll_1 > roll_2:
            return (0, roll_1)
        return (1, roll_2)


if __name__ == "__main__":
    from Die_Class import Die
    from Weapon_Class import Weapon

    dave = Entity().set_attribute('Vit', 3156)
    joe = Entity().set_attribute('Str', 2865)

    game = Game_Master().add_entities([dave, joe])

    print(game.clash_stats(dave, 'Vit', joe, 'Str'))
    game.delta_HP(dave, -50)
    print(game.active_entities[dave])

    stick = Weapon().set_dmg_dice(Die().set_num_sides(20), Die().set_num_sides(20), Die().set_num_sides(20))
    stick.set_use_attr('Str').set_attr_req(3000)
    print(Entity.roll_damage(joe, stick))
