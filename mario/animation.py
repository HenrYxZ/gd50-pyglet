class Animation:
    def __init__(self, frames, interval):
        self.frames = frames
        self.interval = interval
        self.current_frame = 0
        self.timer = 0

    def update(self, dt):
        if len(self.frames) > 1:
            self.timer += dt

            if self.timer > self.interval:
                self.timer %= self.interval
                self.current_frame = (self.current_frame + 1) % len(self.frames)

    def get_current_frame(self):
        return self.frames[self.current_frame]
