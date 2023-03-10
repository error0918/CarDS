from config import Cars
from data.data import Data
from data.result import Result
from internal import module
from internal import util
from jajucha.planning import BasePlanning
from jajucha.graphics import Graphics
import sys
import config

"""
CarDS - main.py
Copyright 2023. jtaeyeon05 all rights reserved 
"""


# Model
class Planning(BasePlanning):

    def __init__(self, graphics_):
        super().__init__(graphics_)

    def process(
            self,
            second,  # 경과 시간
            front_image,  # 전면 이미지
            rear_image,  # 후면 이미지 (없음)
            front_lidar,  # 전면 라이다 센서
            rear_lidar  # 후면 라이다 센서 (없음)
    ):
        if config.is_canny_show:
            self.imshow('canny', self.canny(front_image))

        v, l, r = self.gridFront(front_image, cols=7, rows=3)

        difference_data = config.difference[Cars.B422]
        data: Data = Data(
            second=second,
            front_lidar=front_lidar,
            v=v, l=l, r=r
        )

        # 배열에서 인덱스가 높을 수록 우선순위 ↑
        result: Result = module.operation(
            result_list=[
                module.default(data=data, difference_data=difference_data),
                module.four_lane(data=data, direction=module.Direction.Straight),
                module.left_three_lane(data=data, direction=module.Direction.Straight),
                module.right_three_lane(data=data, direction=module.Direction.Straight),
                module.t_three_lane(data=data, direction=module.Direction.Left),
                module.exit_left_dot_line(data=data, difference_data=difference_data),
                module.exit_right_dot_line(data=data, difference_data=difference_data),
                module.lidar_scan(data=data, direction=module.Direction.Left, scan_distance=350),
                module.back_car(data=data),
                module.hold_result(),
                module.manual_drive()
            ]
        )

        module.non_op.esc_to_pause()
        module.non_op.control_base_velocity()

        sys.stdout.write("\n\n")
        sys.stdout.write(
            "CarDS\n" +
            "situation = %s \n" % util.not_none(result.situation, "None") +
            "front_lidar = %d\n" % front_lidar +
            "steer = %d last_steer = %d\n"
            % (util.not_none(result.steer, -1), util.not_none(module.non_op.get_last_result().steer, -1)) +
            "velocity = %d\n"
            % util.not_none(result.velocity, -1) +
            "l[0] = %d l[1] = %d l[2] = %d | r[0] = %d r[1] = %d r[2] = %d\n"
            % (l[0], l[1], l[2], r[0], r[1], r[2]) +
            "v[0] = %d v[1] = %d v[2] = %d v[3] = %d v[4] = %d v[5] = %d v[5] = %d\n"
            % (v[0], v[1], v[2], v[3], v[4], v[5], v[6])
        )

        module.non_op.save_result(result=result)

        return difference_data.steer + util.not_none(result.steer, difference_data.steer), \
            module.non_op.control_current_velocity(util.not_none(result.velocity, config.base_velocity))


# Run
util.run_message("main")
graphics = Graphics(Planning)
graphics.root.mainloop()
graphics.exit()
