from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

from ..models.account_type import AccountType

T = TypeVar("T", bound="AccountEStatementEnrollment")


@_attrs_define
class AccountEStatementEnrollment:
    """
    Attributes:
        account_number (str):
        account_type (AccountType):
        enroll (bool):
    """

    account_number: str
    account_type: AccountType
    enroll: bool

    def to_dict(self) -> Dict[str, Any]:
        account_number = self.account_number

        account_type = self.account_type.value

        enroll = self.enroll

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "accountNumber": account_number,
                "accountType": account_type,
                "enroll": enroll,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        account_number = d.pop("accountNumber")

        account_type = AccountType(d.pop("accountType"))

        enroll = d.pop("enroll")

        account_e_statement_enrollment = cls(
            account_number=account_number,
            account_type=account_type,
            enroll=enroll,
        )

        return account_e_statement_enrollment
