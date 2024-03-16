'''
# `provider`

Refer to the Terraform Registry for docs: [`chef`](https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class ChefProvider(
    _cdktf_9a9027ec.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="chef.provider.ChefProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs chef}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        client_name: builtins.str,
        server_url: builtins.str,
        alias: typing.Optional[builtins.str] = None,
        allow_unverified_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_material: typing.Optional[builtins.str] = None,
        private_key_pem: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs chef} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param client_name: Name of a registered client within the Chef server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs#client_name ChefProvider#client_name}
        :param server_url: URL of the root of the target Chef server or organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs#server_url ChefProvider#server_url}
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs#alias ChefProvider#alias}
        :param allow_unverified_ssl: If set, the Chef client will permit unverifiable SSL certificates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs#allow_unverified_ssl ChefProvider#allow_unverified_ssl}
        :param key_material: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs#key_material ChefProvider#key_material}.
        :param private_key_pem: PEM-formatted private key for client authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs#private_key_pem ChefProvider#private_key_pem}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9867b4d71736eab7c2b2c27ba59a8c5d4161e8f1d93cd42449b96e5982a0b2bb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = ChefProviderConfig(
            client_name=client_name,
            server_url=server_url,
            alias=alias,
            allow_unverified_ssl=allow_unverified_ssl,
            key_material=key_material,
            private_key_pem=private_key_pem,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a ChefProvider resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ChefProvider to import.
        :param import_from_id: The id of the existing ChefProvider that should be imported. Refer to the {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ChefProvider to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30af9e964b09b4a13516cea667af6546730630b52c7fef22ad123e3c4b6c4352)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="resetAllowUnverifiedSsl")
    def reset_allow_unverified_ssl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowUnverifiedSsl", []))

    @jsii.member(jsii_name="resetKeyMaterial")
    def reset_key_material(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyMaterial", []))

    @jsii.member(jsii_name="resetPrivateKeyPem")
    def reset_private_key_pem(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateKeyPem", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property
    @jsii.member(jsii_name="allowUnverifiedSslInput")
    def allow_unverified_ssl_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowUnverifiedSslInput"))

    @builtins.property
    @jsii.member(jsii_name="clientNameInput")
    def client_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientNameInput"))

    @builtins.property
    @jsii.member(jsii_name="keyMaterialInput")
    def key_material_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyMaterialInput"))

    @builtins.property
    @jsii.member(jsii_name="privateKeyPemInput")
    def private_key_pem_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyPemInput"))

    @builtins.property
    @jsii.member(jsii_name="serverUrlInput")
    def server_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c55b1e971f1a318c6c00537b9b6db012f7238d67481153462e99aa0f86a61c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value)

    @builtins.property
    @jsii.member(jsii_name="allowUnverifiedSsl")
    def allow_unverified_ssl(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowUnverifiedSsl"))

    @allow_unverified_ssl.setter
    def allow_unverified_ssl(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec2c4ba500bc86abcfb472e03b8b790bc177948f535b89bab22e8caecda21461)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowUnverifiedSsl", value)

    @builtins.property
    @jsii.member(jsii_name="clientName")
    def client_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientName"))

    @client_name.setter
    def client_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1515d6912c4ebd09ccea7973dbcf981b48bbbcb87c9386babb8d7cbdf67385f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientName", value)

    @builtins.property
    @jsii.member(jsii_name="keyMaterial")
    def key_material(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyMaterial"))

    @key_material.setter
    def key_material(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fe6629b6862d03836bbcdf785f24a7ffad42a363f224ba73c3886fb29daa852)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyMaterial", value)

    @builtins.property
    @jsii.member(jsii_name="privateKeyPem")
    def private_key_pem(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyPem"))

    @private_key_pem.setter
    def private_key_pem(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ac31d492f55c37c7c1abd343220ae877243cbc37e105b391e7ede0583b7676c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKeyPem", value)

    @builtins.property
    @jsii.member(jsii_name="serverUrl")
    def server_url(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverUrl"))

    @server_url.setter
    def server_url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54635574fef6276ae6d846d37cd5c4e3fb601824c2d6a4e266fd6b2c1622fc35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverUrl", value)


@jsii.data_type(
    jsii_type="chef.provider.ChefProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "client_name": "clientName",
        "server_url": "serverUrl",
        "alias": "alias",
        "allow_unverified_ssl": "allowUnverifiedSsl",
        "key_material": "keyMaterial",
        "private_key_pem": "privateKeyPem",
    },
)
class ChefProviderConfig:
    def __init__(
        self,
        *,
        client_name: builtins.str,
        server_url: builtins.str,
        alias: typing.Optional[builtins.str] = None,
        allow_unverified_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_material: typing.Optional[builtins.str] = None,
        private_key_pem: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_name: Name of a registered client within the Chef server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs#client_name ChefProvider#client_name}
        :param server_url: URL of the root of the target Chef server or organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs#server_url ChefProvider#server_url}
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs#alias ChefProvider#alias}
        :param allow_unverified_ssl: If set, the Chef client will permit unverifiable SSL certificates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs#allow_unverified_ssl ChefProvider#allow_unverified_ssl}
        :param key_material: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs#key_material ChefProvider#key_material}.
        :param private_key_pem: PEM-formatted private key for client authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs#private_key_pem ChefProvider#private_key_pem}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04735aaf5da97f396e06b3981827aea1c574955908fdc41e0e307105185ad42e)
            check_type(argname="argument client_name", value=client_name, expected_type=type_hints["client_name"])
            check_type(argname="argument server_url", value=server_url, expected_type=type_hints["server_url"])
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument allow_unverified_ssl", value=allow_unverified_ssl, expected_type=type_hints["allow_unverified_ssl"])
            check_type(argname="argument key_material", value=key_material, expected_type=type_hints["key_material"])
            check_type(argname="argument private_key_pem", value=private_key_pem, expected_type=type_hints["private_key_pem"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_name": client_name,
            "server_url": server_url,
        }
        if alias is not None:
            self._values["alias"] = alias
        if allow_unverified_ssl is not None:
            self._values["allow_unverified_ssl"] = allow_unverified_ssl
        if key_material is not None:
            self._values["key_material"] = key_material
        if private_key_pem is not None:
            self._values["private_key_pem"] = private_key_pem

    @builtins.property
    def client_name(self) -> builtins.str:
        '''Name of a registered client within the Chef server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs#client_name ChefProvider#client_name}
        '''
        result = self._values.get("client_name")
        assert result is not None, "Required property 'client_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server_url(self) -> builtins.str:
        '''URL of the root of the target Chef server or organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs#server_url ChefProvider#server_url}
        '''
        result = self._values.get("server_url")
        assert result is not None, "Required property 'server_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs#alias ChefProvider#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allow_unverified_ssl(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set, the Chef client will permit unverifiable SSL certificates.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs#allow_unverified_ssl ChefProvider#allow_unverified_ssl}
        '''
        result = self._values.get("allow_unverified_ssl")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key_material(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs#key_material ChefProvider#key_material}.'''
        result = self._values.get("key_material")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_key_pem(self) -> typing.Optional[builtins.str]:
        '''PEM-formatted private key for client authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs#private_key_pem ChefProvider#private_key_pem}
        '''
        result = self._values.get("private_key_pem")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChefProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ChefProvider",
    "ChefProviderConfig",
]

publication.publish()

def _typecheckingstub__9867b4d71736eab7c2b2c27ba59a8c5d4161e8f1d93cd42449b96e5982a0b2bb(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    client_name: builtins.str,
    server_url: builtins.str,
    alias: typing.Optional[builtins.str] = None,
    allow_unverified_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key_material: typing.Optional[builtins.str] = None,
    private_key_pem: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30af9e964b09b4a13516cea667af6546730630b52c7fef22ad123e3c4b6c4352(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c55b1e971f1a318c6c00537b9b6db012f7238d67481153462e99aa0f86a61c5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec2c4ba500bc86abcfb472e03b8b790bc177948f535b89bab22e8caecda21461(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1515d6912c4ebd09ccea7973dbcf981b48bbbcb87c9386babb8d7cbdf67385f7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fe6629b6862d03836bbcdf785f24a7ffad42a363f224ba73c3886fb29daa852(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ac31d492f55c37c7c1abd343220ae877243cbc37e105b391e7ede0583b7676c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54635574fef6276ae6d846d37cd5c4e3fb601824c2d6a4e266fd6b2c1622fc35(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04735aaf5da97f396e06b3981827aea1c574955908fdc41e0e307105185ad42e(
    *,
    client_name: builtins.str,
    server_url: builtins.str,
    alias: typing.Optional[builtins.str] = None,
    allow_unverified_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key_material: typing.Optional[builtins.str] = None,
    private_key_pem: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
