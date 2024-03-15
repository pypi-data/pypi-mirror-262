from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserModel")


@_attrs_define
class UserModel:
    """
    Attributes:
        user_id (Union[Unset, int]):
        first_name (Union[None, Unset, str]):
        last_name (Union[None, Unset, str]):
        user_name (Union[None, Unset, str]):
        email (Union[None, Unset, str]):
        phone_number (Union[None, Unset, str]):
        user_roles (Union[List[str], None, Unset]):
    """

    user_id: Union[Unset, int] = UNSET
    first_name: Union[None, Unset, str] = UNSET
    last_name: Union[None, Unset, str] = UNSET
    user_name: Union[None, Unset, str] = UNSET
    email: Union[None, Unset, str] = UNSET
    phone_number: Union[None, Unset, str] = UNSET
    user_roles: Union[List[str], None, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        user_id = self.user_id

        first_name: Union[None, Unset, str]
        if isinstance(self.first_name, Unset):
            first_name = UNSET
        else:
            first_name = self.first_name

        last_name: Union[None, Unset, str]
        if isinstance(self.last_name, Unset):
            last_name = UNSET
        else:
            last_name = self.last_name

        user_name: Union[None, Unset, str]
        if isinstance(self.user_name, Unset):
            user_name = UNSET
        else:
            user_name = self.user_name

        email: Union[None, Unset, str]
        if isinstance(self.email, Unset):
            email = UNSET
        else:
            email = self.email

        phone_number: Union[None, Unset, str]
        if isinstance(self.phone_number, Unset):
            phone_number = UNSET
        else:
            phone_number = self.phone_number

        user_roles: Union[List[str], None, Unset]
        if isinstance(self.user_roles, Unset):
            user_roles = UNSET
        elif isinstance(self.user_roles, list):
            user_roles = self.user_roles

        else:
            user_roles = self.user_roles

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if user_id is not UNSET:
            field_dict["userId"] = user_id
        if first_name is not UNSET:
            field_dict["firstName"] = first_name
        if last_name is not UNSET:
            field_dict["lastName"] = last_name
        if user_name is not UNSET:
            field_dict["userName"] = user_name
        if email is not UNSET:
            field_dict["email"] = email
        if phone_number is not UNSET:
            field_dict["phoneNumber"] = phone_number
        if user_roles is not UNSET:
            field_dict["userRoles"] = user_roles

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        user_id = d.pop("userId", UNSET)

        def _parse_first_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        first_name = _parse_first_name(d.pop("firstName", UNSET))

        def _parse_last_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        last_name = _parse_last_name(d.pop("lastName", UNSET))

        def _parse_user_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        user_name = _parse_user_name(d.pop("userName", UNSET))

        def _parse_email(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        email = _parse_email(d.pop("email", UNSET))

        def _parse_phone_number(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        phone_number = _parse_phone_number(d.pop("phoneNumber", UNSET))

        def _parse_user_roles(data: object) -> Union[List[str], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                user_roles_type_0 = cast(List[str], data)

                return user_roles_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[str], None, Unset], data)

        user_roles = _parse_user_roles(d.pop("userRoles", UNSET))

        user_model = cls(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            user_name=user_name,
            email=email,
            phone_number=phone_number,
            user_roles=user_roles,
        )

        return user_model
