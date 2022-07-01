import time

def get_direction(ball_vector: list) -> int:
    """Get direction to navigate robot to face the ball
    Args:
        ball_vector (list of floats): Current vector of the ball with respect
            to the robot.
    Returns:
        int: 0 = forward, -1 = right, 1 = left
    """
    if -0.13 <= ball_vector[1] <= 0.13:
        return 0
    return -1 if ball_vector[1] < 0 else 1


class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd 
        # intialize
        self.t_prev = time.time()
        self.e_prev = 0
        self.I = 0
        self.D = 0
        self.P = 0

    def give_output(self, e_now):
        t_now = time.time()
        self.P = self.kp * e_now
        self.I = self.I + self.ki * e_now * (t_now - self.t_prev)
        self.D = self.kd * (e_now - self.e_prev) / (t_now - self.t_prev)
        
        self.t_prev = t_now
        self.e_prev = e_now

        return self.P + self.D + self.I