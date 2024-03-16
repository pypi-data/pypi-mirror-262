'''
# `chef_role`

Refer to the Terraform Registry for docs: [`chef_role`](https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/role).
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


class Role(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="chef.role.Role",
):
    '''Represents a {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/role chef_role}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        default_attributes_json: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        override_attributes_json: typing.Optional[builtins.str] = None,
        run_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/role chef_role} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/role#name Role#name}.
        :param default_attributes_json: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/role#default_attributes_json Role#default_attributes_json}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/role#description Role#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/role#id Role#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param override_attributes_json: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/role#override_attributes_json Role#override_attributes_json}.
        :param run_list: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/role#run_list Role#run_list}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__521b07a0e98680d8ba49d9f337dd27ea955cb469211a5548eec367c8dd5f16a4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = RoleConfig(
            name=name,
            default_attributes_json=default_attributes_json,
            description=description,
            id=id,
            override_attributes_json=override_attributes_json,
            run_list=run_list,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a Role resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Role to import.
        :param import_from_id: The id of the existing Role that should be imported. Refer to the {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/role#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Role to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6198e96bd58937eeb97081e7b259ac957b478d9a3c47b20681f1325bdef99c5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetDefaultAttributesJson")
    def reset_default_attributes_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultAttributesJson", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOverrideAttributesJson")
    def reset_override_attributes_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverrideAttributesJson", []))

    @jsii.member(jsii_name="resetRunList")
    def reset_run_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunList", []))

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
    @jsii.member(jsii_name="defaultAttributesJsonInput")
    def default_attributes_json_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultAttributesJsonInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="overrideAttributesJsonInput")
    def override_attributes_json_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "overrideAttributesJsonInput"))

    @builtins.property
    @jsii.member(jsii_name="runListInput")
    def run_list_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "runListInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultAttributesJson")
    def default_attributes_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultAttributesJson"))

    @default_attributes_json.setter
    def default_attributes_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfd582092a5c6c9ad4a9c1a3d0c55bbc88b8a304b45407b763cdfed278ffe700)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultAttributesJson", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3429bfc30c182a65c4bf545e27d462316b0ab2dc2bb21c09dc45768b33925b72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d81b78e830dd0d645dbd742029df5fbdd95b4e51cae2808b5374a2dd398b577)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f54dc8b0d6a30a6f50ea0caed069e7e8f94f58988c004166babc04f7cd8c164)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="overrideAttributesJson")
    def override_attributes_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "overrideAttributesJson"))

    @override_attributes_json.setter
    def override_attributes_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4235a0f135daae371fc71e3f91d4a8785a12191b63c94f325dcc5a94ba12d3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overrideAttributesJson", value)

    @builtins.property
    @jsii.member(jsii_name="runList")
    def run_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "runList"))

    @run_list.setter
    def run_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ebaf15bce5cbb12167fdebc8b8174670e83aa552b0e0eba3dc7c058242c0b43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runList", value)


@jsii.data_type(
    jsii_type="chef.role.RoleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "default_attributes_json": "defaultAttributesJson",
        "description": "description",
        "id": "id",
        "override_attributes_json": "overrideAttributesJson",
        "run_list": "runList",
    },
)
class RoleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        name: builtins.str,
        default_attributes_json: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        override_attributes_json: typing.Optional[builtins.str] = None,
        run_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/role#name Role#name}.
        :param default_attributes_json: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/role#default_attributes_json Role#default_attributes_json}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/role#description Role#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/role#id Role#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param override_attributes_json: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/role#override_attributes_json Role#override_attributes_json}.
        :param run_list: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/role#run_list Role#run_list}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3208bd1c32e444216870d00468ee5d8d6739aca4dad482c6f3524319134147d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument default_attributes_json", value=default_attributes_json, expected_type=type_hints["default_attributes_json"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument override_attributes_json", value=override_attributes_json, expected_type=type_hints["override_attributes_json"])
            check_type(argname="argument run_list", value=run_list, expected_type=type_hints["run_list"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if default_attributes_json is not None:
            self._values["default_attributes_json"] = default_attributes_json
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if override_attributes_json is not None:
            self._values["override_attributes_json"] = override_attributes_json
        if run_list is not None:
            self._values["run_list"] = run_list

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/role#name Role#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_attributes_json(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/role#default_attributes_json Role#default_attributes_json}.'''
        result = self._values.get("default_attributes_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/role#description Role#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/role#id Role#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def override_attributes_json(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/role#override_attributes_json Role#override_attributes_json}.'''
        result = self._values.get("override_attributes_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def run_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/role#run_list Role#run_list}.'''
        result = self._values.get("run_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RoleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Role",
    "RoleConfig",
]

publication.publish()

def _typecheckingstub__521b07a0e98680d8ba49d9f337dd27ea955cb469211a5548eec367c8dd5f16a4(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    default_attributes_json: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    override_attributes_json: typing.Optional[builtins.str] = None,
    run_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6198e96bd58937eeb97081e7b259ac957b478d9a3c47b20681f1325bdef99c5(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfd582092a5c6c9ad4a9c1a3d0c55bbc88b8a304b45407b763cdfed278ffe700(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3429bfc30c182a65c4bf545e27d462316b0ab2dc2bb21c09dc45768b33925b72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d81b78e830dd0d645dbd742029df5fbdd95b4e51cae2808b5374a2dd398b577(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f54dc8b0d6a30a6f50ea0caed069e7e8f94f58988c004166babc04f7cd8c164(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4235a0f135daae371fc71e3f91d4a8785a12191b63c94f325dcc5a94ba12d3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ebaf15bce5cbb12167fdebc8b8174670e83aa552b0e0eba3dc7c058242c0b43(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3208bd1c32e444216870d00468ee5d8d6739aca4dad482c6f3524319134147d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    default_attributes_json: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    override_attributes_json: typing.Optional[builtins.str] = None,
    run_list: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
