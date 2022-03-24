class SingleTimer:
    elapsed = 0
    counter = 0

    def __init__(self, interval):
        self.interval = interval

    def update(self, dt):
        self.elapsed += dt
        if self.elapsed > self.interval:
            self.elapsed = self.elapsed % self.interval
            self.counter += 1


class Timer:
    items = []

    def schedule(self, interval):
        self.items.append(SingleTimer(interval))

    def update(self, dt):
        for item in self.items:
            item.update(dt)
