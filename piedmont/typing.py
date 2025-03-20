import typing as t

T_Handler = t.TypeVar("T_Handler", bound=t.Callable[..., t.Any])
T_Mapper = t.TypeVar("T_Mapper", bound=t.Dict[t.AnyStr, T_Handler])
