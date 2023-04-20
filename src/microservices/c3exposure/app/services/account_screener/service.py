from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Optional
from cryptography import fernet

from app.schemas.account_screener.schema import (
    LabelORMSchema
)
from app.orm.cfg.engine import ORMSettings
from app.cfg.settings import settings
from app.orm import base


class AccountScreenerService:

    def __init__(self, session: Session = Depends(ORMSettings.get_session)):
        self._session: Session = session
        self._fn = fernet.Fernet(key=settings.JWT_FERNET_KEY)

    def _get_h_label_by_name(self, label_name: str) -> Optional[base.hLabels]:
        return self._session.query(base.hLabels).filter_by(h_label_name=label_name).first()

    def _insert_h_label(self, label_name: str, label_api_key: str, label_api_secret: str) -> base.hLabels:
        h_label = self._get_h_label_by_name(label_name=label_name)
        if not h_label:
            h_label = base.hLabels(
                h_label_name=label_name,
                h_label_api_key=label_api_key,
                h_label_secret_key=label_api_secret
            )
            self._session.add(h_label)
            self._session.commit()
        return h_label

    def _hash_by_fernet(self, value: str) -> str:
        return self._fn.encrypt(value.encode()).decode()

    def on_post(self, label_name: str, label_api_key: str, label_api_secret: str) -> LabelORMSchema:
        h_label = self._insert_h_label(
            label_name=label_name,
            label_api_key=self._hash_by_fernet(value=label_api_key),
            label_api_secret=self._hash_by_fernet(value=label_api_secret)
        )
        return LabelORMSchema.from_orm(h_label)
