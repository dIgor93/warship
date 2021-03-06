import uuid

from back.entities.entity import Entity
from back.physics import LinePhysics


class Bullet(Entity):
    def __init__(self, x: float, y: float, r: float, player_owner):
        __resource_name = f'bullet_{player_owner.ship_model.name}'
        super().__init__(x, y, r, __resource_name)
        self.id = f'bullet_{player_owner.ship_model.name}-{str(uuid.uuid1())[:8]}'
        self.owner = player_owner
        self.damage = self.owner.ship_model.bullet_damage
        self.physics = LinePhysics(x, y, r)
        self.physics.load_points(__resource_name)
        self.physics.set_move_speed(player_owner.ship_model.bullet_speed)

    def action_on_collision(self, entity):
        import back.entities as ee
        if isinstance(entity, ee.SpaceShip):
            entity.hp -= self.damage
            if entity.hp > 0:
                self.owner.score += 10
            else:
                self.owner.score += 50
            self.hp = 0
        elif isinstance(entity, ee.Statics):
            self.hp = 0
        elif isinstance(entity, Bullet):
            self.hp = 0
            entity.hp = 0
        elif isinstance(entity, ee.Bonus):
            entity.hp -= self.damage
            self.hp = 0
        else:
            print(f'Bullet. Not described case for type {type(entity)}')
