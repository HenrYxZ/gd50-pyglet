class SingleTimer:
    elapsed = 0
    ended = False
    finish_callback = None

    def __init__(self, duration, tasks):
        self.duration = duration
        self.tasks = {}
        for target, definitions in tasks.items():
            self.tasks[target] = []
            for key, end_value in definitions.items():
                initial_value = getattr(target, key)
                change = end_value - initial_value
                self.tasks[target].append({
                    'key': key,
                    'initial': initial_value,
                    'change': change,
                    'end': end_value
                })

    def update(self, dt):
        if self.ended:
            return
        self.elapsed += dt
        if self.elapsed < self.duration:
            t = self.elapsed / self.duration
            for target, definitions in self.tasks.items():
                for task in definitions:
                    key = task['key']
                    change = task['change']
                    initial = task['initial']
                    current_value = initial + t * change
                    setattr(target, key, current_value)
        else:
            self.ended = True
            if self.finish_callback:
                self.finish_callback()

    def finish(self, callback):
        self.finish_callback = callback


class Timer:
    items = []

    def tween(self, duration, tasks):
        new_timer = SingleTimer(duration, tasks)
        self.items.append(new_timer)
        return new_timer

    def update(self, dt):
        for item in self.items:
            item.update(dt)
        for to_delete in [item for item in self.items if item.ended]:
            self.items.remove(to_delete)
