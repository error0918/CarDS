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
    last_steer = 0

    def __init__(self, graphics_):
        super().__init__(graphics_)

    def process(
            self,
            second,  # 경과 시간 (안 씀)
            front_image,  # 전면 이미지 (안 씀)
            rear_image,  # 후면 이미지 (없음)
            front_lidar,  # 전면 라이다 센서
            rear_lidar  # 후면 라이다 센서 (없음)
    ):
        self.imshow('canny', self.canny(front_image))  # canny 창 (차선 인식 상황)
        v, l, r = self.gridFront(front_image, cols=7, rows=3)
        # situation: 도로 상황
        # steer: 조향
        # velocity: 속력
        # v: 세로선, 0 ~ 6 (상단: 255, 하단: 0)
        # l: 가로선이 왼쪽에서 만나는 좌표, 0 ~ 2
        # r: 가로선이 오른쪽에서 만나는 좌표, 0 ~ 2
        # l, r은 중앙이 0, 위로부터 l[0]/r[0], l[1]/r[1], l[2]/r[2]

        difference_data = module.difference[module.B422]
        data: config.data_type = (
            front_lidar, self.last_steer, v, l, r
        )

        # 배열에서 인덱스가 높을 수록 우선순위 ↑
        result = module.operation(
            result_list=[
                module.default(data=data, difference_data=difference_data),
                # module.four_lane(data=data, direction=module.Direction.Straight),
                module.left_three_lane(data=data, direction=module.Direction.Straight),
                module.right_three_lane(data=data, direction=module.Direction.Straight),
                module.lidar_scan(data=data, direction=module.Direction.Left, scan_distance=400),
                module.manual_drive()
            ]
        )
        module.esc_to_halt()

        result_list = list(result)
        self.last_steer = result_list[2]

        sys.stdout.write(
            "CarDS\n" +
            "situation = %s\n\n" % ("None" if result_list[0] is None else result_list[0]) +
            "front_lidar = %d\n" % front_lidar +
            "steer = %d last_steer = %d\n"
            % (-1 if result_list[1] is None else result_list[1],
               -1 if self.last_steer is None else self.last_steer) +
            "velocity = %s\n"
            % ("-1" if result_list[2] is None else str(result_list[2])) +
            "l[0] = %d l[1] = %d l[2] = %d | r[0] = %d r[1] = %d r[2] = %d\n"
            % (l[0], l[1], l[2], r[0], r[1], r[2]) +
            "v[0] = %d v[1] = %d v[2] = %d v[3] = %d v[4] = %d v[5] = %d\n"
            % (v[0], v[1], v[2], v[3], v[4], v[5]) +
            "\n\n"
        )

        return difference_data["steer"] + self.last_steer if result[1] is None else result[1], \
            module.base_velocity if result[2] is None else result[2]


# Run
util.run_message("main")
graphics = Graphics(Planning)
graphics.root.mainloop()
graphics.exit()
