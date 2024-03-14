from enum import Enum

class ClassFactory:

    class Type(Enum):
        pass

    def __new__(cls, type_: Type, *args, **kwargs) -> object:

        if not hasattr(cls, "LUT"):
            raise(NotImplementedError(
                f"{cls.__name__}.LUT must be defined")
            )
        
        if type_ in cls.LUT:
            return cls.LUT[type_](*args, **kwargs)
        else:
            raise(ValueError(f"Unsupported class type value: {type_}"))


