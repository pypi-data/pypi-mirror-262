import json
import re
import time

from ..types.abc import BotEvent
from ..types.typing import *
from .cq import get_cq as _get_cq
from .cq import get_cq_params as _get_cq_params
from .cq import to_cq_arr, to_cq_str


class BotEventBuilder:
    @staticmethod
    def build(rawEvent: dict | str) -> BotEvent:
        if isinstance(rawEvent, str):
            rawEvent = json.loads(rawEvent)

        etype = rawEvent.get("post_type")
        if etype in ("message_sent", "message"):
            return MessageEvent(rawEvent)
        elif etype == "request":
            return RequestEvent(rawEvent)
        elif etype == "notice":
            return NoticeEvent(rawEvent)
        elif etype == "meta_event":
            return MetaEvent(rawEvent)
        else:
            return ResponseEvent(rawEvent)


class MessageEvent(BotEvent):
    def __init__(self, rawEvent: dict) -> None:
        super().__init__(rawEvent)
        self.bot_id = rawEvent.get("self_id")

        self.id: int
        self.sender: MessageEvent.Sender
        self.group_id: Optional[int]
        # 使用 CQ 字符串编码的消息
        self.raw_content: str
        # array 格式表示所有类型消息段
        self.content: List[CQMsgDict]
        # 消息中所有文本消息段的合并字符串
        self.text: str
        self.font: int
        self.temp_src: Optional[str]

        self._init()

    @property
    def time(self) -> int:
        return self.raw.get("time")

    @property
    def type(self) -> str:
        return "message"

    def _init(self) -> None:
        rawEvent = self.raw

        self._cq_regex = re.compile(r"\[CQ:.*?\]")
        self.id = rawEvent["message_id"]
        self.raw_content = self._format_to_str(rawEvent["raw_message"])
        self.content = self._format_to_array(rawEvent["message"])
        self.text = self._get_text(self.content)
        self.font = rawEvent["font"]

        self.temp_src = None
        temp_src = rawEvent.get("temp_source")
        if temp_src:
            self.temp_src = MessageEvent._TEMP_SRC_MAP[temp_src]

        self.sender = MessageEvent.Sender(
            rawEvent=rawEvent,
            isGroup=self.is_group(),
            isGroupAnonym=self.is_group_anonym(),
        )

        self.group_id = None
        if self.is_group():
            self.group_id = rawEvent["group_id"]

    def _format_to_str(self, content: list | str) -> str:
        """
        对外部零信任，强制转换为 cq 字符串格式
        """
        if not isinstance(content, str):
            return to_cq_str(content)
        else:
            return content

    def _format_to_array(self, content: list | str) -> List[CQMsgDict]:
        """
        对外部零信任，强制转换为消息段格式
        """
        if not isinstance(content, str):
            for item in content:
                if item["type"] == "text":
                    continue
                for k, v in item["data"].items():
                    if not isinstance(v, str):
                        continue
                    if v.isdigit() or (len(v) >= 2 and v[0] == "-" and v[1:].isdigit()):
                        item["data"][k] = int(v)
                        continue
                    try:
                        item["data"][k] = float(v)
                    except Exception:
                        pass
            return content
        else:
            return to_cq_arr(content)

    def _get_text(self, content: List[CQMsgDict]) -> str:
        """
        获取消息中所有文本消息，返回合并字符串
        """
        text_list = []
        for item in content:
            if item["type"] == "text":
                text_list.append(item["data"]["text"])
        return "".join(text_list)

    def get_cq(self, cq_type: str) -> List[CQMsgDict]:
        """
        从当前 event 中获取指定类型的 cq 消息 dict
        """
        return _get_cq(self.content, cq_type)

    def get_cq_params(
        self, cq_type: str, param: str, type: Type[T] = None
    ) -> List[Any]:
        """
        从当前 event 中获取指定类型 cq 消息的指定 param，以列表形式返回。
        当没有任何对应类型的 cq 消息时，为空列表。如果有对应类型 cq 消息，
        但是 param 不存在，则在列表中产生值 None

        可以指定 type 来强制转换类型，不填则使用智能解析出的类型
        """
        return _get_cq_params(self.content, cq_type, param, type)

    def is_private(self) -> bool:
        """是否为私聊消息（注意群临时会话属于该类别）"""
        return self.raw["message_type"] == "private"

    def is_friend(self) -> bool:
        """是否为好友消息"""
        return (
            self.raw["message_type"] == "private" and self.raw["sub_type"] == "friend"
        )

    def is_group(self) -> bool:
        """是否为群消息（正常群消息、群匿名消息、群自身消息、群系统消息属于该类型）"""
        return self.raw["message_type"] == "group"

    def is_group_normal(self) -> bool:
        """是否为正常群消息"""
        return self.raw["message_type"] == "group" and self.raw["sub_type"] == "normal"

    def is_group_anonym(self) -> bool:
        """是否为匿名群消息"""
        return (
            self.raw["message_type"] == "group" and self.raw["sub_type"] == "anonymous"
        )

    def is_group_self(self) -> bool:
        """是否为群自身消息（即 bot 自己群中发的消息）"""
        return (
            self.raw["message_type"] == "group" and self.raw["sub_type"] == "group_self"
        )

    def is_group_temp(self) -> bool:
        """是否为群临时会话（属于私聊的一种）"""
        return self.raw["message_type"] == "private" and self.raw["sub_type"] == "group"

    def is_temp(self) -> bool:
        """是否为临时会话（属于私聊的一种）"""
        return "temp_source" in self.raw.keys()

    def is_group_notice(self) -> bool:
        """是否为群系统消息，特别注意是消息！"""
        return self.raw["message_type"] == "group" and self.raw["sub_type"] == "notice"

    _TEMP_SRC_MAP = {
        0: "群聊",
        1: "QQ咨询",
        2: "查找",
        3: "QQ电影",
        4: "热聊",
        6: "验证消息",
        7: "多人聊天",
        8: "约会",
        9: "通讯录",
    }

    class Sender:
        """
        消息发送者信息类
        """

        def __init__(self, rawEvent: dict, isGroup: bool, isGroupAnonym: bool) -> None:
            self._rawEvent = rawEvent
            self._isGroup = isGroup
            self._isGroupAnonym = isGroupAnonym
            self.id: int
            self.nickname: str
            self.sex: str
            self.age: int

            self.group_card: str
            # 总共有四种：owner, admin, member, anonymous
            self.group_role: Literal["owner", "admin", "member", "anonymous"]
            self.group_title: str
            self.group_area: str
            self.group_level: str

            self.anonym_id: int
            self.anonym_name: str
            # 匿名用户 flag，调用 连接适配器 相关 API 时，需要使用
            self.anonym_flag: str

            # 对应私聊可能缺失 sender 的情况
            if len(rawEvent["sender"]) == 0:
                self._gen_empty()
                return

            self.id = rawEvent["sender"]["user_id"]
            self.nickname = rawEvent["sender"]["nickname"]
            self.sex = (
                rawEvent["sender"]["sex"] if "sex" in rawEvent["sender"].keys() else ""
            )
            self.age = (
                rawEvent["sender"]["age"] if "age" in rawEvent["sender"].keys() else ""
            )
            if isGroup:
                if isGroupAnonym:
                    self.group_card = ""
                    self.group_area = rawEvent["sender"]["area"]
                    self.group_level = rawEvent["sender"]["level"]
                    self.group_role = "anonymous"
                    self.group_title = ""
                    self.anonym_id = rawEvent["anonymous"]["id"]
                    self.anonym_name = rawEvent["anonymous"]["name"]
                    self.anonym_flag = rawEvent["anonymous"]["flag"]
                else:
                    self.group_card = rawEvent["sender"]["card"]
                    self.group_area = (
                        rawEvent["sender"]["area"]
                        if "area" in rawEvent["sender"].keys()
                        else ""
                    )
                    self.group_level = rawEvent["sender"]["level"]
                    self.group_role = rawEvent["sender"]["role"]
                    self.group_title = rawEvent["sender"]["title"]

        def _gen_empty(self) -> None:
            """当传入的 rawEvent 缺失 sender 时，把属性直接置空"""
            self.id = self._rawEvent["user_id"]
            self.nickname = None
            self.sex = None
            self.age = None

        def is_group_owner(self) -> bool:
            """判断是否为群主，若不是或不是群类型消息，返回 False"""
            if not self._isGroup:
                return False
            return self.group_role == "owner"

        def is_group_admin(self) -> bool:
            """判断是否为群管理（包含群主），若不是或不是群类型消息，返回 False"""
            if not self._isGroup:
                return False
            return self.group_role == "admin" or self.group_role == "owner"

        def only_group_member(self) -> bool:
            """判断是否只是群员（注意只是群员，不包括群主、管理和匿名），若不是或不是群类型消息，返回 False"""
            if not self._isGroup:
                return False
            return self.group_role == "member"

        def is_anonym_member(self) -> bool:
            """判断是否是群匿名，若不是或不是群类型消息，返回 False"""
            if not self._isGroup:
                return False
            return self.group_role == "anonymous"

        def is_bot(self) -> bool:
            """判断消息是否是bot自己发送的"""
            return self.id == self._rawEvent["self_id"]


class RequestEvent(BotEvent):
    def __init__(self, rawEvent: dict) -> None:
        super().__init__(rawEvent)
        self.bot_id = rawEvent.get("self_id")

        self.from_id: int
        self.from_group_id: Optional[int]
        # 此处为加群或加好友的验证消息
        self.req_comment: str
        # 请求 flag，调用相关 连接适配器 API 时，需要使用
        self.req_flag: str
        # 当为加群请求时，类型有：add, invite（加群请求和邀请 bot 入群）
        self.group_req_type: Optional[Literal["add", "invite"]]

        self._init()

    @property
    def time(self) -> int:
        return self.raw.get("time")

    @property
    def type(self) -> str:
        return "request"

    def _init(self) -> None:
        rawEvent = self.raw
        self.group_req_type = None
        self.from_group_id = None

        if self.is_friend_req():
            self.from_id = rawEvent["user_id"]
            self.req_comment = rawEvent["comment"]
            self.req_flag = rawEvent["flag"]
        elif self.is_group_req():
            self.group_req_type = rawEvent["sub_type"]
            self.from_id = rawEvent["user_id"]
            self.from_group_id = rawEvent["group_id"]
            self.req_comment = rawEvent["comment"]
            self.req_flag = rawEvent["flag"]

    def is_friend_req(self) -> bool:
        """是否为加好友请求"""
        return self.raw["request_type"] == "friend"

    def is_group_req(self) -> bool:
        """是否为加群请求"""
        return self.raw["request_type"] == "group"


class NoticeEvent(BotEvent):
    def __init__(self, rawEvent: dict) -> None:
        super().__init__(rawEvent)
        self.bot_id = rawEvent.get("self_id")
        # 修复某些 onebot 协议实现，user_id 缺失的问题
        if "target_id" in rawEvent.keys() and "user_id" not in rawEvent:
            rawEvent["user_id"] = rawEvent["target_id"]

        # 通知作用者或主体方的 id，如被禁言的一方
        self.notice_user_id: int
        # 通知若发生在群中，群 id
        self.notice_group_id: int
        # 通知发起者或操作方的 id，如禁言别人的管理员
        self.notice_operator_id: int
        # 通知涉及消息时，消息 id
        self.notice_msg_id: int
        # 若为入群通知，类型有：approve, invite（管理员同意和管理员邀请）
        self.join_group_type: str
        # 若为退群通知，类型有：leave, kick, kick_me
        self.leave_group_type: str
        # 若为群管理员变动通知，类型有：set, unset
        self.admin_change_type: str
        # 若为文件上传通知，此处为 通知文件信息对象
        self.file: NoticeEvent.File
        # 若为群禁言通知，类型有：ban, lift_ban
        self.group_ban_type: str
        # 若为禁言通知，禁言时长
        self.ban_time: int
        # 若为群荣誉变更通知，类型有：talkactive, performer, emotion
        self.honor_change_type: str
        # 若为群头衔变更通知，新头衔
        self.new_title: str
        # 若为群名片更新事件，旧名片和新名片；注意名片为空时，对应属性为空字符串
        self.old_card: str
        self.new_card: str
        # 若为客户端在线状态变更事件，此处为 通知客户端信息对象
        self.client: NoticeEvent.Client
        # 若为精华消息变更事件，类型有：add, delete
        self.essence_change_type: str

        self._init()

    @property
    def time(self) -> int:
        return self.raw.get("time")

    @property
    def type(self) -> str:
        return "notice"

    def _init(self) -> None:
        """
        外部确认为该类型事件时，调用此方法。
        """
        rawEvent = self.raw

        if self.is_friend_recall():
            self.notice_user_id = rawEvent["user_id"]
            self.notice_msg_id = rawEvent["message_id"]
        elif self.is_group_recall():
            self.notice_user_id = rawEvent["user_id"]
            self.notice_group_id = rawEvent["group_id"]
            self.notice_operator_id = rawEvent["operator_id"]
            self.notice_msg_id = rawEvent["message_id"]
        elif self.is_group_increase():
            self.join_group_type = rawEvent["sub_type"]
            self.notice_user_id = rawEvent["user_id"]
            self.notice_group_id = rawEvent["group_id"]
            self.notice_operator_id = rawEvent["operator_id"]
        elif self.is_group_decrease():
            self.leave_group_type = rawEvent["sub_type"]
            self.notice_user_id = rawEvent["user_id"]
            self.notice_group_id = rawEvent["group_id"]
            self.notice_operator_id = rawEvent["operator_id"]
        elif self.is_group_admin():
            self.admin_change_type = rawEvent["sub_type"]
            self.notice_user_id = rawEvent["user_id"]
            self.notice_group_id = rawEvent["group_id"]
        elif self.is_group_upload():
            self.notice_user_id = rawEvent["user_id"]
            self.notice_group_id = rawEvent["group_id"]
            self.file = NoticeEvent.File(rawEvent, isGroup=True)
        elif self.is_group_ban():
            self.notice_user_id = rawEvent["user_id"]
            self.notice_group_id = rawEvent["group_id"]
            self.notice_operator_id = rawEvent["operator_id"]
            self.group_ban_type = rawEvent["sub_type"]
            self.ban_time = rawEvent["duration"]
        elif self.is_friend_add():
            self.notice_user_id = rawEvent["user_id"]
        elif self.is_poke():
            self.notice_user_id = rawEvent["target_id"]
            self.notice_operator_id = rawEvent["user_id"]
            if "group_id" in rawEvent.keys():
                self.notice_group_id = rawEvent["group_id"]
        elif self.is_lucky_king():
            self.notice_user_id = rawEvent["target_id"]
            self.notice_group_id = rawEvent["group_id"]
            self.notice_operator_id = rawEvent["user_id"]
        elif self.is_honor():
            self.honor_change_type = rawEvent["honor_type"]
            self.notice_user_id = rawEvent["user_id"]
            self.notice_group_id = rawEvent["group_id"]
        elif self.is_title():
            self.new_title = rawEvent["title"]
            self.notice_user_id = rawEvent["user_id"]
            self.notice_group_id = rawEvent["group_id"]
        elif self.is_group_card():
            self.old_card = rawEvent["card_old"]
            self.new_card = rawEvent["card_new"]
            self.notice_user_id = rawEvent["user_id"]
            self.notice_group_id = rawEvent["group_id"]
        elif self.is_offline_file():
            self.notice_user_id = rawEvent["user_id"]
            self.file = NoticeEvent.File(rawEvent, isGroup=False)
        elif self.is_client_status():
            self.client = NoticeEvent.Client(rawEvent)
        elif self.is_essence():
            self.essence_change_type = rawEvent["sub_type"]
            self.notice_user_id = rawEvent["sender_id"]
            self.notice_group_id = rawEvent["group_id"]
            self.notice_operator_id = rawEvent["operator_id"]
            self.notice_msg_id = rawEvent["message_id"]

    def is_group(self) -> bool:
        """
        是否是来自群的通知事件
        """
        return "group_id" in self.raw.keys()

    def is_group_upload(self) -> bool:
        return self.raw["notice_type"] == "group_upload"

    def is_group_admin(self) -> bool:
        return self.raw["notice_type"] == "group_admin"

    def is_group_decrease(self) -> bool:
        return self.raw["notice_type"] == "group_decrease"

    def is_group_increase(self) -> bool:
        return self.raw["notice_type"] == "group_increase"

    def is_group_ban(self) -> bool:
        return self.raw["notice_type"] == "group_ban"

    def is_friend_add(self) -> bool:
        return self.raw["notice_type"] == "friend_add"

    def is_group_recall(self) -> bool:
        return self.raw["notice_type"] == "group_recall"

    def is_friend_recall(self) -> bool:
        return self.raw["notice_type"] == "friend_recall"

    def is_group_card(self) -> bool:
        return self.raw["notice_type"] == "group_card"

    def is_offline_file(self) -> bool:
        """是否为离线文件上传事件（即私聊文件上传）"""
        return self.raw["notice_type"] == "offline_file"

    def is_client_status(self) -> bool:
        return self.raw["notice_type"] == "client_status"

    def is_essence(self) -> bool:
        return self.raw["notice_type"] == "essence"

    def is_notify(self) -> bool:
        """是否为系统通知事件（包含群荣誉变更、戳一戳、群红包幸运王、群成员头衔变更）"""
        return self.raw["notice_type"] == "notify"

    def is_honor(self) -> bool:
        return self.raw["notice_type"] == "notify" and self.raw["sub_type"] == "honor"

    def is_poke(self) -> bool:
        return self.raw["notice_type"] == "notify" and self.raw["sub_type"] == "poke"

    def is_lucky_king(self) -> bool:
        return (
            self.raw["notice_type"] == "notify" and self.raw["sub_type"] == "lucky_king"
        )

    def is_title(self) -> bool:
        return self.raw["notice_type"] == "notify" and self.raw["sub_type"] == "title"

    class File:
        """
        通知中文件信息类
        """

        def __init__(self, rawEvent: dict, isGroup: bool) -> None:
            self.id: str = None
            self.name: str = None
            self.size: int = None
            self.busid: int = None
            self.url: str = None

            self.name = rawEvent["file"]["name"]
            self.size = rawEvent["file"]["size"]
            if isGroup:
                self.id = rawEvent["file"]["id"]
                self.busid = rawEvent["file"]["busid"]
            else:
                self.url = rawEvent["file"]["url"]

    class Client:
        """
        通知中客户端信息类
        """

        def __init__(self, rawEvent: dict) -> None:
            self.online = rawEvent["online"]
            self.id = rawEvent["client"]["app_id"]
            self.name = rawEvent["client"]["device_name"]
            self.kind = rawEvent["client"]["device_kind"]


class MetaEvent(BotEvent):
    def __init__(self, rawEvent: dict) -> None:
        super().__init__(rawEvent)
        self.bot_id = rawEvent.get("self_id")

    @property
    def time(self) -> int:
        return self.raw.get("time")

    @property
    def type(self) -> str:
        return "meta"

    def is_lifecycle(self) -> bool:
        return self.raw["meta_event_type"] == "lifecycle"

    def is_heartbeat(self) -> bool:
        return self.raw["meta_event_type"] == "heartbeat"


class ResponseEvent(BotEvent):
    def __init__(self, rawEvent: dict) -> None:
        super().__init__(rawEvent)
        self.status = rawEvent.get("retcode")

        # 响应标识符
        self.id: str = None
        # 状态码
        self.status: int = None
        # 错误
        self.err: str = None
        # 错误提示
        self.err_prompt: str = None
        # 响应数据
        self.data: dict = None

        self._init()

    @property
    def time(self) -> int:
        return int(time.time())

    @property
    def type(self) -> str:
        return "response"

    def _init(self) -> None:
        rawEvent = self.raw
        self.status = rawEvent["retcode"]
        if "echo" in rawEvent.keys() and rawEvent["echo"]:
            self.id = rawEvent["echo"]
        if "data" in rawEvent.keys() and rawEvent["data"]:
            self.data = rawEvent["data"]

    def is_ok(self) -> bool:
        """判断是否为成功响应"""
        return self.raw["status"] == "ok"

    def is_processing(self) -> bool:
        """判断响应是否在被异步处理，即未完成但在处理中"""
        return self.status == 202

    def is_failed(self) -> bool:
        """判断是否为失败响应"""
        return self.raw["status"] != "ok"
