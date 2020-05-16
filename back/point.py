from json import JSONEncoder


class PointEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Point):
            return obj.x, obj.y
        else:
            return JSONEncoder.default(self, obj)


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Movement:
    def __init__(self, curr_value=0.0, delta=0.0, max_value=0.0):
        self.curr = curr_value
        self.max = max_value
        self.delta = delta
        self.moving = 0

    def set_next(self, time: float):
        if self.moving == 0:
            if self.curr > 0:
                if self.curr > self.delta:
                    self.curr -= self.delta
                else:
                    self.curr = 0
            elif self.curr < 0:
                if abs(self.curr) > self.delta:
                    self.curr += self.delta
                else:
                    self.curr = 0
        elif self.moving == 1:
            new_curr = self.curr + self.moving * self.delta
            self.curr = self.max if new_curr >= self.max else new_curr
        elif self.moving == -1:
            new_curr = self.curr + self.moving * self.delta
            self.curr = -self.max if new_curr <= -self.max else new_curr
        self.curr *= time

    @property
    def current(self):
        return self.curr


class AngleMovement(Movement):
    def __init__(self, curr_value=0, delta=0, max_value=0, angle_curr=0):
        super().__init__(curr_value=curr_value,
                         delta=delta,
                         max_value=max_value)
        self.angle_curr = angle_curr

    def set_next(self, time: float):
        if self.moving == 0:
            if abs(self.curr) < self.delta:
                self.curr = 0
            else:
                if self.curr > 0:
                    self.curr -= self.delta
                elif self.curr < 0:
                    self.curr += self.delta
        elif self.moving == 1:
            new_curr = self.curr + self.moving * self.delta
            self.curr = self.max if new_curr >= self.max else new_curr
        elif self.moving == -1:
            new_curr = self.curr + self.moving * self.delta
            self.curr = -self.max if new_curr <= -self.max else new_curr
        self.curr *= time
        self.angle_curr += self.curr

    @property
    def angle_current(self):
        return self.angle_curr
