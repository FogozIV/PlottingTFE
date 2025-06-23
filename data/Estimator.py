class Estimator:
    def __init__(self, bandwidth):
        self.ki = None
        self.kp = None
        self.bandwidth = None
        self.set_bandwidth(bandwidth)
        self.distance_estimation = 0.0
        self.speed = 0.0
        self.real_distance = 0.0

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self.kp = 2.0 * bandwidth
        self.ki = 0.25 * pow(self.kp, 2)

    def update(self, dt, distance):
        self.distance_estimation += self.speed * dt
        self.real_distance += distance
        delta_pos = self.real_distance - self.distance_estimation
        self.distance_estimation += dt * self.kp * delta_pos
        self.speed = dt * self.ki * delta_pos

