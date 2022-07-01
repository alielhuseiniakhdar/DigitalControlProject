# rcj_soccer_player controller - ROBOT B1

# Feel free to import built-in libraries
import math  # noqa: F401

# You can also import scripts that you put into the folder with controller
import utils
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP


class MyRobot1(RCJSoccerRobot):
    def run(self):

        reached_x = False
        reached_y = False
        turned = False

        while self.robot.step(TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()  # noqa: F841

                while self.is_new_team_data():
                    team_data = self.get_new_team_data()  # noqa: F841
                    # Do something with team data

                if self.is_new_ball_data():
                    ball_data = self.get_new_ball_data()
                else:
                    # If the robot does not see the ball, stop motors
                    self.left_motor.setVelocity(0)
                    self.right_motor.setVelocity(0)
                    continue

                # Get data from compass
                heading = self.get_compass_heading()  # noqa: F841

                # Get GPS coordinates of the robot
                robot_pos = self.get_gps_coordinates()  # noqa: F841

                # Get data from sonars
                sonar_values = self.get_sonar_values()  # noqa: F841
    
                max_ball_signal_strength = 275 
                error_angle_direction = 1 - ball_data['direction'][0]
                error_distance = max_ball_signal_strength - 40 - ball_data['strength'] 
                print(error_distance)

                if math.fabs(error_angle_direction) < 0.1:
                    in_ball_direction = True

                if not in_ball_direction:
                    k = 20
                    velocity = k * error_angle_direction
                    self.left_motor.setVelocity(velocity)
                    self.right_motor.setVelocity(0)
                else:
                    k = 0.1
                    velocity = k * error_distance
                    self.left_motor.setVelocity(velocity)
                    self.right_motor.setVelocity(velocity)
                    if math.fabs(error_angle_direction) > 0.1:
                        in_ball_direction = False



                




                


