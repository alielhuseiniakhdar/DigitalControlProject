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

                y_desired = 0.4
                x_desired = 0.4

                error_x = x_desired - robot_pos[0]
                error_y = y_desired - robot_pos[1]
                error_turn = 3.14 / 2 - heading
                print(robot_pos)
                if math.fabs(error_x) < 0.1:
                    reached_x = True 
                if math.fabs(error_y) < 0.1:
                    reached_y = True
                if math.fabs(error_turn) < 0.1:
                    turned = True
                print(reached_y)
                print(error_y)
                if not reached_y:
                    k =10
                    self.left_motor.setVelocity(-k*error_y)
                    self.right_motor.setVelocity(-k*error_y)
                else: 
                    if not turned:
                        k =10
                        self.left_motor.setVelocity(k*error_turn)
                        # self.right_motor.setVelocity(k)
                    else:
                        if not reached_x:
                            k = 10
                            self.left_motor.setVelocity(k*error_x)
                            self.right_motor.setVelocity(k*error_x)
                error_y = 0.4 - robot_pos[1]
                error_x = 0.4 - robot_pos[0]
                error_angle = 3.14 / 2 - heading

                if math.fabs(error_y) < 0.05:
                    reached_y = True
                
                if math.fabs(error_x) < 0.05:
                    reached_x = True

                if math.fabs(error_angle) < 0.001:
                    turned = True

                if not reached_y:
                    k = 20
                    velocity = k * error_y
                    self.set_both_velocity(-velocity)
                elif not turned:
                    k = 20
                    velocity = k * error_angle
                    if velocity > 10:
                        self.left_motor.setVelocity(10)
                    else:
                        self.left_motor.setVelocity(velocity)
                elif not reached_x:
                    k = 20
                    velocity = k * error_x
                    self.set_both_velocity(velocity)

    def set_both_velocity(self, velocity):
        self.left_motor.setVelocity(velocity)
        self.right_motor.setVelocity(velocity)



                




                


