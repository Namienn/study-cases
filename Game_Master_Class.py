from Entity_Class import Entity
import Global_Config as gl
    

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
