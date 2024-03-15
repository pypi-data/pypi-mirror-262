from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.soa_transfer import SoaTransfer


T = TypeVar("T", bound="SoaAccount")


@_attrs_define
class SoaAccount:
    """
    Attributes:
        account_number (Union[None, Unset, str]):
        current_balance (Union[Unset, float]):
        transfers_list (Union[List['SoaTransfer'], None, Unset]):
    """

    account_number: Union[None, Unset, str] = UNSET
    current_balance: Union[Unset, float] = UNSET
    transfers_list: Union[List["SoaTransfer"], None, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        account_number: Union[None, Unset, str]
        if isinstance(self.account_number, Unset):
            account_number = UNSET
        else:
            account_number = self.account_number

        current_balance = self.current_balance

        transfers_list: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.transfers_list, Unset):
            transfers_list = UNSET
        elif isinstance(self.transfers_list, list):
            transfers_list = []
            for transfers_list_type_0_item_data in self.transfers_list:
                transfers_list_type_0_item = transfers_list_type_0_item_data.to_dict()
                transfers_list.append(transfers_list_type_0_item)

        else:
            transfers_list = self.transfers_list

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if account_number is not UNSET:
            field_dict["accountNumber"] = account_number
        if current_balance is not UNSET:
            field_dict["currentBalance"] = current_balance
        if transfers_list is not UNSET:
            field_dict["transfersList"] = transfers_list

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.soa_transfer import SoaTransfer

        d = src_dict.copy()

        def _parse_account_number(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        account_number = _parse_account_number(d.pop("accountNumber", UNSET))

        current_balance = d.pop("currentBalance", UNSET)

        def _parse_transfers_list(data: object) -> Union[List["SoaTransfer"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                transfers_list_type_0 = []
                _transfers_list_type_0 = data
                for transfers_list_type_0_item_data in _transfers_list_type_0:
                    transfers_list_type_0_item = SoaTransfer.from_dict(transfers_list_type_0_item_data)

                    transfers_list_type_0.append(transfers_list_type_0_item)

                return transfers_list_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["SoaTransfer"], None, Unset], data)

        transfers_list = _parse_transfers_list(d.pop("transfersList", UNSET))

        soa_account = cls(
            account_number=account_number,
            current_balance=current_balance,
            transfers_list=transfers_list,
        )

        return soa_account
