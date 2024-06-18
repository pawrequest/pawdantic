import inspect
from typing import Annotated

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
