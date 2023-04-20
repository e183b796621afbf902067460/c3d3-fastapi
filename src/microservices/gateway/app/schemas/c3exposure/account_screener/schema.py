from pydantic import BaseModel
from datetime import datetime


class LabelORMSchema(BaseModel):
    h_label_id: int
    h_label_name: str
    h_label_api_key: str
    h_label_secret_key: str
    h_label_load_ts: datetime

    class Config:
        orm_mode = True


class NewLabelSchema(BaseModel):
    label_name: str
    label_api_key: str
    label_api_secret: str
