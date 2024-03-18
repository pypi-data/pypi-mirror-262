'''
# `data_openstack_sharedfilesystem_sharenetwork_v2`

Refer to the Terraform Registry for docs: [`data_openstack_sharedfilesystem_sharenetwork_v2`](https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2).
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


class DataOpenstackSharedfilesystemSharenetworkV2(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@ithings/cdktf-provider-openstack.dataOpenstackSharedfilesystemSharenetworkV2.DataOpenstackSharedfilesystemSharenetworkV2",
):
    '''(experimental) Represents a {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2 openstack_sharedfilesystem_sharenetwork_v2}.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ip_version: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        network_type: typing.Optional[builtins.str] = None,
        neutron_net_id: typing.Optional[builtins.str] = None,
        neutron_subnet_id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        security_service_id: typing.Optional[builtins.str] = None,
        segmentation_id: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''(experimental) Create a new {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2 openstack_sharedfilesystem_sharenetwork_v2} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param description: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2#description DataOpenstackSharedfilesystemSharenetworkV2#description}.
        :param id: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2#id DataOpenstackSharedfilesystemSharenetworkV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_version: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2#ip_version DataOpenstackSharedfilesystemSharenetworkV2#ip_version}.
        :param name: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2#name DataOpenstackSharedfilesystemSharenetworkV2#name}.
        :param network_type: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2#network_type DataOpenstackSharedfilesystemSharenetworkV2#network_type}.
        :param neutron_net_id: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2#neutron_net_id DataOpenstackSharedfilesystemSharenetworkV2#neutron_net_id}.
        :param neutron_subnet_id: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2#neutron_subnet_id DataOpenstackSharedfilesystemSharenetworkV2#neutron_subnet_id}.
        :param region: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2#region DataOpenstackSharedfilesystemSharenetworkV2#region}.
        :param security_service_id: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2#security_service_id DataOpenstackSharedfilesystemSharenetworkV2#security_service_id}.
        :param segmentation_id: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2#segmentation_id DataOpenstackSharedfilesystemSharenetworkV2#segmentation_id}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ca4380956d01e305f9f2e0401744d6533b906f5d8c065ac4fd89465bb0c7c7e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataOpenstackSharedfilesystemSharenetworkV2Config(
            description=description,
            id=id,
            ip_version=ip_version,
            name=name,
            network_type=network_type,
            neutron_net_id=neutron_net_id,
            neutron_subnet_id=neutron_subnet_id,
            region=region,
            security_service_id=security_service_id,
            segmentation_id=segmentation_id,
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
        '''(experimental) Generates CDKTF code for importing a DataOpenstackSharedfilesystemSharenetworkV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataOpenstackSharedfilesystemSharenetworkV2 to import.
        :param import_from_id: The id of the existing DataOpenstackSharedfilesystemSharenetworkV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataOpenstackSharedfilesystemSharenetworkV2 to import is found.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24f0daf183193a2b4c5a638faa44c6048a5050e91e71ef0c4d901f591c30c384)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpVersion")
    def reset_ip_version(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetIpVersion", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNetworkType")
    def reset_network_type(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetNetworkType", []))

    @jsii.member(jsii_name="resetNeutronNetId")
    def reset_neutron_net_id(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetNeutronNetId", []))

    @jsii.member(jsii_name="resetNeutronSubnetId")
    def reset_neutron_subnet_id(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetNeutronSubnetId", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSecurityServiceId")
    def reset_security_service_id(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetSecurityServiceId", []))

    @jsii.member(jsii_name="resetSegmentationId")
    def reset_segmentation_id(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetSegmentationId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="cidr")
    def cidr(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "cidr"))

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @builtins.property
    @jsii.member(jsii_name="securityServiceIds")
    def security_service_ids(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityServiceIds"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipVersionInput")
    def ip_version_input(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ipVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkTypeInput")
    def network_type_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="neutronNetIdInput")
    def neutron_net_id_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "neutronNetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="neutronSubnetIdInput")
    def neutron_subnet_id_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "neutronSubnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="securityServiceIdInput")
    def security_service_id_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityServiceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="segmentationIdInput")
    def segmentation_id_input(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "segmentationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34d86e9318ac34fb7cbfcbc21d5ab559bcf4a43eef0896998331ba639ac2fd27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__145b8c5ae4a97efb7688854fa2951507b1f6ccaa3ab50e47228a75d0f4028024)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="ipVersion")
    def ip_version(self) -> jsii.Number:
        '''
        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "ipVersion"))

    @ip_version.setter
    def ip_version(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87bff2a5cbd8297eb383f44b55756a5ae8924328bb8f82bfdd49a515561c8bcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipVersion", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e567a29262cfaa52c2591e72e6a19360d789b819412e59ee7a9ecab1d14ee4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="networkType")
    def network_type(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "networkType"))

    @network_type.setter
    def network_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__888bcb1d68f9e80aaf338ad90e86618fba8b1bd0c004287b5d7dae6fbf2e628e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkType", value)

    @builtins.property
    @jsii.member(jsii_name="neutronNetId")
    def neutron_net_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "neutronNetId"))

    @neutron_net_id.setter
    def neutron_net_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb0a8a72ea7873b383d9e081ca9bf95394d97735ce53eaa5b2278a46362eb60a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "neutronNetId", value)

    @builtins.property
    @jsii.member(jsii_name="neutronSubnetId")
    def neutron_subnet_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "neutronSubnetId"))

    @neutron_subnet_id.setter
    def neutron_subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc3c061eb21d101d204805e85de70d3417045dc3b81da8d4d78cc06bdef1cf65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "neutronSubnetId", value)

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd6943215f2bb43b5d208be6a82e4e7b60eb6fc6306038e5a9be155f961afe41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value)

    @builtins.property
    @jsii.member(jsii_name="securityServiceId")
    def security_service_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "securityServiceId"))

    @security_service_id.setter
    def security_service_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95edf401b2c876c641e990e2937c45794c508e11dcbfac0098fb8c3e472c52df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityServiceId", value)

    @builtins.property
    @jsii.member(jsii_name="segmentationId")
    def segmentation_id(self) -> jsii.Number:
        '''
        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "segmentationId"))

    @segmentation_id.setter
    def segmentation_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09a70329a8ea02a36c1786eb984402fab98a3d598ba2132ec63d0e9370a63d8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "segmentationId", value)


@jsii.data_type(
    jsii_type="@ithings/cdktf-provider-openstack.dataOpenstackSharedfilesystemSharenetworkV2.DataOpenstackSharedfilesystemSharenetworkV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "description": "description",
        "id": "id",
        "ip_version": "ipVersion",
        "name": "name",
        "network_type": "networkType",
        "neutron_net_id": "neutronNetId",
        "neutron_subnet_id": "neutronSubnetId",
        "region": "region",
        "security_service_id": "securityServiceId",
        "segmentation_id": "segmentationId",
    },
)
class DataOpenstackSharedfilesystemSharenetworkV2Config(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ip_version: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        network_type: typing.Optional[builtins.str] = None,
        neutron_net_id: typing.Optional[builtins.str] = None,
        neutron_subnet_id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        security_service_id: typing.Optional[builtins.str] = None,
        segmentation_id: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param description: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2#description DataOpenstackSharedfilesystemSharenetworkV2#description}.
        :param id: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2#id DataOpenstackSharedfilesystemSharenetworkV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_version: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2#ip_version DataOpenstackSharedfilesystemSharenetworkV2#ip_version}.
        :param name: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2#name DataOpenstackSharedfilesystemSharenetworkV2#name}.
        :param network_type: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2#network_type DataOpenstackSharedfilesystemSharenetworkV2#network_type}.
        :param neutron_net_id: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2#neutron_net_id DataOpenstackSharedfilesystemSharenetworkV2#neutron_net_id}.
        :param neutron_subnet_id: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2#neutron_subnet_id DataOpenstackSharedfilesystemSharenetworkV2#neutron_subnet_id}.
        :param region: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2#region DataOpenstackSharedfilesystemSharenetworkV2#region}.
        :param security_service_id: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2#security_service_id DataOpenstackSharedfilesystemSharenetworkV2#security_service_id}.
        :param segmentation_id: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2#segmentation_id DataOpenstackSharedfilesystemSharenetworkV2#segmentation_id}.

        :stability: experimental
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d83fc5212122113d798dd67e01bad82193e507fdd3469dd57442fb1dc95a3f1)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ip_version", value=ip_version, expected_type=type_hints["ip_version"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_type", value=network_type, expected_type=type_hints["network_type"])
            check_type(argname="argument neutron_net_id", value=neutron_net_id, expected_type=type_hints["neutron_net_id"])
            check_type(argname="argument neutron_subnet_id", value=neutron_subnet_id, expected_type=type_hints["neutron_subnet_id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument security_service_id", value=security_service_id, expected_type=type_hints["security_service_id"])
            check_type(argname="argument segmentation_id", value=segmentation_id, expected_type=type_hints["segmentation_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if ip_version is not None:
            self._values["ip_version"] = ip_version
        if name is not None:
            self._values["name"] = name
        if network_type is not None:
            self._values["network_type"] = network_type
        if neutron_net_id is not None:
            self._values["neutron_net_id"] = neutron_net_id
        if neutron_subnet_id is not None:
            self._values["neutron_subnet_id"] = neutron_subnet_id
        if region is not None:
            self._values["region"] = region
        if security_service_id is not None:
            self._values["security_service_id"] = security_service_id
        if segmentation_id is not None:
            self._values["segmentation_id"] = segmentation_id

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
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2#description DataOpenstackSharedfilesystemSharenetworkV2#description}.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2#id DataOpenstackSharedfilesystemSharenetworkV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.

        :stability: experimental
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_version(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2#ip_version DataOpenstackSharedfilesystemSharenetworkV2#ip_version}.

        :stability: experimental
        '''
        result = self._values.get("ip_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2#name DataOpenstackSharedfilesystemSharenetworkV2#name}.

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2#network_type DataOpenstackSharedfilesystemSharenetworkV2#network_type}.

        :stability: experimental
        '''
        result = self._values.get("network_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def neutron_net_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2#neutron_net_id DataOpenstackSharedfilesystemSharenetworkV2#neutron_net_id}.

        :stability: experimental
        '''
        result = self._values.get("neutron_net_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def neutron_subnet_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2#neutron_subnet_id DataOpenstackSharedfilesystemSharenetworkV2#neutron_subnet_id}.

        :stability: experimental
        '''
        result = self._values.get("neutron_subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2#region DataOpenstackSharedfilesystemSharenetworkV2#region}.

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_service_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2#security_service_id DataOpenstackSharedfilesystemSharenetworkV2#security_service_id}.

        :stability: experimental
        '''
        result = self._values.get("security_service_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def segmentation_id(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/data-sources/sharedfilesystem_sharenetwork_v2#segmentation_id DataOpenstackSharedfilesystemSharenetworkV2#segmentation_id}.

        :stability: experimental
        '''
        result = self._values.get("segmentation_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpenstackSharedfilesystemSharenetworkV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataOpenstackSharedfilesystemSharenetworkV2",
    "DataOpenstackSharedfilesystemSharenetworkV2Config",
]

publication.publish()

def _typecheckingstub__2ca4380956d01e305f9f2e0401744d6533b906f5d8c065ac4fd89465bb0c7c7e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ip_version: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    network_type: typing.Optional[builtins.str] = None,
    neutron_net_id: typing.Optional[builtins.str] = None,
    neutron_subnet_id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    security_service_id: typing.Optional[builtins.str] = None,
    segmentation_id: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__24f0daf183193a2b4c5a638faa44c6048a5050e91e71ef0c4d901f591c30c384(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34d86e9318ac34fb7cbfcbc21d5ab559bcf4a43eef0896998331ba639ac2fd27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__145b8c5ae4a97efb7688854fa2951507b1f6ccaa3ab50e47228a75d0f4028024(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87bff2a5cbd8297eb383f44b55756a5ae8924328bb8f82bfdd49a515561c8bcd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e567a29262cfaa52c2591e72e6a19360d789b819412e59ee7a9ecab1d14ee4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__888bcb1d68f9e80aaf338ad90e86618fba8b1bd0c004287b5d7dae6fbf2e628e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb0a8a72ea7873b383d9e081ca9bf95394d97735ce53eaa5b2278a46362eb60a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc3c061eb21d101d204805e85de70d3417045dc3b81da8d4d78cc06bdef1cf65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd6943215f2bb43b5d208be6a82e4e7b60eb6fc6306038e5a9be155f961afe41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95edf401b2c876c641e990e2937c45794c508e11dcbfac0098fb8c3e472c52df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09a70329a8ea02a36c1786eb984402fab98a3d598ba2132ec63d0e9370a63d8f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d83fc5212122113d798dd67e01bad82193e507fdd3469dd57442fb1dc95a3f1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ip_version: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    network_type: typing.Optional[builtins.str] = None,
    neutron_net_id: typing.Optional[builtins.str] = None,
    neutron_subnet_id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    security_service_id: typing.Optional[builtins.str] = None,
    segmentation_id: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
