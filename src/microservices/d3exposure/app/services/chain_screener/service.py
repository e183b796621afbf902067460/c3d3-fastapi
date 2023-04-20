from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Optional
from cryptography import fernet

from app.schemas.chain_screener.schema import (
    ChainORMSchema
)
from app.orm.cfg.engine import ORMSettings
from app.cfg.settings import settings
from app.orm import base


class ChainScreenerService:

    def __init__(self, session: Session = Depends(ORMSettings.get_session)):
        self._session: Session = session
        self._fn = fernet.Fernet(key=settings.JWT_FERNET_KEY)

    def _get_h_chain_by_name(self, network_name: str) -> Optional[base.hChains]:
        return self._session.query(base.hChains).filter_by(h_network_name=network_name).first()

    def _insert_h_chain(
            self,
            network_name: str, native_chain_token: str,
            rpc_node: str, block_limit: int, network_uri: str,
            network_api_key: str
    ) -> base.hChains:
        h_chain = self._get_h_chain_by_name(
            network_name=network_name
        )
        if not h_chain:
            h_chain = base.hChains(
                h_network_name=network_name,
                h_native_chain_token=native_chain_token,
                h_network_rpc_node=rpc_node,
                h_network_block_limit=block_limit,
                h_network_uri=network_uri,
                h_network_api_key=network_api_key
            )
            self._session.add(h_chain)
            self._session.commit()
        return h_chain

    def _hash_by_fernet(self, value: str) -> str:
        return self._fn.encrypt(value.encode()).decode()

    def on_post(
            self,
            network_name: str, native_chain_token: str,
            rpc_node: str, block_limit: int, network_uri: str,
            network_api_key: str
    ) -> ChainORMSchema:
        h_chain = self._get_h_chain_by_name(
            network_name=network_name
        )
        if not h_chain:
            h_chain = self._insert_h_chain(
                network_name=network_name,
                native_chain_token=native_chain_token,
                rpc_node=self._hash_by_fernet(value=rpc_node),
                block_limit=block_limit,
                network_uri=network_uri,
                network_api_key=self._hash_by_fernet(value=network_api_key)
            )
        return ChainORMSchema.from_orm(h_chain)
