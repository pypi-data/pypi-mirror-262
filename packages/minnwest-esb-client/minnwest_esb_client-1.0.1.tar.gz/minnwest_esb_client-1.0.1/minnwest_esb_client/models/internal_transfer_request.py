from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.account_type import AccountType
from ..types import UNSET, Unset

T = TypeVar("T", bound="InternalTransferRequest")


@_attrs_define
class InternalTransferRequest:
    """
    Attributes:
        portfolio_name_line (Union[None, Unset, str]):
        from_account_type (Union[Unset, AccountType]):
        from_account_id (Union[None, Unset, str]):
        to_account_id (Union[None, Unset, str]):
        to_account_type (Union[Unset, AccountType]):
        amount (Union[Unset, float]):
    """

    portfolio_name_line: Union[None, Unset, str] = UNSET
    from_account_type: Union[Unset, AccountType] = UNSET
    from_account_id: Union[None, Unset, str] = UNSET
    to_account_id: Union[None, Unset, str] = UNSET
    to_account_type: Union[Unset, AccountType] = UNSET
    amount: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        portfolio_name_line: Union[None, Unset, str]
        if isinstance(self.portfolio_name_line, Unset):
            portfolio_name_line = UNSET
        else:
            portfolio_name_line = self.portfolio_name_line

        from_account_type: Union[Unset, str] = UNSET
        if not isinstance(self.from_account_type, Unset):
            from_account_type = self.from_account_type.value

        from_account_id: Union[None, Unset, str]
        if isinstance(self.from_account_id, Unset):
            from_account_id = UNSET
        else:
            from_account_id = self.from_account_id

        to_account_id: Union[None, Unset, str]
        if isinstance(self.to_account_id, Unset):
            to_account_id = UNSET
        else:
            to_account_id = self.to_account_id

        to_account_type: Union[Unset, str] = UNSET
        if not isinstance(self.to_account_type, Unset):
            to_account_type = self.to_account_type.value

        amount = self.amount

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if portfolio_name_line is not UNSET:
            field_dict["portfolioNameLine"] = portfolio_name_line
        if from_account_type is not UNSET:
            field_dict["fromAccountType"] = from_account_type
        if from_account_id is not UNSET:
            field_dict["fromAccountId"] = from_account_id
        if to_account_id is not UNSET:
            field_dict["toAccountId"] = to_account_id
        if to_account_type is not UNSET:
            field_dict["toAccountType"] = to_account_type
        if amount is not UNSET:
            field_dict["amount"] = amount

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_portfolio_name_line(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        portfolio_name_line = _parse_portfolio_name_line(d.pop("portfolioNameLine", UNSET))

        _from_account_type = d.pop("fromAccountType", UNSET)
        from_account_type: Union[Unset, AccountType]
        if isinstance(_from_account_type, Unset):
            from_account_type = UNSET
        else:
            from_account_type = AccountType(_from_account_type)

        def _parse_from_account_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        from_account_id = _parse_from_account_id(d.pop("fromAccountId", UNSET))

        def _parse_to_account_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        to_account_id = _parse_to_account_id(d.pop("toAccountId", UNSET))

        _to_account_type = d.pop("toAccountType", UNSET)
        to_account_type: Union[Unset, AccountType]
        if isinstance(_to_account_type, Unset):
            to_account_type = UNSET
        else:
            to_account_type = AccountType(_to_account_type)

        amount = d.pop("amount", UNSET)

        internal_transfer_request = cls(
            portfolio_name_line=portfolio_name_line,
            from_account_type=from_account_type,
            from_account_id=from_account_id,
            to_account_id=to_account_id,
            to_account_type=to_account_type,
            amount=amount,
        )

        return internal_transfer_request
