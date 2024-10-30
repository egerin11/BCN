import random
import time


class ChannelSimulator:
    def __init__(self, collision_probability=0.3, busy_probability=0.5):
        self.collision_probability = collision_probability
        self.busy_probability = busy_probability

    def listen_channel(self):
        return random.random() < self.busy_probability

    def detect_collision(self):
        return random.random() < self.collision_probability

    @staticmethod
    def exponential_backoff_delay(attempt, base_delay=0.5, max_delay=1):
        delay_factor = min(2 ** attempt - 1, max_delay / base_delay)
        delay = random.uniform(base_delay, base_delay * delay_factor)
        time.sleep(delay)
