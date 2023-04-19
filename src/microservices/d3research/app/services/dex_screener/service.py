from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Optional
from cryptography import fernet

from app.schemas.dex_screener.schema import (
    AddressChainProtocolSpecificationORMSchema
)
from app.orm.cfg.engine import ORMSettings
from app.cfg.settings import settings
from app.orm import base


class DexScreenerService:

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

    def _hash_by_fernet(self, value: str) -> str:
        return self._fn.encrypt(value.encode()).decode()

    def on_post(
            self,
            pool_address: str, network_name: str,
            protocol_name: str, specification_name: str,
            is_reverse: bool
    ) -> Optional[AddressChainProtocolSpecificationORMSchema]:
        l_address_chain_protocol_specification = self._insert_l_address_chain_protocol_specification(
            address_name=pool_address,
            network_name=network_name,
            protocol_name=protocol_name,
            specification_name=specification_name
        )
        if l_address_chain_protocol_specification:
            s_is_reverse = base.sIsReverse(
                l_address_chain_protocol_specification_id=l_address_chain_protocol_specification.l_address_chain_protocol_specification_id,
                s_is_reverse=is_reverse
            )
            self._session.add(s_is_reverse)
            self._session.commit()
        return AddressChainProtocolSpecificationORMSchema.from_orm(l_address_chain_protocol_specification) if l_address_chain_protocol_specification else None
