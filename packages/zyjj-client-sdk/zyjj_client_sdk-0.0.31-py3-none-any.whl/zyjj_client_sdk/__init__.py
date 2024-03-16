import json
import logging

from zyjj_client_sdk.api import Api, TaskStatus
from zyjj_client_sdk.base import Base
from zyjj_client_sdk.storage import Storage
from zyjj_client_sdk.entity import EntityHelper, EntityAudio, EntitySubtitles
from zyjj_client_sdk.ffmpeg_sdk import FFMpegService
from zyjj_client_sdk.client import MqttServer, MqttEventType
from typing import Callable
from tencentcloud.common import credential


# 给回调函数使用的api
class HandleApi:
    def __init__(
            self,
            _base: Base,
            _api: Api,
            uid: str,
            task_id: str,
            _input: dict,
            mqtt: MqttServer,
            global_data: dict
    ):
        self.__base = _base
        self.__api = _api
        self.__ffmpeg = FFMpegService()
        self.__storage = Storage(_base, _api)
        self.__entity = EntityHelper(_base)
        self.__mqtt = mqtt
        self.__global_data = global_data

        self.__uid = uid
        self.__task_id = task_id
        self.__input = _input
        self.__output = {}

    # 更新任务进度
    def progress_update(self, progress: float):
        self.__mqtt.send_task_event(self.__uid, self.__task_id, MqttEventType.Progress, progress)

    # 下载输入的文件并返回耗时信息
    def input_download_with_duration_by_unique(self, unique: str) -> (str, float):
        audio_path = self.__storage.download_file(self.input_get_path_by_unique(unique))
        return audio_path, self.__ffmpeg.get_duration(audio_path) * 1000

    # 下载文件到临时目录
    def input_download_by_unique(self, unique: str) -> str:
        return self.__storage.download_file(self.input_get_path_by_unique(unique))

    # 直接获取文件的url
    def input_get_url_by_unique(self, unique: str) -> str:
        return self.__storage.tencent_get_url_by_key(self.input_get_path_by_unique(unique))

    # 获取变量的path信息
    def input_get_path_by_unique(self, unique: str) -> str:
        return self.__input[unique]['path']

    # 获取文件的耗时信息(单位s)
    def input_get_duration_by_unique(self, unique: str) -> float:
        return self.__input[unique]["duration"]

    # 获取任务的原始输入
    def input_get_data(self) -> dict:
        return self.__input

    # 获取用户积分
    def point_get(self) -> int:
        return self.__api.get_user_point(self.__uid)

    # 检查用户积分
    def point_check(self, point: int):
        if self.__api.get_user_point(self.__uid) < point:
            raise Exception("积分不足请充值")

    # 扣除用户积分
    def point_use(self, name: str, cost: float, desc=''):
        if not self.__api.use_user_point(self.__uid, name, cost, desc):
            raise Exception("积分不足请充值")

    # 上传字幕文件
    def output_file_with_subtitle(self, unique: str, subtitles: EntitySubtitles):
        subtitle_file = self.__entity.generate_subtitle_file(subtitles)
        self.__output[unique] = self.__storage.upload_file(subtitle_file.file_path, self.__uid, 1)

    #  直接上传文件
    def output_file_with_path(self, unique: str, path: str):
        self.__output[unique] = self.__storage.upload_file(path, self.__uid, 1)

    # 通过本地路径获取url
    def output_url_with_path(self, unique: str, path: str):
        key = self.__storage.tencent_get_key_by_path(path, self.__uid)
        self.__output[unique] = self.__storage.tencent_get_url_by_key(key)

    # 通过bytes获取url
    def output_url_with_bytes(self, unique: str, ext: str, data: bytes):
        self.__output[unique] = self.tencent_get_url_by_bytes(ext, data)

    # 设置输出
    def output_set(self, unique: str, value: any):
        self.__output[unique] = value

    # 获取任务的输出
    def output_get_data_str(self) -> str:
        return json.dumps(self.__output)

    # 获取任务的输出
    def output_get_data(self) -> dict:
        return self.__output

    # mqtt发送成功信息
    def success(self, data: dict):
        self.__mqtt.send_task_event(self.__uid, self.__task_id, MqttEventType.Success, data)

    #
    def tencent_get_key_by_local(self, path: str) -> str:
        return self.__storage.tencent_get_key_by_path(path, self.__uid)

    # 从本地上传文件并获取url
    def tencent_get_url_by_path(self, path: str) -> str:
        key = self.__storage.tencent_get_key_by_path(path, self.__uid)
        return self.__storage.tencent_get_url_by_key(key)

    # 直接cos key中提取url
    def tencent_get_url_by_key(self, key: str):
        return self.__storage.tencent_get_url_by_key(key)

    # 获取二进制的url链接
    def tencent_get_url_by_bytes(self, extend: str, data: bytes) -> str:
        # 上传二进制
        key = self.__storage.tencent_get_key_by_bytes(self.__uid, self.__base.generate_filename(extend), data)
        # 获取url
        return self.__storage.tencent_get_url_by_key(key)

    # 获取腾讯的认证信息
    def tencent_get_credential(self) -> credential.Credential:
        token = self.__api.could_get_tencent_token()
        return credential.Credential(token["TmpSecretId"], token["TmpSecretKey"])

    #  获取全局数据
    def global_get(self, key: str):
        return self.__global_data[key]

    # 获取配置字符串
    def config_get_str(self, key: str) -> str:
        return self.__api.get_config(key)

    # 获取配置文件
    def config_get(self, key: str) -> dict:
        return json.loads(self.config_get_str(key))

    # 随机生成一个文件名
    def tool_generate_file_path(self, ext: str) -> str:
        return self.__base.generate_local_file(ext)


class SdkService:
    def __init__(self):
        self.__base = Base()
        self.__api = Api(self.__base)
        self.__handle = {}
        self.__mqtt = MqttServer(self.__api)
        self.__global_data = {}

    # 添加处理器
    def add_handle(self, task_type: int, handle: Callable[[HandleApi, dict], None]) -> 'SdkService':
        self.__handle[task_type] = handle
        return self

    # 添加全局变量
    def add_global(self, key: str, value: any) -> 'SdkService':
        self.__global_data[key] = value
        return self

    # 启动服务
    def start(self) -> 'SdkService':
        # 后台启动mqtt
        self.__mqtt.start_backend()
        return self

    # 停止服务
    def stop(self) -> 'SdkService':
        self.__mqtt.close()
        return self

    # 开始处理任务
    def execute_task(self) -> dict:
        # 拉取任务
        task_info = self.__api.task_pull_task()
        if task_info is None:
            logging.info("[task] task not found")
            return {"msg": "task not found"}
        logging.info(f'[task] pull task is {task_info}')
        # 获取任务信息
        uid = task_info['uid']
        task_type = task_info['task_type']
        task_input = json.loads(task_info['input'])
        task_id = task_info['id']
        # 寻找处理器
        if task_type in self.__handle:
            self.__mqtt.send_task_event(uid, task_id, MqttEventType.Start, "")
            handle_api = HandleApi(
                self.__base,
                self.__api,
                uid,
                task_id,
                task_input,
                self.__mqtt,
                self.__global_data
            )
            try:
                # 执行任务
                self.__handle[task_type](handle_api, task_input)
                self.__api.task_update_task(
                    task_id,
                    status=TaskStatus.Success,
                    output=handle_api.output_get_data_str()
                )
                self.__mqtt.send_task_event(
                    uid,
                    task_id,
                    MqttEventType.Success,
                    handle_api.output_get_data()
                )
                return handle_api.output_get_data()
            except Exception as e:
                self.__api.task_update_task(task_id, status=TaskStatus.Fail, extra=str(e))
                self.__mqtt.send_task_event(uid, task_id, MqttEventType.Fail, str(e))
                return {"msg": str(e)}
        else:
            err_info = f"task type {task_type} not found"
            logging.error(err_info)
            self.__api.task_update_task(task_id, status=TaskStatus.Fail, extra=err_info)
            self.__mqtt.send_task_event(uid, task_id, MqttEventType.Fail, err_info)
            return {"msg": err_info}
