class SingleTimer:
    elapsed = 0
    ended = False

    def __init__(self, duration, target, definition):
        self.duration = duration
        self.target = target
        self.definition = definition

    def update(self, dt):
        self.elapsed += dt
        if self.elapsed < self.duration:
            for key, end_value in self.definition.items():
                t = self.elapsed / self.duration
                current_value = t * end_value
                setattr(self.target, key, current_value)
        else:
            self.ended = True


class Timer:
    items = []

    def tween(self, duration, target, definition):
        new_timer = SingleTimer(duration, target, definition)
        self.items.append(new_timer)

    def update(self, dt):
        for item in self.items:
            item.update(dt)
        # for to_delete in [item for item in self.items if item.ended]:
        #     self.items.remove(to_delete)
