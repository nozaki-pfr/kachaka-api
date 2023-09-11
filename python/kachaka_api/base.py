# This file generated by tools/update_kachaka_api_base.py
# Don't edit directly

#  Copyright 2023 Preferred Robotics, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from functools import wraps

import grpc
from google._upb._message import RepeatedCompositeContainer

from .generated import kachaka_api_pb2 as pb2
from .generated.kachaka_api_pb2_grpc import KachakaApiStub
from .util.layout import ShelfLocationResolver


def kachaka_command(func):
    @wraps(func)
    def start_command(
        self: KachakaApiClientBase,
        *args,
        cancel_all=True,
        tts_on_success="",
        title="",
        wait_for_completion=True,
        **kwargs,
    ) -> pb2.Result:
        request = pb2.StartCommandRequest(
            command=func(self, *args, **kwargs),
            cancel_all=cancel_all,
            tts_on_success=tts_on_success,
            title=title,
        )
        response: pb2.StartCommandResponse = self.stub.StartCommand(request)
        if not wait_for_completion:
            return response.result
        metadata = pb2.Metadata(cursor=0)
        while True:
            history_list_response: pb2.GetHistoryListResponse = (
                self.stub.GetHistoryList(pb2.GetRequest(metadata=metadata))
            )
            for history in history_list_response.histories:
                if history.id == response.command_id:
                    return pb2.Result(
                        success=history.success,
                        error_code=history.error_code,
                    )
            metadata.cursor = history_list_response.metadata.cursor

    return start_command


class KachakaApiClientBase:
    def __init__(self, target: str = "100.94.1.1:26400"):
        self.stub = KachakaApiStub(grpc.insecure_channel(target))
        self.resolver = ShelfLocationResolver()

    def get_robot_serial_number(self) -> str:
        request = pb2.GetRequest()
        response: pb2.GetRobotSerialNumberResponse = (
            self.stub.GetRobotSerialNumber(request)
        )
        return response.serial_number

    def get_robot_version(self) -> str:
        request = pb2.GetRequest()
        response: pb2.GetRobotVersionResponse = self.stub.GetRobotVersion(
            request
        )
        return response.version

    def get_robot_pose(self) -> pb2.Pose:
        request = pb2.GetRequest()
        response: pb2.GetRobotPoseResponse = self.stub.GetRobotPose(request)
        return response.pose

    def get_png_map(self) -> pb2.Map:
        request = pb2.GetRequest()
        response: pb2.GetPngMapResponse = self.stub.GetPngMap(request)
        return response.map

    def get_object_detection(
        self,
    ) -> tuple[pb2.RosHeader, RepeatedCompositeContainer]:
        request = pb2.GetRequest()
        response: pb2.GetObjectDetectionResponse = self.stub.GetObjectDetection(
            request
        )
        return (response.header, response.objects)

    def get_ros_imu(self) -> pb2.RosImu:
        request = pb2.GetRequest()
        response: pb2.GetRosImuResponse = self.stub.GetRosImu(request)
        return response.imu

    def get_ros_odometry(self) -> pb2.RosOdometry:
        request = pb2.GetRequest()
        response: pb2.GetRosOdometryResponse = self.stub.GetRosOdometry(request)
        return response.odometry

    def get_ros_laser_scan(self) -> pb2.RosLaserScan:
        request = pb2.GetRequest()
        response: pb2.GetRosLaserScanResponse = self.stub.GetRosLaserScan(
            request
        )
        return response.scan

    def get_front_camera_ros_camera_info(self) -> pb2.RosCameraInfo:
        request = pb2.GetRequest()
        response: pb2.GetFrontCameraRosCameraInfoResponse = (
            self.stub.GetFrontCameraRosCameraInfo(request)
        )
        return response.camera_info

    def get_front_camera_ros_image(self) -> pb2.RosImage:
        request = pb2.GetRequest()
        response: pb2.GetFrontCameraRosImageResponse = (
            self.stub.GetFrontCameraRosImage(request)
        )
        return response.image

    def get_front_camera_ros_compressed_image(
        self,
    ) -> pb2.RosCompressedImage:
        request = pb2.GetRequest()
        response: pb2.GetFrontCameraRosCompressedImageResponse = (
            self.stub.GetFrontCameraRosCompressedImage(request)
        )
        return response.image

    @kachaka_command
    def start_command(self, command: pb2.Command) -> pb2.Command:
        return command

    @kachaka_command
    def move_shelf(
        self, shelf_name_or_id: str, location_name_or_id: str
    ) -> pb2.Command:
        shelf_id = self.resolver.get_shelf_id_by_name(shelf_name_or_id)
        location_id = self.resolver.get_location_id_by_name(location_name_or_id)
        return pb2.Command(
            move_shelf_command=pb2.MoveShelfCommand(
                target_shelf_id=shelf_id,
                destination_location_id=location_id,
            )
        )

    @kachaka_command
    def return_shelf(self, shelf_name_or_id: str = "") -> pb2.Command:
        shelf_id = self.resolver.get_shelf_id_by_name(shelf_name_or_id)
        return pb2.Command(
            return_shelf_command=pb2.ReturnShelfCommand(
                target_shelf_id=shelf_id
            )
        )

    @kachaka_command
    def undock_shelf(self) -> pb2.Command:
        return pb2.Command(undock_shelf_command=pb2.UndockShelfCommand())

    @kachaka_command
    def move_to_location(self, location_name_or_id: str) -> pb2.Command:
        location_id = self.resolver.get_location_id_by_name(location_name_or_id)
        return pb2.Command(
            move_to_location_command=pb2.MoveToLocationCommand(
                target_location_id=location_id
            )
        )

    @kachaka_command
    def return_home(self) -> pb2.Command:
        return pb2.Command(return_home_command=pb2.ReturnHomeCommand())

    @kachaka_command
    def dock_shelf(self) -> pb2.Command:
        return pb2.Command(dock_shelf_command=pb2.DockShelfCommand())

    @kachaka_command
    def speak(self, text: str) -> pb2.Command:
        return pb2.Command(speak_command=pb2.SpeakCommand(text=text))

    @kachaka_command
    def move_to_pose(self, x: float, y: float, yaw: float) -> pb2.Command:
        return pb2.Command(
            move_to_pose_command=pb2.MoveToPoseCommand(x=x, y=y, yaw=yaw)
        )

    def cancel_command(self) -> tuple[pb2.Result, pb2.Command]:
        request = pb2.EmptyRequest()
        response: pb2.CancelCommandResponse = self.stub.CancelCommand(request)
        return (response.result, response.command)

    def get_command_state(self) -> tuple[pb2.CommandState, pb2.Command]:
        request = pb2.GetRequest()
        response: pb2.GetCommandStateResponse = self.stub.GetCommandState(
            request
        )
        return (response.state, response.command)

    def is_command_running(self) -> bool:
        request = pb2.GetRequest()
        response: pb2.GetCommandStateResponse = self.stub.GetCommandState(
            request
        )
        return response.state == pb2.CommandState.COMMAND_STATE_RUNNING

    def get_running_command(self) -> pb2.Command | None:
        request = pb2.GetRequest()
        response: pb2.GetCommandStateResponse = self.stub.GetCommandState(
            request
        )
        return response.command if response.HasField("command") else None

    def get_last_command_result(self) -> tuple[pb2.Result, pb2.Command]:
        request = pb2.GetRequest()
        response: pb2.GetLastCommandResultResponse = (
            self.stub.GetLastCommandResult(request)
        )
        return (response.result, response.command)

    def get_locations(
        self,
    ) -> RepeatedCompositeContainer:
        request = pb2.GetRequest()
        response: pb2.GetLocationsResponse = self.stub.GetLocations(request)
        return response.locations

    def get_default_location_id(self) -> str:
        request = pb2.GetRequest()
        response: pb2.GetLocationsResponse = self.stub.GetLocations(request)
        return response.default_location_id

    def get_shelves(
        self,
    ) -> RepeatedCompositeContainer:
        request = pb2.GetRequest()
        response: pb2.GetShelvesResponse = self.stub.GetShelves(request)
        return response.shelves

    def set_auto_homing_enabled(self, enable: bool) -> pb2.Result:
        request = pb2.SetAutoHomingEnabledRequest(enable=enable)
        response: pb2.SetAutoHomingEnabledResponse = (
            self.stub.SetAutoHomingEnabled(request)
        )
        return response.result

    def get_auto_homing_enabled(self) -> bool:
        request = pb2.GetRequest()
        response: pb2.GetAutoHomingEnabledResponse = (
            self.stub.GetAutoHomingEnabled(request)
        )
        return response.enabled

    def set_manual_control_enabled(self, enable: bool) -> pb2.Result:
        request = pb2.SetManualControlEnabledRequest(enable=enable)
        response: pb2.SetManualControlEnabledResponse = (
            self.stub.SetManualControlEnabled(request)
        )
        return response.result

    def get_manual_control_enabled(self) -> bool:
        request = pb2.GetRequest()
        response: pb2.GetManualControlEnabledResponse = (
            self.stub.GetManualControlEnabled(request)
        )
        return response.enabled

    def set_robot_velocity(self, linear: float, angular: float) -> pb2.Result:
        request = pb2.SetRobotVelocityRequest(linear=linear, angular=angular)
        response: pb2.SetRobotVelocityResponse = self.stub.SetRobotVelocity(
            request
        )
        return response.result

    def get_history_list(
        self,
    ) -> RepeatedCompositeContainer:
        request = pb2.GetRequest()
        response: pb2.GetHistoryListResponse = self.stub.GetHistoryList(request)
        return response.histories

    def update_resolver(self) -> None:
        self.resolver.set_shelves(self.get_shelves())
        self.resolver.set_locations(self.get_locations())
