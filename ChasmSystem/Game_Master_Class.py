from .Entity_Class import Entity, BattleEntity
from . import Global_Config as gl

class GameMaster():
    def __init__(self) -> None:
        """The mediator between entities within a conflict
        
        Current properties (and build patterns) include:
        - active_entities
        
        Current methods include:
        - start_engagement(self) - Method for initializing entities for conflict
        """

        self.active_entities: dict[str, BattleEntity] = {}

    def add_entities(self, *args: Entity):
        "Builder pattern for active_entities"
        
        for arg in args:
            gl.check_for_type(arg, Entity)  # Error Handling
            
            b_entity = BattleEntity.from_entity(arg)
            self.active_entities[arg.id_name] = b_entity
        
        return self
    
    def start_engagement(self) -> None:
        "Feature method that calls for the initialization of every entity"
        for ent in self.active_entities.values():
            BattleEntity.start_up(ent)

