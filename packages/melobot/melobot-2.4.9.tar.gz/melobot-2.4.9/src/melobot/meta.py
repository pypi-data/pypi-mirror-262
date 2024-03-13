import os
import sys
from typing import Any, Dict


class MetaInfo:
    """melobot 元信息类"""

    def __init__(self) -> None:
        self.VER = "2.4.9"
        self.PROJ_NAME = "MeloBot"
        self.PROJ_DESC = "A qbot module with friendly interface, session control and plugin-supported."
        self.PROJ_SRC = "https://github.com/aicorein/melobot"
        self.AUTHOR = "aicorein"
        self.AUTHOR_EMAIL = "melodyecho@glowmem.com"
        self.ARGV = sys.argv
        self.PLATFORM = sys.platform
        self.PY_VER = sys.version
        self.PY_INFO = sys.version_info
        self.OS_SEP = os.sep
        self.PATH_SEP = os.pathsep
        self.LINE_SEP = os.linesep
        self.ENV = os.environ

    def get_all(self) -> Dict[str, Any]:
        """将所有元信息以字典形式返回

        Returns:
            Dict[str, Any]: 包含所有元信息的字典
        """
        return dict(self.__dict__.items())


MODULE_MODE_FLAG = "MELOBOT_MODULE"
MODULE_MODE_SET = "1"
MODULE_MODE_UNSET = "0"
EXIT_CLOSE = 0x0
EXIT_ERROR = 0x1
EXIT_RESTART = 0x10
MELOBOT_LOGO = """  __  __      _       ____        _   
 |  \/  | ___| | ___ | __ )  ___ | |_ 
 | |\/| |/ _ \ |/ _ \|  _ \ / _ \| __|
 | |  | |  __/ | (_) | |_) | (_) | |_ 
 |_|  |_|\___|_|\___/|____/ \___/ \__|
"""
