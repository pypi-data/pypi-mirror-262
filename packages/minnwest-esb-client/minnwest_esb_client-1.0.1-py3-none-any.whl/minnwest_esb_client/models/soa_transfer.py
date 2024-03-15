from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="SoaTransfer")


@_attrs_define
class SoaTransfer:
    """
    Attributes:
        from_account_number (Union[None, Unset, str]):
        to_account_number (Union[None, Unset, str]):
        amount (Union[None, Unset, float]):
        description (Union[None, Unset, str]):
        remaining_transfers (Union[None, Unset, str]):
        transfer_frequency_code (Union[None, Unset, int]):
    """

    from_account_number: Union[None, Unset, str] = UNSET
    to_account_number: Union[None, Unset, str] = UNSET
    amount: Union[None, Unset, float] = UNSET
    description: Union[None, Unset, str] = UNSET
    remaining_transfers: Union[None, Unset, str] = UNSET
    transfer_frequency_code: Union[None, Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        from_account_number: Union[None, Unset, str]
        if isinstance(self.from_account_number, Unset):
            from_account_number = UNSET
        else:
            from_account_number = self.from_account_number

        to_account_number: Union[None, Unset, str]
        if isinstance(self.to_account_number, Unset):
            to_account_number = UNSET
        else:
            to_account_number = self.to_account_number

        amount: Union[None, Unset, float]
        if isinstance(self.amount, Unset):
            amount = UNSET
        else:
            amount = self.amount

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        remaining_transfers: Union[None, Unset, str]
        if isinstance(self.remaining_transfers, Unset):
            remaining_transfers = UNSET
        else:
            remaining_transfers = self.remaining_transfers

        transfer_frequency_code: Union[None, Unset, int]
        if isinstance(self.transfer_frequency_code, Unset):
            transfer_frequency_code = UNSET
        else:
            transfer_frequency_code = self.transfer_frequency_code

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if from_account_number is not UNSET:
            field_dict["fromAccountNumber"] = from_account_number
        if to_account_number is not UNSET:
            field_dict["toAccountNumber"] = to_account_number
        if amount is not UNSET:
            field_dict["amount"] = amount
        if description is not UNSET:
            field_dict["description"] = description
        if remaining_transfers is not UNSET:
            field_dict["remainingTransfers"] = remaining_transfers
        if transfer_frequency_code is not UNSET:
            field_dict["transferFrequencyCode"] = transfer_frequency_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_from_account_number(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        from_account_number = _parse_from_account_number(d.pop("fromAccountNumber", UNSET))

        def _parse_to_account_number(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        to_account_number = _parse_to_account_number(d.pop("toAccountNumber", UNSET))

        def _parse_amount(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        amount = _parse_amount(d.pop("amount", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_remaining_transfers(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        remaining_transfers = _parse_remaining_transfers(d.pop("remainingTransfers", UNSET))

        def _parse_transfer_frequency_code(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        transfer_frequency_code = _parse_transfer_frequency_code(d.pop("transferFrequencyCode", UNSET))

        soa_transfer = cls(
            from_account_number=from_account_number,
            to_account_number=to_account_number,
            amount=amount,
            description=description,
            remaining_transfers=remaining_transfers,
            transfer_frequency_code=transfer_frequency_code,
        )

        return soa_transfer
