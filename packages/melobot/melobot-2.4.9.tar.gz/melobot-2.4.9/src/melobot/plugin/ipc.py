import asyncio as aio
from asyncio import iscoroutinefunction
from functools import partial
from types import MethodType

from ..types.abc import PluginSignalHandlerArgs, ShareObjCbArgs
from ..types.exceptions import *
from ..types.tools import get_rich_str
from ..types.typing import *

if TYPE_CHECKING:
    from ..plugin.plugin import Plugin
    from ..utils.logger import Logger


class ShareObject:
    """
    共享对象
    """

    def __init__(self, namespace: str, id: str) -> None:
        self.__space = namespace
        self.__id = id
        self.__reflect: Callable[[None], object] = lambda: None
        self.__callback: Coroutine

        self.__cb_set = aio.Event()

    def _fill_ref(self, reflect_func: Callable[[None], object]) -> None:
        self.__reflect = reflect_func

    def _fill_cb(self, callback: Coroutine) -> None:
        self.__callback = callback
        self.__cb_set.set()

    @property
    def val(self) -> Any:
        """
        共享对象引用的值
        """
        return self.__reflect()

    async def affect(self, *args, **kwargs) -> Any:
        """
        触发共享对象的回调，回调未设置时会等待。
        如果本来就没有回调，则会陷入无休止等待
        """
        await self.__cb_set.wait()
        return await self.__callback(*args, **kwargs)


class PluginStore:
    """
    插件共享存储
    """

    __store__: Dict[str, Dict[str, ShareObject]] = {}

    @classmethod
    def _create_so(
        cls, property: Optional[str], namespace: str, id: str, plugin: "Plugin"
    ) -> None:
        """
        创建共享对象。property 为 None 时，共享对象会引用到一个 None
        """
        if namespace not in cls.__store__.keys():
            cls.__store__[namespace] = {}
        obj = cls.__store__[namespace].get(id)
        if obj is None:
            obj = ShareObject(namespace, id)
            cls.__store__[namespace][id] = obj
        if property is not None:
            obj._fill_ref(lambda: getattr(plugin, property))
        else:
            obj._fill_ref(lambda: None)

    @classmethod
    def _bind_cb(
        cls,
        namespace: str,
        id: str,
        cb: Callable[..., Coroutine[Any, Any, Any]],
        plugin: "Plugin",
    ) -> None:
        """
        为共享对象绑定回调
        """
        if namespace not in cls.__store__.keys():
            raise ShareObjError(f"共享对象回调指定的命名空间 {namespace} 不存在")
        if id not in cls.__store__[namespace].keys():
            raise ShareObjError(
                f"共享对象回调指定的命名空间中，不存在标记为 {id} 的共享对象"
            )
        if cls.__store__[namespace][id].__cb_set.is_set():
            raise ShareObjError(
                f"{namespace} 中标记为 {id} 的共享对象已被注册过回调，拒绝再次注册"
            )
        cls.__store__[namespace][id]._fill_cb(partial(cb, plugin))

    @classmethod
    def echo(cls, namespace: str, id: str) -> Callable:
        """
        为共享对象指定回调的装饰器，用于处理外部的 affect 请求。
        绑定为回调后，不提供异步安全担保
        """

        def bind_cb(cb: Callable[..., Coroutine[Any, Any, Any]]) -> ShareObjCbArgs:
            return ShareObjCbArgs(namespace=namespace, id=id, cb=cb)

        return bind_cb

    @classmethod
    def get(cls, namespace: str, id: str) -> ShareObject:
        """
        获取共享对象，注意：共享对象不存在或暂时未初始化时会产生 None 引用。
        区别是前者会一直保持 None 引用，而后者则会随后绑定映射。
        但注意，除上述两种情况外，共享对象定义时也可引用到 None
        """
        if namespace not in cls.__store__.keys():
            cls.__store__[namespace] = {}
        if id not in cls.__store__[namespace].keys():
            cls.__store__[namespace][id] = ShareObject(namespace, id)
        return cls.__store__[namespace][id]


class PluginSignalHandler:
    """
    插件信号处理器
    """

    def __init__(
        self,
        namespace: str,
        signal: str,
        func: Callable[..., Coroutine[Any, Any, Any]],
        plugin: Optional[object],
    ) -> None:
        self._func = func
        self._plugin = plugin
        # 对应：绑定的 func 是插件类的实例方法
        if plugin:
            self.cb = partial(self._func, plugin)
        # 对应：绑定的 func 是普通函数
        else:
            self.cb = self._func
        self.namespace = namespace
        self.signal = signal


class PluginBus:
    """
    插件信号总线
    """

    __store__: Dict[str, Dict[str, PluginSignalHandler]] = {}
    __logger: "Logger"

    @classmethod
    def _bind(cls, logger: "Logger") -> None:
        """
        初始化该类，绑定全局日志器和行为响应器
        """
        cls.__logger = logger

    @classmethod
    def _register(
        cls, namespace: str, signal: str, handler: PluginSignalHandler
    ) -> None:
        """
        注册一个插件信号处理方法。由 plugin build 过程调用
        """
        if namespace not in cls.__store__.keys():
            cls.__store__[namespace] = {}
        cls.__store__[namespace][signal] = handler

    @classmethod
    def on(
        cls,
        namespace: str,
        signal: str,
        callback: Callable[..., Coroutine[Any, Any, Any]] = None,
    ):
        """
        动态地注册插件信号处理方法。callback 可以是类实例方法，也可以不是。
        callback 如果是类实例方法，请自行包裹为一个 partial 函数。

        例如你的插件类是：`A`，而你需要传递一个类实例方法：`A.xxx`，
        那么你的 callback 参数就应该是：`functools.partial(A.xxx, self)`
        """

        def make_args(
            func: Callable[..., Coroutine[Any, Any, Any]]
        ) -> PluginSignalHandlerArgs:
            return PluginSignalHandlerArgs(
                func=func, namespace=namespace, signal=signal
            )

        if callback is None:
            return make_args
        else:
            if isinstance(callback, PluginSignalHandlerArgs):
                raise PluginSignalError("已注册的插件信号处理方法不能再注册")
            if not iscoroutinefunction(callback):
                raise PluginSignalError(
                    f"插件信号处理方法 {callback.__name__} 必须为异步函数"
                )
            if (
                isinstance(callback, partial) and isinstance(callback.func, MethodType)
            ) or isinstance(callback, MethodType):
                raise PluginSignalError(
                    "callback 应该是 function，而不是 bound method。"
                )
            handler = PluginSignalHandler(namespace, signal, callback, plugin=None)
            cls._register(namespace, signal, handler)

    @classmethod
    async def _run_on_ctx(cls, handler: PluginSignalHandler, *args, **kwargs) -> Any:
        """
        在指定的上下文下运行插件信号处理方法
        """
        try:
            ret = await handler.cb(*args, **kwargs)
            return ret
        except Exception as e:
            func_name = handler._func.__qualname__
            pre_str = "插件" + handler._plugin.ID if handler._plugin else "动态注册的"
            cls.__logger.error(f"{pre_str} 插件信号处理方法 {func_name} 发生异常")
            cls.__logger.error("异常回溯栈：\n" + get_better_exc(e))
            cls.__logger.error("异常点局部变量：\n" + get_rich_str(locals()))

    @classmethod
    async def emit(
        cls,
        namespace: str,
        signal: str,
        *args,
        wait: bool = False,
        **kwargs,
    ) -> Any:
        """
        触发一个插件信号。如果指定 wait 为 True，则会等待所有插件信号处理方法完成。
        若启用 forward，则会将 session 从信号触发处转发到信号处理处。
        但启用 forward，必须同时启用 wait。

        注意：如果你要等待返回结果，则需要指定 wait=True，否则不会等待且始终返回 None
        """
        if namespace not in cls.__store__.keys():
            raise PluginSignalError(
                f"插件信号命名空间 {namespace} 不存在，无法触发信号"
            )
        if signal not in cls.__store__[namespace].keys():
            return

        handler = cls.__store__[namespace][signal]
        if not wait:
            aio.create_task(cls._run_on_ctx(handler, *args, **kwargs))
            return None
        else:
            return await cls._run_on_ctx(handler, *args, **kwargs)
