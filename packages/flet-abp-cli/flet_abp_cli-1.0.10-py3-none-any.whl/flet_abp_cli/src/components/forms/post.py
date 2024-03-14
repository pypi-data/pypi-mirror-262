from pydantic import BaseModel, Field
from typing_extensions import Literal
from components.forms.base import BaseForm


class PostForm(BaseForm):
    class Schema(BaseModel):
        content: str = Field(title='Введите логин', default='какая то дефолтная строчка', min_length=5)
        phone: str = Field(title='Введите телефон', type='phone', min_length=14)
        currency: float = Field(title="Введите сумму", type='float', decimals=2)
        tag: Literal['IT', 'COOKING', 'ENTERTAINMENT'] = Field(title='Тип', default=None)

    schema = Schema
