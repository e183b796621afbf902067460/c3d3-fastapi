from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Optional
from cryptography import fernet

from app.schemas.dex_borrow_screener.schema import (
    AddressChainProtocolSpecificationLabelORMSchema
)
from app.orm.cfg.engine import ORMSettings
from app.cfg.settings import settings
from app.orm import base


class DexBorrowScreenerService:

    def __init__(self, session: Session = Depends(ORMSettings.get_session)):
        self._session: Session = session
        self._fn = fernet.Fernet(key=settings.JWT_FERNET_KEY)

    def _get_h_chain_by_name(self, network_name: str) -> Optional[base.hChains]:
        return self._session.query(base.hChains).filter_by(h_network_name=network_name).first()

    def _get_h_address_by_name(self, address_name: str) -> Optional[base.hAddresses]:
        return self._session.query(base.hAddresses).filter_by(h_address=address_name).first()

    def _get_h_specification_by_name(self, specification_name: str) -> Optional[base.hSpecifications]:
        return self._session.query(base.hSpecifications).filter_by(h_specification_name=specification_name).first()

    def _get_h_protocol_by_name(self, protocol_name: str) -> Optional[base.hProtocols]:
        return self._session.query(base.hProtocols).filter_by(h_protocol_name=protocol_name).first()

    def _get_h_label_by_name(self, label_name: str) -> Optional[base.hLabels]:
        return self._session.query(base.hLabels).filter_by(h_label_name=label_name).first()

    def _get_l_address_chain(self, address_name: str, network_name: str) -> Optional[base.lAddressesChains]:
        h_address, h_chain = self._get_h_address_by_name(address_name=address_name), self._get_h_chain_by_name(network_name=network_name)
        if not h_address or not h_chain: return None

        return self._session.query(base.lAddressesChains).filter_by(
            h_address_id=h_address.h_address_id,
            h_chain_id=h_chain.h_chain_id
        ).first()

    def _get_l_protocol_specification(self, protocol_name: str, specification_name: str) -> Optional[base.lProtocolsSpecifications]:
        h_protocol, h_specification = self._get_h_protocol_by_name(protocol_name=protocol_name), self._get_h_specification_by_name(specification_name=specification_name)
        if not h_protocol or not h_specification: return None

        return self._session.query(base.lProtocolsSpecifications).filter_by(
            h_protocol_id=h_protocol.h_protocol_id,
            h_specification_id=h_specification.h_specification_id
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

    def _get_l_address_chain_protocol_specification(self, protocol_name: str, specification_name: str, network_name: str, address_name: str) -> Optional[base.lAddressesChainsProtocolsSpecifications]:
        l_address_chain, l_protocol_specification = self._get_l_address_chain(
            address_name=address_name,
            network_name=network_name
        ), self._get_l_protocol_specification(
            protocol_name=protocol_name,
            specification_name=specification_name
        )
        if not l_address_chain or not l_protocol_specification: return None

        return self._session.query(base.lAddressesChainsProtocolsSpecifications).filter_by(
            l_address_chain_id=l_address_chain.l_address_chain_id,
            l_protocol_specification_id=l_protocol_specification.l_protocol_specification_id
        ).first()

    def _get_l_address_chain_protocol_specification_label(
            self,
            wallet_address: str, pool_address: str,
            protocol_name: str, specification_name: str,
            network_name: str, label_name: str
    ) -> Optional[base.lAddressesChainsProtocolsSpecificationsLabels]:

        l_address_chain_label, l_address_chain_protocol_specification = self._get_l_address_chain_label(
            address_name=wallet_address,
            network_name=network_name,
            label_name=label_name
        ), self._get_l_address_chain_protocol_specification(
            address_name=pool_address,
            network_name=network_name,
            protocol_name=protocol_name,
            specification_name=specification_name
        )
        if not l_address_chain_label or not l_address_chain_protocol_specification: return None

        return self._session.query(base.lAddressesChainsProtocolsSpecificationsLabels).filter_by(
            l_address_chain_label_id=l_address_chain_label.l_address_chain_label_id,
            l_address_chain_protocol_specification_id=l_address_chain_protocol_specification.l_address_chain_protocol_specification_id
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

    def _insert_h_protocol(self, protocol_name: str) -> base.hProtocols:
        h_protocol = self._get_h_protocol_by_name(
            protocol_name=protocol_name
        )
        if not h_protocol:
            h_protocol = base.hProtocols(
                h_protocol_name=protocol_name
            )
            self._session.add(h_protocol)
            self._session.commit()
        return h_protocol

    def _insert_h_specification(self, specification_name: str) -> base.hSpecifications:
        h_specification = self._get_h_specification_by_name(
            specification_name=specification_name
        )
        if not h_specification:
            h_specification = base.hSpecifications(
                h_specification_name=specification_name
            )
            self._session.add(h_specification)
            self._session.commit()
        return h_specification

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

    def _insert_l_protocol_specification(self, protocol_name: str, specification_name: str) -> base.lProtocolsSpecifications:
        h_protocol, h_specification = self._insert_h_protocol(
            protocol_name=protocol_name
        ), self._insert_h_specification(
            specification_name=specification_name
        )

        l_protocol_specification = self._get_l_protocol_specification(
            protocol_name=protocol_name,
            specification_name=specification_name
        )
        if not l_protocol_specification:
            l_protocol_specification = base.lProtocolsSpecifications(
                h_protocol_id=h_protocol.h_protocol_id,
                h_specification_id=h_specification.h_specification_id
            )
            self._session.add(l_protocol_specification)
            self._session.commit()
        return l_protocol_specification

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

    def _insert_l_address_chain_protocol_specification(
            self,
            address_name: str, network_name: str,
            protocol_name: str, specification_name: str
    ) -> Optional[base.lAddressesChainsProtocolsSpecifications]:
        l_address_chain, l_protocol_specification = self._insert_l_address_chain(
            network_name=network_name,
            address_name=address_name
        ), self._insert_l_protocol_specification(
            protocol_name=protocol_name,
            specification_name=specification_name
        )
        if not l_address_chain: return None

        l_address_chain_protocol_specification = self._get_l_address_chain_protocol_specification(
            address_name=address_name,
            protocol_name=protocol_name,
            network_name=network_name,
            specification_name=specification_name
        )
        if not l_address_chain_protocol_specification:
            l_address_chain_protocol_specification = base.lAddressesChainsProtocolsSpecifications(
                l_address_chain_id=l_address_chain.l_address_chain_id,
                l_protocol_specification_id=l_protocol_specification.l_protocol_specification_id
            )
            self._session.add(l_address_chain_protocol_specification)
            self._session.commit()
        return l_address_chain_protocol_specification

    def _insert_l_address_chain_protocol_specification_label(
            self,
            wallet_address: str, pool_address: str,
            network_name: str, label_name: str,
            protocol_name: str, specification_name: str
    ) -> Optional[base.lAddressesChainsProtocolsSpecificationsLabels]:
        l_address_chain_label, l_address_chain_protocol_specification = self._insert_l_address_chain_label(
            address_name=wallet_address,
            network_name=network_name,
            label_name=label_name
        ), self._insert_l_address_chain_protocol_specification(
            address_name=pool_address,
            network_name=network_name,
            protocol_name=protocol_name,
            specification_name=specification_name
        )
        if not l_address_chain_label or not l_address_chain_protocol_specification: return None

        l_address_chain_protocol_specification_label = self._get_l_address_chain_protocol_specification_label(
            wallet_address=wallet_address,
            pool_address=pool_address,
            network_name=network_name,
            label_name=label_name,
            protocol_name=protocol_name,
            specification_name=specification_name
        )
        if not l_address_chain_protocol_specification_label:
            l_address_chain_protocol_specification_label = base.lAddressesChainsProtocolsSpecificationsLabels(
                l_address_chain_label_id=l_address_chain_label.l_address_chain_label_id,
                l_address_chain_protocol_specification_id=l_address_chain_protocol_specification.l_address_chain_protocol_specification_id
            )
            self._session.add(l_address_chain_protocol_specification_label)
            self._session.commit()
        return l_address_chain_protocol_specification_label

    def on_post(
            self,
            wallet_address: str, token_address: str,
            network_name: str, label_name: str,
            protocol_name: str, specification_name: str
    ) -> Optional[AddressChainProtocolSpecificationLabelORMSchema]:
        l_address_chain_protocol_specification_label = self._insert_l_address_chain_protocol_specification_label(
            wallet_address=wallet_address,
            pool_address=token_address,
            network_name=network_name,
            label_name=label_name,
            protocol_name=protocol_name,
            specification_name=specification_name
        )
        return AddressChainProtocolSpecificationLabelORMSchema.from_orm(l_address_chain_protocol_specification_label) if l_address_chain_protocol_specification_label else None
