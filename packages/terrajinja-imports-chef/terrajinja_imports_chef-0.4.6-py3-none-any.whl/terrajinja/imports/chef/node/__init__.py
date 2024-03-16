'''
# `chef_node`

Refer to the Terraform Registry for docs: [`chef_node`](https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node).
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


class Node(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="chef.node.Node",
):
    '''Represents a {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node chef_node}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        automatic_attributes_json: typing.Optional[builtins.str] = None,
        client_name: typing.Optional[builtins.str] = None,
        default_attributes_json: typing.Optional[builtins.str] = None,
        environment_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        key_material: typing.Optional[builtins.str] = None,
        normal_attributes_json: typing.Optional[builtins.str] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node chef_node} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node#name Node#name}.
        :param automatic_attributes_json: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node#automatic_attributes_json Node#automatic_attributes_json}.
        :param client_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node#client_name Node#client_name}.
        :param default_attributes_json: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node#default_attributes_json Node#default_attributes_json}.
        :param environment_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node#environment_name Node#environment_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node#id Node#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param key_material: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node#key_material Node#key_material}.
        :param normal_attributes_json: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node#normal_attributes_json Node#normal_attributes_json}.
        :param override_attributes_json: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node#override_attributes_json Node#override_attributes_json}.
        :param run_list: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node#run_list Node#run_list}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d31dc1fad4271346543157ca0ee952179446df500e022fd5299f639eb550899)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NodeConfig(
            name=name,
            automatic_attributes_json=automatic_attributes_json,
            client_name=client_name,
            default_attributes_json=default_attributes_json,
            environment_name=environment_name,
            id=id,
            key_material=key_material,
            normal_attributes_json=normal_attributes_json,
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
        '''Generates CDKTF code for importing a Node resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Node to import.
        :param import_from_id: The id of the existing Node that should be imported. Refer to the {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Node to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3034c5ac9f4e5011d99fed707ba7fd2c8e105dfc071b868bab65445359ca167f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAutomaticAttributesJson")
    def reset_automatic_attributes_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomaticAttributesJson", []))

    @jsii.member(jsii_name="resetClientName")
    def reset_client_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientName", []))

    @jsii.member(jsii_name="resetDefaultAttributesJson")
    def reset_default_attributes_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultAttributesJson", []))

    @jsii.member(jsii_name="resetEnvironmentName")
    def reset_environment_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironmentName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKeyMaterial")
    def reset_key_material(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyMaterial", []))

    @jsii.member(jsii_name="resetNormalAttributesJson")
    def reset_normal_attributes_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNormalAttributesJson", []))

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
    @jsii.member(jsii_name="automaticAttributesJsonInput")
    def automatic_attributes_json_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "automaticAttributesJsonInput"))

    @builtins.property
    @jsii.member(jsii_name="clientNameInput")
    def client_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientNameInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultAttributesJsonInput")
    def default_attributes_json_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultAttributesJsonInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentNameInput")
    def environment_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "environmentNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="keyMaterialInput")
    def key_material_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyMaterialInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="normalAttributesJsonInput")
    def normal_attributes_json_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "normalAttributesJsonInput"))

    @builtins.property
    @jsii.member(jsii_name="overrideAttributesJsonInput")
    def override_attributes_json_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "overrideAttributesJsonInput"))

    @builtins.property
    @jsii.member(jsii_name="runListInput")
    def run_list_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "runListInput"))

    @builtins.property
    @jsii.member(jsii_name="automaticAttributesJson")
    def automatic_attributes_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "automaticAttributesJson"))

    @automatic_attributes_json.setter
    def automatic_attributes_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6250f87a38116575b5a39ecf6069af615934a08794a68abf1692eae473fd7dd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "automaticAttributesJson", value)

    @builtins.property
    @jsii.member(jsii_name="clientName")
    def client_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientName"))

    @client_name.setter
    def client_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64f5a30be45ead49e401698d2d6e9deca9cdc1ba0c5f8ab7350e8fdee1aef702)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientName", value)

    @builtins.property
    @jsii.member(jsii_name="defaultAttributesJson")
    def default_attributes_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultAttributesJson"))

    @default_attributes_json.setter
    def default_attributes_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__309708a9d0d64747ac150ff89dfe9af2549828d35161982611a6cf7c5ede90d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultAttributesJson", value)

    @builtins.property
    @jsii.member(jsii_name="environmentName")
    def environment_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "environmentName"))

    @environment_name.setter
    def environment_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2b637ad0fa22c33d1aba9a8cd0ec93079c8232816cb91000eb16cdbfc99e0c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentName", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d323890dae3c2cdfc0658ebeec3df1f8a1c21932fd3c2a921c29600cc65c5aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="keyMaterial")
    def key_material(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyMaterial"))

    @key_material.setter
    def key_material(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09122177eade5f0831e30f3153f80f3e7254495a2b7d800e2901a04b12676726)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyMaterial", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29977e3022d91767d2abf5b74f975c46e567f404ff78f174faebcc66e9642f2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="normalAttributesJson")
    def normal_attributes_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "normalAttributesJson"))

    @normal_attributes_json.setter
    def normal_attributes_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2469a4f1e350d975dad6c16f1345a134db82b91c58462e4b2b75a93c63dcb4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "normalAttributesJson", value)

    @builtins.property
    @jsii.member(jsii_name="overrideAttributesJson")
    def override_attributes_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "overrideAttributesJson"))

    @override_attributes_json.setter
    def override_attributes_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b74646f161723b6d1e7be6db99e9a8d262a544a173e8bc984115769f23e966e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overrideAttributesJson", value)

    @builtins.property
    @jsii.member(jsii_name="runList")
    def run_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "runList"))

    @run_list.setter
    def run_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2634b3924175d53bf302e61b2860b2c4ee1d2fbc36ae72d591c211719383b4e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runList", value)


@jsii.data_type(
    jsii_type="chef.node.NodeConfig",
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
        "automatic_attributes_json": "automaticAttributesJson",
        "client_name": "clientName",
        "default_attributes_json": "defaultAttributesJson",
        "environment_name": "environmentName",
        "id": "id",
        "key_material": "keyMaterial",
        "normal_attributes_json": "normalAttributesJson",
        "override_attributes_json": "overrideAttributesJson",
        "run_list": "runList",
    },
)
class NodeConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        automatic_attributes_json: typing.Optional[builtins.str] = None,
        client_name: typing.Optional[builtins.str] = None,
        default_attributes_json: typing.Optional[builtins.str] = None,
        environment_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        key_material: typing.Optional[builtins.str] = None,
        normal_attributes_json: typing.Optional[builtins.str] = None,
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
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node#name Node#name}.
        :param automatic_attributes_json: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node#automatic_attributes_json Node#automatic_attributes_json}.
        :param client_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node#client_name Node#client_name}.
        :param default_attributes_json: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node#default_attributes_json Node#default_attributes_json}.
        :param environment_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node#environment_name Node#environment_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node#id Node#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param key_material: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node#key_material Node#key_material}.
        :param normal_attributes_json: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node#normal_attributes_json Node#normal_attributes_json}.
        :param override_attributes_json: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node#override_attributes_json Node#override_attributes_json}.
        :param run_list: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node#run_list Node#run_list}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__816895085818cf9bb408f9443624403ba208af6eaa092231f6ac7d3abdfac85b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument automatic_attributes_json", value=automatic_attributes_json, expected_type=type_hints["automatic_attributes_json"])
            check_type(argname="argument client_name", value=client_name, expected_type=type_hints["client_name"])
            check_type(argname="argument default_attributes_json", value=default_attributes_json, expected_type=type_hints["default_attributes_json"])
            check_type(argname="argument environment_name", value=environment_name, expected_type=type_hints["environment_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument key_material", value=key_material, expected_type=type_hints["key_material"])
            check_type(argname="argument normal_attributes_json", value=normal_attributes_json, expected_type=type_hints["normal_attributes_json"])
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
        if automatic_attributes_json is not None:
            self._values["automatic_attributes_json"] = automatic_attributes_json
        if client_name is not None:
            self._values["client_name"] = client_name
        if default_attributes_json is not None:
            self._values["default_attributes_json"] = default_attributes_json
        if environment_name is not None:
            self._values["environment_name"] = environment_name
        if id is not None:
            self._values["id"] = id
        if key_material is not None:
            self._values["key_material"] = key_material
        if normal_attributes_json is not None:
            self._values["normal_attributes_json"] = normal_attributes_json
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node#name Node#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def automatic_attributes_json(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node#automatic_attributes_json Node#automatic_attributes_json}.'''
        result = self._values.get("automatic_attributes_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node#client_name Node#client_name}.'''
        result = self._values.get("client_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_attributes_json(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node#default_attributes_json Node#default_attributes_json}.'''
        result = self._values.get("default_attributes_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node#environment_name Node#environment_name}.'''
        result = self._values.get("environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node#id Node#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_material(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node#key_material Node#key_material}.'''
        result = self._values.get("key_material")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def normal_attributes_json(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node#normal_attributes_json Node#normal_attributes_json}.'''
        result = self._values.get("normal_attributes_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def override_attributes_json(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node#override_attributes_json Node#override_attributes_json}.'''
        result = self._values.get("override_attributes_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def run_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/dbresson/chef/0.4.6/docs/resources/node#run_list Node#run_list}.'''
        result = self._values.get("run_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NodeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Node",
    "NodeConfig",
]

publication.publish()

def _typecheckingstub__5d31dc1fad4271346543157ca0ee952179446df500e022fd5299f639eb550899(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    automatic_attributes_json: typing.Optional[builtins.str] = None,
    client_name: typing.Optional[builtins.str] = None,
    default_attributes_json: typing.Optional[builtins.str] = None,
    environment_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    key_material: typing.Optional[builtins.str] = None,
    normal_attributes_json: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__3034c5ac9f4e5011d99fed707ba7fd2c8e105dfc071b868bab65445359ca167f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6250f87a38116575b5a39ecf6069af615934a08794a68abf1692eae473fd7dd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64f5a30be45ead49e401698d2d6e9deca9cdc1ba0c5f8ab7350e8fdee1aef702(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__309708a9d0d64747ac150ff89dfe9af2549828d35161982611a6cf7c5ede90d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2b637ad0fa22c33d1aba9a8cd0ec93079c8232816cb91000eb16cdbfc99e0c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d323890dae3c2cdfc0658ebeec3df1f8a1c21932fd3c2a921c29600cc65c5aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09122177eade5f0831e30f3153f80f3e7254495a2b7d800e2901a04b12676726(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29977e3022d91767d2abf5b74f975c46e567f404ff78f174faebcc66e9642f2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2469a4f1e350d975dad6c16f1345a134db82b91c58462e4b2b75a93c63dcb4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b74646f161723b6d1e7be6db99e9a8d262a544a173e8bc984115769f23e966e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2634b3924175d53bf302e61b2860b2c4ee1d2fbc36ae72d591c211719383b4e0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__816895085818cf9bb408f9443624403ba208af6eaa092231f6ac7d3abdfac85b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    automatic_attributes_json: typing.Optional[builtins.str] = None,
    client_name: typing.Optional[builtins.str] = None,
    default_attributes_json: typing.Optional[builtins.str] = None,
    environment_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    key_material: typing.Optional[builtins.str] = None,
    normal_attributes_json: typing.Optional[builtins.str] = None,
    override_attributes_json: typing.Optional[builtins.str] = None,
    run_list: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
