from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict
import datetime as dt
from typing import Optional
from enum import Enum
import io
import base58
from ccdefundamentals.GRPCClient import GRPCClient
from ccdefundamentals.GRPCClient.CCD_Types import *  # noqa: F403
from ccdefundamentals.enums import NET
from rich.console import Console

# import math
import leb128

console = Console()

LEN_ACCOUNT_ADDRESS = 50


# Metadata classes
class TokenAttribute(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    type: Optional[str] = None
    name: Optional[str] = None
    value: Optional[str] = None


class TokenURLJSON(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    url: Optional[str] = None
    hash: Optional[str] = None


class TokenMetaData(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    name: Optional[str] = None
    symbol: Optional[str] = None
    unique: Optional[bool] = None
    decimals: Optional[int] = None
    description: Optional[str] = None
    thumbnail: Optional[TokenURLJSON] = None
    display: Optional[TokenURLJSON] = None
    artifact: Optional[TokenURLJSON] = None
    assets: Optional[list[TokenMetaData]] = None
    attributes: Optional[list[TokenAttribute]] = None
    localization: Optional[dict[str, TokenURLJSON]] = None


# class MongoTypeTokenHolder(BaseModel):
#     account_address: CCD_AccountAddress
#     token_amount: str


class MongoTypeTokenForAddress(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    token_address: str
    contract: str
    token_id: str
    token_amount: str


class MongoTypeTokenLink(BaseModel):
    id: str = Field(..., alias="_id")
    account_address: Optional[str] = None
    account_address_canonical: Optional[str] = None
    token_holding: Optional[MongoTypeTokenForAddress] = None


class MongoTypeTokenHolderAddress(BaseModel):
    id: str = Field(..., alias="_id")
    account_address_canonical: Optional[str] = None
    tokens: dict[str, MongoTypeTokenForAddress]


class MongoTypeLoggedEvent(BaseModel):
    id: str = Field(..., alias="_id")
    logged_event: str
    result: dict
    tag: int
    event_type: str
    block_height: int
    slot_time: Optional[dt.datetime] = None
    tx_index: int  #####################################################################
    ordering: int
    tx_hash: str
    token_address: str
    contract: str
    date: Optional[str] = None


class MongoTypeTokensTag(BaseModel):
    id: str = Field(..., alias="_id")
    contracts: list[str]
    tag_template: Optional[bool] = None
    single_use_contract: Optional[bool] = None
    logo_url: Optional[str] = None
    decimals: Optional[int] = None
    exchange_rate: Optional[float] = None
    logged_events_count: Optional[int] = None
    owner: Optional[str] = None
    module_name: Optional[str] = None
    token_type: Optional[str] = None
    display_name: Optional[str] = None
    tvl_for_token_in_usd: Optional[float] = None


class FailedAttempt(BaseModel):
    attempts: int
    do_not_try_before: dt.datetime
    last_error: str


class MongoTypeTokenAddress(BaseModel):
    id: str = Field(..., alias="_id")
    contract: str
    token_id: str
    token_amount: Optional[str] = None
    metadata_url: Optional[str] = None
    last_height_processed: int
    token_holders: Optional[dict[str, str]] = None
    tag_information: Optional[MongoTypeTokensTag] = None
    exchange_rate: Optional[float] = None
    domain_name: Optional[str] = None
    token_metadata: Optional[TokenMetaData] = None
    failed_attempt: Optional[FailedAttempt] = None
    hidden: Optional[bool] = None


# CIS
class StandardIdentifiers(Enum):
    CIS_0 = "CIS-0"
    CIS_1 = "CIS-1"
    CIS_2 = "CIS-2"
    CIS_3 = "CIS-3"
    CIS_4 = "CIS-4"


class LoggedEvents(Enum):
    transfer_event = 255
    mint_event = 254
    burn_event = 253
    operator_event = 252
    metadata_event = 251
    nonce_event = 250
    register_credential_event = 249
    revoke_credential_event = 248
    issuer_metadata_event = 247
    credential_metadata_event = 246
    credential_schemaref_event = 245
    recovation_key_event = 244


# CIS-2 Logged Event Types


class transferEvent(BaseModel):
    tag: int
    token_id: Optional[str] = None
    token_amount: Optional[int] = None
    from_address: Optional[str] = None
    to_address: Optional[str] = None


class mintEvent(BaseModel):
    tag: int
    token_id: Optional[str] = None
    token_amount: Optional[int] = None
    to_address: Optional[str] = None


class burnEvent(BaseModel):
    tag: int
    token_id: Optional[str] = None
    token_amount: Optional[int] = None
    from_address: Optional[str] = None


class updateOperatorEvent(BaseModel):
    tag: int
    operator_update: Optional[str] = None
    owner: Optional[str] = None
    operator: Optional[str] = None


class SchemaRef(BaseModel):
    url: str
    checksum: Optional[str] = None


class registerCredentialEvent(BaseModel):
    tag: int
    credential_id: Optional[str] = None
    schema_ref: Optional[SchemaRef] = None
    credential_type: Optional[str] = None


class revokeCredentialEvent(BaseModel):
    tag: int
    credential_id: Optional[str] = None
    revoker: Optional[str] = None
    reason: Optional[str] = None


class issuerMetadataEvent(BaseModel):
    tag: int
    metadata: MetadataUrl


class credentialMetadataEvent(BaseModel):
    tag: int
    id: str  # credentialHolderId
    metadata: MetadataUrl


class credentialSchemaRefEvent(BaseModel):
    tag: int
    type: Optional[str] = None
    schema_ref: Optional[str] = None


class revocationKeyEvent(BaseModel):
    tag: int
    action: Optional[str] = None


class MetadataUrl(BaseModel):
    url: str
    checksum: Optional[str] = None


class tokenMetadataEvent(BaseModel):
    tag: int
    token_id: str
    metadata: MetadataUrl


class nonceEvent(BaseModel):
    tag: int
    nonce: Optional[int] = None
    sponsoree: Optional[str] = None


class CIS:
    def __init__(
        self,
        grpcclient: GRPCClient = None,
        instance_index=None,
        instance_subindex=None,
        entrypoint=None,
        net: NET.MAINNET = None,
    ):
        self.grpcclient = grpcclient
        self.instance_index = instance_index
        self.instance_subindex = instance_subindex
        self.entrypoint = entrypoint
        self.net = net

    def standard_identifier(self, identifier: StandardIdentifiers) -> bytes:
        si = io.BytesIO()
        # write the length of ASCII characters for the identifier
        number = len(identifier.value)
        byte_array = number.to_bytes(1, "little")
        si.write(byte_array)
        # write the identifier
        si.write(bytes(identifier.value, encoding="ASCII"))
        # convert to bytes
        return si.getvalue()

    def supports_parameter(self, standard_identifier: StandardIdentifiers) -> bytes:
        sp = io.BytesIO()
        # write the number of standardIdentifiers present
        number = 1
        byte_array = number.to_bytes(2, "little")
        sp.write(byte_array)
        # write the standardIdentifier
        sp.write(self.standard_identifier(standard_identifier))
        # convert to bytes
        return sp.getvalue()

    def support_result(self, bs: io.BytesIO):
        t = int.from_bytes(bs.read(2), byteorder="little")
        if t == 0:
            return t, "Standard is not supported"
        elif t == 1:
            return t, "Standard is supported by this contract"
        elif t == 2:
            contracts = []
            n = int.from_bytes(bs.read(1), byteorder="little")
            for _ in range(n):
                contracts.append(self.contract_address(bs))
                return (
                    t,
                    "Standard is supported by using one of these contract addresses: "
                    + [x for x in contracts],
                )

    def supports_response(self, res: bytes):
        bs = io.BytesIO(bytes.fromhex(res.decode()))
        if bs.getbuffer().nbytes > 0:
            n = int.from_bytes(bs.read(2), byteorder="big")
            responses = []
            for _ in range(n):
                responses.append(self.support_result(bs))
            if len(responses) > 0:
                return responses[0]
            else:
                return False, "Lookup Failure"
        else:
            return False, "Lookup Failure"

    def supports_standard(self, standard_identifier: StandardIdentifiers) -> bool:
        parameter_bytes = self.supports_parameter(standard_identifier)

        ii = self.grpcclient.invoke_instance(
            "last_final",
            self.instance_index,
            self.instance_subindex,
            self.entrypoint,
            parameter_bytes,
            self.net,
        )

        res = ii.success.return_value
        support_result, support_result_text = self.supports_response(res)

        return support_result == 1

    def supports_standards(
        self, standard_identifiers: list[StandardIdentifiers]
    ) -> bool:
        support = False
        for si in standard_identifiers:
            parameter_bytes = self.supports_parameter(si)

            ii = self.grpcclient.invoke_instance(
                "last_final",
                self.instance_index,
                self.instance_subindex,
                self.entrypoint,
                parameter_bytes,
                self.net,
            )

            res = ii.success.return_value
            support_result, support_result_text = self.supports_response(res)

            support = support_result == 1
        return support

    def balanceOf(self, block_hash: str, tokenID: str, account_id: str):
        parameter_bytes = self.balanceOfParameter(tokenID, account_id)

        ii = self.grpcclient.invoke_instance(
            block_hash,
            self.instance_index,
            self.instance_subindex,
            self.entrypoint,
            parameter_bytes,
            self.net,
        )

        res = ii.success.return_value
        support_result = self.balanceOfResponse(res)

        return support_result, ii

    def account_address(self, bs: io.BytesIO):
        addr = bs.read(32)
        return base58.b58encode_check(b"\x01" + addr).decode()

    def contract_address(self, bs: io.BytesIO):
        return int.from_bytes(bs.read(8), byteorder="little"), int.from_bytes(
            bs.read(8), byteorder="little"
        )

    def address(self, bs: io.BytesIO):
        t = int.from_bytes(bs.read(1), byteorder="little")
        if t == 0:
            return self.account_address(bs)
        elif t == 1:
            return self.contract_address(bs)
        else:
            raise Exception("invalid type")

    def receiver(self, bs: io.BytesIO):
        t = int.from_bytes(bs.read(1), byteorder="little")
        if t == 0:
            return self.account_address(bs)
        elif t == 1:
            return self.contract_address(bs), self.receiveHookName(bs)
        else:
            raise Exception("invalid type")

    def url(self, n: int, bs: io.BytesIO):
        data = bs.read(n)
        return data

    def metadataChecksum(self, bs: io.BytesIO):
        t = int.from_bytes(bs.read(1), byteorder="little")
        if t == 0:
            return None
        elif t == 1:
            return bs.read(32)
        else:
            raise Exception("invalid type")

    def metadataUrl(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(2), byteorder="little")
        url = bs.read(n).decode()
        # checksum = self.metadataChecksum(bs)
        return MetadataUrl(**{"url": url, "checksum": None})

    def schema_ref(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(2), byteorder="little")
        url = bs.read(n).decode()
        return SchemaRef(**{"url": url, "checksum": None})

    def receiveHookName(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(2), byteorder="little")
        name = bs.read(n)
        return bytes.decode(name, "UTF-8")

    def additionalData(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(2), byteorder="little")
        data = bs.read(n)
        return data

    def tokenID(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(1), byteorder="little")
        return bytes.hex(bs.read(n))

    def balanceOfQuery(self, tokenID: str, address: str):
        sp = io.BytesIO()

        tokenID = self.generate_tokenID(tokenID)
        address = self.generate_address(address)
        sp.write(tokenID)
        sp.write(address)
        return sp.getvalue()

    def balanceOfParameter(self, tokenID: str, address: str):
        sp = io.BytesIO()

        sp.write(int(1).to_bytes(2, "little"))
        sp.write(self.balanceOfQuery(tokenID, address))
        # convert to bytes
        return sp.getvalue()

    def balanceOfResponse(self, res: bytes):
        bs = io.BytesIO(bytes.fromhex(res.decode()))
        n = int.from_bytes(bs.read(2), byteorder="little")
        print(n)
        result = self.token_amount(bs)

        return result

    def generate_tokenID(self, tokenID: str):
        sp = io.BytesIO()
        tokenID_in_bytes = bytes.fromhex(tokenID)
        sp.write(int(len(tokenID_in_bytes)).to_bytes(1, "little"))
        sp.write(tokenID_in_bytes)
        return sp.getvalue()

    def generate_account_address(self, address: str):
        return bytearray(base58.b58decode_check(address)[1:])

    def generate_contract_address(self, address: str):
        # TODO
        sp = io.BytesIO()

        address_in_bytes = bytes.fromhex(address.encode("utf-8"))

        sp.write(address_in_bytes)
        return sp.getvalue()

    def generate_address(self, address: str):
        sp = io.BytesIO()

        if len(address) == 50:
            sp.write(int(0).to_bytes(1, "little"))
            sp.write(self.generate_account_address(address))
        else:
            sp.write(int(1).to_bytes(1, "little"))
            sp.write(self.generate_contract_address(address))

        return sp.getvalue()

    def invoke_token_metadataUrl(self, tokenID: str) -> bool:
        parameter_bytes = self.tokenMetadataParameter(tokenID)

        ii = self.grpcclient.invoke_instance(
            "last_final",
            self.instance_index,
            self.instance_subindex,
            self.entrypoint,
            parameter_bytes,
            self.net,
        )

        res = ii.success.return_value
        return self.tokenMetadataResultParameter(res)

    def viewOwnerHistoryRequest(self, tokenID: str):
        return self.generate_tokenID(tokenID)

    def viewOwnerHistoryResponse(self, res: bytes):
        bs = io.BytesIO(bytes.fromhex(res.decode()))
        n = int.from_bytes(bs.read(1), byteorder="little")
        _ = bs.read(3)  # own_str
        results = []
        for _ in range(0, n):
            results.append(self.address(bs))

        return results

    def tokenMetadataParameter(self, tokenID: str):
        sp = io.BytesIO()
        sp.write(int(1).to_bytes(2, "little"))
        sp.write(self.generate_tokenID(tokenID))
        return sp.getvalue()

    def metadata_result(self, bs: bytes):
        n = int(bs[:2].decode("ASCII"))
        bs = io.BytesIO(bs)
        bs.read(2)
        url = self.url(n, bs)
        return url

    def metadata_response(self, bs: bytes):
        # bs: io.BytesIO = io.BytesIO(bs)
        if len(bs) > 0:
            n = int(bs[:2].decode("ASCII"))
            # n = int.from_bytes(bs.read(2), byteorder="big")
            responses = []
            for _ in range(n):
                responses.append(self.metadata_result(bs))
            return responses[0]
        else:
            return False, "Lookup Failure"

    def tokenMetadataResultParameter(self, res: bytes):
        bs = io.BytesIO(bytes.fromhex(res.decode()))
        n = int.from_bytes(bs.read(2), byteorder="little")
        results = []
        for _ in range(0, n):
            results.append(self.metadataUrl(bs))

        return results

    def operator_update(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(1), byteorder="little")
        if n == 0:
            return "Remove operator"
        elif n == 1:
            return "Add operator"

    def token_id(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(1), byteorder="little")
        return bytes.hex(bs.read(n))

    def nonce(self, bs: io.BytesIO):
        return bytes.hex(bs.read(8))

    def token_amount(self, bs: io.BytesIO):
        return leb128.u.decode_reader(bs)[0]

    def credential_id(self, bs: io.BytesIO):
        return bytes.hex(bs.read(32))

    def credential_type(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(1), byteorder="little")
        return bytes.hex(bs.read(n))

    def reason_string(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(1), byteorder="little")
        return bytes.hex(bs.read(n))

    def revoker(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(1), byteorder="little")
        if n == 0:
            return "Issuer"
        elif n == 1:
            return "Holder"
        elif n == 2:
            key_ = self.credential_id(bs)
            return f"Other ({key_})"

    def optional_reason(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(1), byteorder="little")
        if n == 0:
            return None
        elif n == 2:
            reason_string_ = self.reason_string(bs)
            return reason_string_

    def revocation_key_action(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(1), byteorder="little")
        if n == 0:
            return "Register"
        elif n == 1:
            return "Remove"

    def transferEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        token_id_ = self.token_id(bs)
        amount_ = self.token_amount(bs)

        from_ = self.address(bs)
        if type(from_) is not tuple:
            # it's an account address
            if len(from_) != LEN_ACCOUNT_ADDRESS:
                return None

        if type(from_) == tuple:
            from_ = f"<{from_[0]},{from_[1]}>"
        to_ = self.address(bs)
        if type(to_) is not tuple:
            # it's an account address
            if len(to_) != LEN_ACCOUNT_ADDRESS:
                return None

        if type(to_) == tuple:
            to_ = f"<{to_[0]},{to_[1]}>"

        return transferEvent(
            **{
                "tag": tag_,
                "token_id": token_id_,
                "token_amount": amount_,
                "from_address": from_,
                "to_address": to_,
            }
        )

    def updateOperatorEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        # token_id_ = self.token_id(bs)
        update_ = self.operator_update(bs)

        owner_ = self.address(bs)
        if type(owner_) is not tuple:
            # it's an account address
            if len(owner_) != LEN_ACCOUNT_ADDRESS:
                return None

        if type(owner_) == tuple:
            owner_ = f"<{owner_[0]},{owner_[1]}>"
        operator_ = self.address(bs)
        if type(operator_) is not tuple:
            # it's an account address
            if len(operator_) != LEN_ACCOUNT_ADDRESS:
                return None

        if type(operator_) == tuple:
            operator_ = f"<{operator_[0]},{operator_[1]}>"

        return updateOperatorEvent(
            **{
                "tag": tag_,
                "operator_update": update_,
                "owner": owner_,
                "operator": operator_,
            }
        )

    def mintEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        token_id_ = self.token_id(bs)
        amount_ = self.token_amount(bs)
        to_ = self.address(bs)
        if type(to_) is not tuple:
            # it's an account address
            if len(to_) != LEN_ACCOUNT_ADDRESS:
                return None

        if type(to_) == tuple:
            to_ = f"<{to_[0]},{to_[1]}>"

        return mintEvent(
            **{
                "tag": tag_,
                "token_id": token_id_,
                "token_amount": amount_,
                "to_address": to_,
            }
        )

    def burnEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        token_id_ = self.token_id(bs)
        amount_ = self.token_amount(bs)
        from_ = self.address(bs)
        if type(from_) is not tuple:
            # it's an account address
            if len(from_) != LEN_ACCOUNT_ADDRESS:
                return None

        if type(from_) == tuple:
            from_ = f"<{from_[0]},{from_[1]}>"

        return burnEvent(
            **{
                "tag": tag_,
                "token_id": token_id_,
                "token_amount": amount_,
                "from_address": from_,
            }
        )

    def tokenMetaDataEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")

        token_id_ = self.token_id(bs)
        metadata_ = self.metadataUrl(bs)

        return tokenMetadataEvent(
            **{
                "tag": tag_,
                "token_id": token_id_,
                "metadata": metadata_,
            }
        )

    def nonceEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")

        nonce_ = self.nonce(bs)
        sponsoree_ = self.account_address(bs)

        return nonceEvent(
            **{
                "tag": tag_,
                "nonce": nonce_,
                "sponsoree": sponsoree_,
            }
        )

    def registerCredentialEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        credential_id_ = self.credential_id(bs)
        schema_ref_ = self.schema_ref(bs)
        credential_type_ = self.credential_type(bs)
        return registerCredentialEvent(
            **{
                "tag": tag_,
                "credential_id": credential_id_,
                "schema_ref": schema_ref_,
                "credential_type": credential_type_,
            }
        )

    def revokeCredentialEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        credential_id_ = self.credential_id(bs)
        revoker_ = self.revoker(bs)
        reason_ = self.optional_reason(bs)
        return revokeCredentialEvent(
            **{
                "tag": tag_,
                "credential_id": credential_id_,
                "revoker": revoker_,
                "reason": reason_,
            }
        )

    def issuerMetaDataEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        metadata_ = self.metadataUrl(bs)

        return issuerMetadataEvent(
            **{
                "tag": tag_,
                "metadata": metadata_,
            }
        )

    def credentialMetaDataEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        credential_id_ = self.credential_id(bs)
        metadata_ = self.metadataUrl(bs)

        return credentialMetadataEvent(
            **{
                "tag": tag_,
                "id": credential_id_,
                "metadata": metadata_,
            }
        )

    def credentialSchemaRefEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        schema_ref_ = self.schema_ref(bs)
        credential_type_ = self.credential_type(bs)
        return credentialSchemaRefEvent(
            **{
                "tag": tag_,
                "type": credential_type_,
                "schema_ref": schema_ref_,
            }
        )

    def revocationKeyEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        action = self.revocation_key_action(bs)

        return revocationKeyEvent(
            **{
                "tag": tag_,
                "action": action,
            }
        )

    def process_log_events(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        if tag_ == 255:
            try:
                event = self.transferEvent(hexParameter)
                return tag_, event
            except:  # noqa: E722
                return tag_, None
        elif tag_ == 254:
            try:
                event = self.mintEvent(hexParameter)
                return tag_, event
            except:  # noqa: E722
                return tag_, None
        elif tag_ == 253:
            try:
                event = self.burnEvent(hexParameter)
                return tag_, event
            except:  # noqa: E722
                return tag_, None
        elif tag_ == 252:
            try:
                event = self.updateOperatorEvent(hexParameter)
                return tag_, event
            except:  # noqa: E722
                return tag_, None
        elif tag_ == 251:
            try:
                event = self.tokenMetaDataEvent(hexParameter)
                return tag_, event
            except:  # noqa: E722
                return tag_, None
        elif tag_ == 250:
            try:
                event = self.nonceEvent(hexParameter)
                return tag_, event
            except:  # noqa: E722
                return tag_, None
        elif tag_ == 249:
            try:
                event = self.registerCredentialEvent(hexParameter)
                return tag_, event
            except:  # noqa: E722
                return tag_, None
        elif tag_ == 248:
            try:
                event = self.revokeCredentialEvent(hexParameter)
                return tag_, event
            except:  # noqa: E722
                return tag_, None
        elif tag_ == 247:
            try:
                event = self.issuerMetaDataEvent(hexParameter)
                return tag_, event
            except:  # noqa: E722
                return tag_, None
        elif tag_ == 246:
            try:
                event = self.credentialMetaDataEvent(hexParameter)
                return tag_, event
            except:  # noqa: E722
                return tag_, None
        elif tag_ == 245:
            try:
                event = self.credentialSchemaRefEvent(hexParameter)
                return tag_, event
            except:  # noqa: E722
                return tag_, None
        elif tag_ == 244:
            try:
                event = self.revocationKeyEvent(hexParameter)
                return tag_, event
            except:  # noqa: E722
                return tag_, None
        else:
            return tag_, f"Custom even with tag={tag_}."
