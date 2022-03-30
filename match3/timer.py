class SingleTimer:
    elapsed = 0
    ended = False
    finish_callback = None

    def __init__(self, duration, target, definition):
        self.duration = duration
        self.target = target
        self.definition = definition
        self.initials = {}
        self.changes = {}
        for key, end_value in self.definition.items():
            initial_value = getattr(self.target, key)
            self.initials[key] = initial_value
            self.changes[key] = end_value - initial_value

    def update(self, dt):
        if self.ended:
            return
        self.elapsed += dt
        if self.elapsed < self.duration:
            for key, end_value in self.definition.items():
                t = self.elapsed / self.duration
                current_value = self.initials[key] + t * self.changes[key]
                setattr(self.target, key, current_value)
        else:
            self.ended = True
            if self.finish_callback:
                self.finish_callback()

    def finish(self, callback):
        self.finish_callback = callback


class Timer:
    items = []

    def tween(self, duration, target, definition):
        new_timer = SingleTimer(duration, target, definition)
        self.items.append(new_timer)
        return new_timer

    def update(self, dt):
        for item in self.items:
            item.update(dt)
        for to_delete in [item for item in self.items if item.ended]:
            self.items.remove(to_delete)
