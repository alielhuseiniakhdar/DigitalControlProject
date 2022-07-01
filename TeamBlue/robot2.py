# rcj_soccer_player controller - ROBOT Y2

# Feel free to import built-in libraries
import math  # noqa: F401

# You can also import scripts that you put into the folder with controller
import utils
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP


class MyRobot2(RCJSoccerRobot):
    def run(self):
        self.pid_controller = utils.PIDController(30, 0, 0)
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

                # Compute the speed for motors
                direction = utils.get_direction(ball_data["direction"])

                ball_signal_strength = ball_data['strength']
                

                if ball_signal_strength > 20 and robot_pos[1] < -0.2:
                    if direction == 0:
                        left_speed = 10
                        right_speed = 10
                    else:
                        left_speed = direction * 7
                        right_speed = direction * -7

                    # Set the speed to motors
                    self.left_motor.setVelocity(left_speed)
                    self.right_motor.setVelocity(right_speed)
                else:    
                    in_position = self.go_in_position(0, -0.74, robot_pos, heading)
                    if in_position:
                        # rotate to ball
                        left_speed = direction * 4
                        right_speed = direction * -4
                        self.left_motor.setVelocity(left_speed)
                        self.right_motor.setVelocity(right_speed)   

                # Send message to team robots
                self.send_data_to_team(self.player_id)

    def go_in_position(self, x, y, robot_pos, heading):
        error_x = x - robot_pos[0]
        error_y = y - robot_pos[1]

        if math.fabs(error_x) > 0.1:
            if error_x > 0:
                desired_heading = -math.pi / 2
            else:
                desired_heading = math.pi / 2

            heading_error = desired_heading - heading
            if math.fabs(heading_error) > 0.01:
                velocity = self.pid_controller.give_output(heading_error)
                velocity = velocity if velocity <= 10 else 10
                velocity = velocity if velocity >= -10 else -10
                self.left_motor.setVelocity(velocity)
                self.right_motor.setVelocity(-velocity)
            else:
                self.left_motor.setVelocity(10)
                self.right_motor.setVelocity(10)

            return False

        elif math.fabs(error_y) > 0.1:
            if error_y > 0:
                desired_heading = 0
            else:
                desired_heading = math.pi

            heading_error = desired_heading - heading
            if math.fabs(heading_error) > 0.01:
                velocity = self.pid_controller.give_output(heading_error)
                velocity = velocity if velocity <= 10 else 10
                velocity = velocity if velocity >= -10 else -10
                self.left_motor.setVelocity(velocity)
                self.right_motor.setVelocity(-velocity)
            else:
                self.left_motor.setVelocity(10)
                self.right_motor.setVelocity(10)

            return False

        else:
            return True