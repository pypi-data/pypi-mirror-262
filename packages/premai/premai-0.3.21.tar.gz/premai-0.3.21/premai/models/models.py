from typing import Dict, List, Type, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Any, NotRequired, TypedDict, TypeVar

from ..models.blank_enum import BlankEnum
from ..models.model_provider_enum import ModelProviderEnum
from ..models.model_type_enum import ModelTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="Models")


class ModelsDict(TypedDict):
    id: int
    slug: str
    model_type: NotRequired[Union[Unset, ModelTypeEnum]]
    model_provider: NotRequired[Union[BlankEnum, ModelProviderEnum, None, Unset]]
    pass


@_attrs_define
class Models:
    """
    Attributes:
        id (int):
        slug (str):
        model_type (Union[Unset, ModelTypeEnum]): * `text2text` - Text to Text
            * `text2image` - Text to Image
            * `text2vector` - Text to Vector
        model_provider (Union[BlankEnum, ModelProviderEnum, None, Unset]):
    """

    id: int
    slug: str
    model_type: Union[Unset, ModelTypeEnum] = UNSET
    model_provider: Union[BlankEnum, ModelProviderEnum, None, Unset] = UNSET

    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        slug = self.slug

        model_type: Union[Unset, str] = UNSET
        if not isinstance(self.model_type, Unset):
            model_type = self.model_type.value

        model_provider: Union[None, Unset, str]
        if isinstance(self.model_provider, Unset):
            model_provider = UNSET
        elif isinstance(self.model_provider, ModelProviderEnum):
            model_provider = self.model_provider.value
        elif isinstance(self.model_provider, BlankEnum):
            model_provider = self.model_provider.value
        else:
            model_provider = self.model_provider

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "slug": slug,
            }
        )
        if model_type is not UNSET:
            field_dict["model_type"] = model_type
        if model_provider is not UNSET:
            field_dict["model_provider"] = model_provider

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy() if src_dict else {}
        id = d.pop("id")

        slug = d.pop("slug")

        _model_type = d.pop("model_type", UNSET)
        model_type: Union[Unset, ModelTypeEnum]
        if isinstance(_model_type, Unset):
            model_type = UNSET
        else:
            model_type = ModelTypeEnum(_model_type)

        def _parse_model_provider(data: object) -> Union[BlankEnum, ModelProviderEnum, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                model_provider_type_0 = ModelProviderEnum(data)

                return model_provider_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                model_provider_type_1 = BlankEnum(data)

                return model_provider_type_1
            except:  # noqa: E722
                pass
            return cast(Union[BlankEnum, ModelProviderEnum, None, Unset], data)

        model_provider = _parse_model_provider(d.pop("model_provider", UNSET))

        models = cls(
            id=id,
            slug=slug,
            model_type=model_type,
            model_provider=model_provider,
        )

        models.additional_properties = d
        return models

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
