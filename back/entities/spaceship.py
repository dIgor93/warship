import back.entities as ee
from back.entities.bonus import Bonus, Egg
from back.entity_manager import EntityManager
from back.ships import Ship


class GunState:
    def __init__(self, speed):
        self.is_shooting = False
        self.shot_counter = 0
        self.shot_speed = speed


class BonusSystem:
    def __init__(self):
        self._bonuses = []

    def update(self, delta_time):
        for bonus in self._bonuses[::]:
            bonus.update(delta_time)
            if bonus.expired:
                self._bonuses.remove(bonus)

    def register(self, egg_object: Egg):
        for b in self._bonuses:
            if (b.get_target() == egg_object.get_target()) and (type(b) == type(egg_object)):
                b.reset_timer()
                return
        self._bonuses.append(egg_object)

    def get_info(self):
        return {'bonuses': [x.get_info() for x in self._bonuses]}


class SpaceShip(ee.Entity):
    def __init__(self,
                 x: float,
                 y: float,
                 r: float,
                 uid: str,
                 ship_model: Ship,
                 prepared_name):
        super().__init__(x, y, r, ship_model.name)
        self.id = uid
        self.name = prepared_name
        self.ship_model = ship_model
        self.physics.load_points(ship_model.name)
        self.physics.vector_motion.set_delta(ship_model.acceleration)
        self.physics.vector_motion.set_max_current(ship_model.speed)
        self.physics.angle_motion.set_delta(ship_model.mobility)

        self.physics.eval_approximately_aabb()
        self.gun_state = GunState(ship_model.shot_speed)
        self.hp = ship_model.hp
        self.hp_max = ship_model.hp_max
        self.score = 0
        self.__bonus_system = BonusSystem()

    def set_shooting(self, flag):
        if flag:
            self.gun_state.is_shooting = True
        else:
            self.gun_state.is_shooting = False

    def shooting(self, time_delta):
        if self.gun_state.is_shooting:
            if self.gun_state.shot_counter <= 0:
                self.gun_state.shot_counter = 1 / self.gun_state.shot_speed
                EntityManager().create_bullet(self.x, self.y, self.r, self)
            else:
                self.gun_state.shot_counter -= time_delta

    def action_on_collision(self, entity):
        if isinstance(entity, SpaceShip) or isinstance(entity, ee.Statics):
            self.physics.rollback()
        if isinstance(entity, Bonus):
            pass

    def next(self, t: float):
        super(SpaceShip, self).next(t)
        self.shooting(t)
        self.__bonus_system.update(t)

    def get_info(self):
        data = super(SpaceShip, self).get_info()
        additional_info = {'hp': self.hp,
                           'hp_max': self.hp_max,
                           'name': self.name,
                           'score': self.score
                           }
        data.update(additional_info)
        data.update(self.__bonus_system.get_info())
        return data

    def on_dead(self):
        EntityManager().create_bonus(self.x, self.y)

    def reg_bonus(self, egg_obj):
        egg_obj.set_target(self)
        self.__bonus_system.register(egg_obj)
