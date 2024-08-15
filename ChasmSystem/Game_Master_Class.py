from Entity_Class import Entity, BattleEntity
import Global_Config as gl
    

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
        for ent in self.active_entities.values():
            BattleEntity.start_up(ent)


if __name__ == '__main__':
    from Weapon_Class import Weapon
    from Die_Class import Die

    d4 = Die().set_num_sides(4)

    dave = Entity() \
        .set_attribute('Vit', 350) \
        .set_attribute('Pat', 220) \
        .set_attribute('Arc', 130) \
        .set_attribute('Int', 330) \
        .set_name('dave')
    
    wand = Weapon() \
        .set_attr_use('Int', 'Pat') \
        .set_attr_req(100, 100) \
        .set_dmg_dice(d4, d4, d4)

    game = GameMaster().add_entities(dave)
    
    print(game.active_entities['dave'].hp, end=' ')
    game.start_engagement()
    print(game.active_entities['dave'].hp)

    print(BattleEntity.roll_damage(game.active_entities['dave'], wand))