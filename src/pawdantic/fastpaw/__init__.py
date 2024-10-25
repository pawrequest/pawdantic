import inspect
from typing import Annotated
from pydantic import BaseModel

from fastapi import Form


def as_form(cls):
    new_params = [
        inspect.Parameter(
            field_name,
            inspect.Parameter.POSITIONAL_ONLY,
            default=model_field.default,
            annotation=Annotated[model_field.annotation, *model_field.metadata, Form(alias=model_field.alias, alias_priority=model_field.alias_priority)]
        )
        for field_name, model_field in cls.model_fields.items()
    ]

    cls.__signature__ = cls.__signature__.replace(parameters=new_params)

    return cls

def as_form_old(cls: type[BaseModel]):
    new_parameters = []

    for field_name, model_field in cls.model_fields.items():
        model_field: ModelField  # type: ignore

        new_parameters.append(
             inspect.Parameter(
                 model_field.alias,
                 inspect.Parameter.POSITIONAL_ONLY,
                 default=Form(...) if model_field.required else Form(model_field.default),
                 annotation=model_field.outer_type_,
             )
         )

    async def as_form_func(**data):
        return cls(**data)

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_func.__signature__ = sig  # type: ignore
    setattr(cls, 'as_form', as_form_func)
    return cls

"""
https://stackoverflow.com/questions/60127234/how-to-use-a-pydantic-model-with-form-data-in-fastapi/77113651#77113651
def before_validate_int(value: int) -> int:
    raise ValueError('before int')


MyInt = Annotated[int, BeforeValidator(before_validate_int)]


@as_form
class User(BaseModel):
    age: MyInt


@app.post("/postdata")
def postdata(user: User = Depends()):
    return {"age": user.age}
    """
