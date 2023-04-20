from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Optional
from cryptography import fernet

from app.schemas.dex_erc_screener.schema import (
    TokenOnWalletORMSchema
)
from app.orm.cfg.engine import ORMSettings
from app.cfg.settings import settings
from app.orm import base


class DexERCScreenerService:

    def __init__(self, session: Session = Depends(ORMSettings.get_session)):
        self._session: Session = session
        self._fn = fernet.Fernet(key=settings.JWT_FERNET_KEY)

    def _get_h_chain_by_name(self, network_name: str) -> Optional[base.hChains]:
        return self._session.query(base.hChains).filter_by(h_network_name=network_name).first()

    def _get_h_address_by_name(self, address_name: str) -> Optional[base.hAddresses]:
        return self._session.query(base.hAddresses).filter_by(h_address=address_name).first()

    def _get_h_label_by_name(self, label_name: str) -> Optional[base.hLabels]:
        return self._session.query(base.hLabels).filter_by(h_label_name=label_name).first()

    def _get_l_address_chain(self, address_name: str, network_name: str) -> Optional[base.lAddressesChains]:
        h_address, h_chain = self._get_h_address_by_name(address_name=address_name), self._get_h_chain_by_name(network_name=network_name)
        if not h_address or not h_chain: return None

        return self._session.query(base.lAddressesChains).filter_by(
            h_address_id=h_address.h_address_id,
            h_chain_id=h_chain.h_chain_id
        ).first()

    def _get_l_address_chain_label(self, address_name: str, network_name: str, label_name: str) -> Optional[base.lAddressesChainsLabels]:
        h_label = self._get_h_label_by_name(label_name=label_name)
        if not h_label: return None

        l_address_chain = self._get_l_address_chain(address_name=address_name, network_name=network_name)
        if not l_address_chain: return None

        return self._session.query(base.lAddressesChainsLabels).filter_by(
            l_address_chain_id=l_address_chain.l_address_chain_id,
            h_label_id=h_label.h_label_id
        ).first()

    def _get_l_token_on_wallet(self, wallet_address: str, token_address: str, network_name: str, label_name: str) -> Optional[base.lTokensOnWallets]:
        l_address_chain, l_address_chain_label = self._get_l_address_chain(
            address_name=token_address,
            network_name=network_name
        ), self._get_l_address_chain_label(
            address_name=wallet_address,
            network_name=network_name,
            label_name=label_name
        )

        if not l_address_chain_label or not l_address_chain: return None

        return self._session.query(base.lTokensOnWallets).filter_by(
            l_address_chain_id=l_address_chain.l_address_chain_id,
            l_address_chain_label_id=l_address_chain_label.l_address_chain_label_id
        ).first()

    def _insert_h_address(self, address_name: str) -> base.hAddresses:
        h_address = self._get_h_address_by_name(
            address_name=address_name
        )
        if not h_address:
            h_address = base.hAddresses(
                h_address=address_name
            )
            self._session.add(h_address)
            self._session.commit()
        return h_address

    def _insert_h_label(self, label_name: str) -> base.hLabels:
        h_label = self._get_h_label_by_name(
            label_name=label_name
        )
        if not h_label:
            h_label = base.hLabels(
                h_label_name=label_name
            )
            self._session.add(h_label)
            self._session.commit()
        return h_label

    def _insert_l_address_chain(self, network_name: str, address_name: str) -> Optional[base.lAddressesChains]:
        h_chain, h_address = self._get_h_chain_by_name(
            network_name=network_name
        ), self._insert_h_address(
            address_name=address_name
        )
        if not h_chain: return None

        l_address_chain = self._get_l_address_chain(
            address_name=address_name,
            network_name=network_name
        )
        if not l_address_chain:
            l_address_chain = base.lAddressesChains(
                h_address_id=h_address.h_address_id,
                h_chain_id=h_chain.h_chain_id
            )
            self._session.add(l_address_chain)
            self._session.commit()
        return l_address_chain

    def _insert_l_address_chain_label(self, address_name: str, network_name: str, label_name: str) -> Optional[base.lAddressesChainsLabels]:
        h_label = self._insert_h_label(
            label_name=label_name
        )
        l_address_chain = self._insert_l_address_chain(
            network_name=network_name,
            address_name=address_name
        )
        if not l_address_chain: return None

        l_address_chain_label = self._get_l_address_chain_label(
            address_name=address_name,
            network_name=network_name,
            label_name=label_name
        )
        if not l_address_chain_label:
            l_address_chain_label = base.lAddressesChainsLabels(
                l_address_chain_id=l_address_chain.l_address_chain_id,
                h_label_id=h_label.h_label_id
            )
            self._session.add(l_address_chain_label)
            self._session.commit()
        return l_address_chain_label

    def _insert_l_token_on_wallet(
            self,
            wallet_address: str, token_address: str,
            network_name: str, label_name: str
    ) -> Optional[base.lTokensOnWallets]:
        l_address_chain_label, l_address_chain = self._insert_l_address_chain_label(
            address_name=wallet_address,
            network_name=network_name,
            label_name=label_name
        ), self._insert_l_address_chain(
            address_name=token_address,
            network_name=network_name
        )
        if not l_address_chain_label or not l_address_chain: return None

        l_token_on_wallet = self._get_l_token_on_wallet(
            wallet_address=wallet_address,
            token_address=token_address,
            network_name=network_name,
            label_name=label_name
        )
        if not l_token_on_wallet:
            l_token_on_wallet = base.lTokensOnWallets(
                l_address_chain_id=l_address_chain.l_address_chain_id,
                l_address_chain_label_id=l_address_chain_label.l_address_chain_label_id
            )
            self._session.add(l_token_on_wallet)
            self._session.commit()
        return l_token_on_wallet

    def on_post(
            self,
            wallet_address: str, token_address: str,
            network_name: str, label_name: str
    ) -> Optional[TokenOnWalletORMSchema]:
        l_token_on_wallet = self._insert_l_token_on_wallet(
            wallet_address=wallet_address,
            token_address=token_address,
            network_name=network_name,
            label_name=label_name
        )
        return TokenOnWalletORMSchema.from_orm(l_token_on_wallet) if l_token_on_wallet else None
