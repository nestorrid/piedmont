import typing as t
import serial

T_Handler = t.TypeVar("T_Handler", bound=t.Callable[..., t.Any])
T_Mapper = t.TypeVar("T_Mapper", bound=t.Dict[t.AnyStr, T_Handler])
T_PP_Message_Payload = t.TypeVar(
    "T_PP_Message_Payload",
    bound=t.Union[str, t.List[t.Any], t.Dict[t.AnyStr, t.Any]]
)

T_Serial_Config = t.TypeVar("T_Serial_Config", bound=t.Union[
    t.List[t.Any],
    t.Dict[t.AnyStr, t.Any],
    serial.Serial
])
