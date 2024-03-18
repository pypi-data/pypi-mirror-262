'''
# `openstack_containerinfra_clustertemplate_v1`

Refer to the Terraform Registry for docs: [`openstack_containerinfra_clustertemplate_v1`](https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1).
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


class ContainerinfraClustertemplateV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@ithings/cdktf-provider-openstack.containerinfraClustertemplateV1.ContainerinfraClustertemplateV1",
):
    '''(experimental) Represents a {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1 openstack_containerinfra_clustertemplate_v1}.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        coe: builtins.str,
        image: builtins.str,
        name: builtins.str,
        apiserver_port: typing.Optional[jsii.Number] = None,
        cluster_distro: typing.Optional[builtins.str] = None,
        dns_nameserver: typing.Optional[builtins.str] = None,
        docker_storage_driver: typing.Optional[builtins.str] = None,
        docker_volume_size: typing.Optional[jsii.Number] = None,
        external_network_id: typing.Optional[builtins.str] = None,
        fixed_network: typing.Optional[builtins.str] = None,
        fixed_subnet: typing.Optional[builtins.str] = None,
        flavor: typing.Optional[builtins.str] = None,
        floating_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hidden: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        http_proxy: typing.Optional[builtins.str] = None,
        https_proxy: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        insecure_registry: typing.Optional[builtins.str] = None,
        keypair_id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        master_flavor: typing.Optional[builtins.str] = None,
        master_lb_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        network_driver: typing.Optional[builtins.str] = None,
        no_proxy: typing.Optional[builtins.str] = None,
        public: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        registry_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        server_type: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ContainerinfraClustertemplateV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        tls_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        volume_driver: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''(experimental) Create a new {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1 openstack_containerinfra_clustertemplate_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param coe: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#coe ContainerinfraClustertemplateV1#coe}.
        :param image: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#image ContainerinfraClustertemplateV1#image}.
        :param name: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#name ContainerinfraClustertemplateV1#name}.
        :param apiserver_port: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#apiserver_port ContainerinfraClustertemplateV1#apiserver_port}.
        :param cluster_distro: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#cluster_distro ContainerinfraClustertemplateV1#cluster_distro}.
        :param dns_nameserver: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#dns_nameserver ContainerinfraClustertemplateV1#dns_nameserver}.
        :param docker_storage_driver: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#docker_storage_driver ContainerinfraClustertemplateV1#docker_storage_driver}.
        :param docker_volume_size: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#docker_volume_size ContainerinfraClustertemplateV1#docker_volume_size}.
        :param external_network_id: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#external_network_id ContainerinfraClustertemplateV1#external_network_id}.
        :param fixed_network: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#fixed_network ContainerinfraClustertemplateV1#fixed_network}.
        :param fixed_subnet: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#fixed_subnet ContainerinfraClustertemplateV1#fixed_subnet}.
        :param flavor: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#flavor ContainerinfraClustertemplateV1#flavor}.
        :param floating_ip_enabled: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#floating_ip_enabled ContainerinfraClustertemplateV1#floating_ip_enabled}.
        :param hidden: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#hidden ContainerinfraClustertemplateV1#hidden}.
        :param http_proxy: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#http_proxy ContainerinfraClustertemplateV1#http_proxy}.
        :param https_proxy: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#https_proxy ContainerinfraClustertemplateV1#https_proxy}.
        :param id: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#id ContainerinfraClustertemplateV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param insecure_registry: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#insecure_registry ContainerinfraClustertemplateV1#insecure_registry}.
        :param keypair_id: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#keypair_id ContainerinfraClustertemplateV1#keypair_id}.
        :param labels: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#labels ContainerinfraClustertemplateV1#labels}.
        :param master_flavor: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#master_flavor ContainerinfraClustertemplateV1#master_flavor}.
        :param master_lb_enabled: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#master_lb_enabled ContainerinfraClustertemplateV1#master_lb_enabled}.
        :param network_driver: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#network_driver ContainerinfraClustertemplateV1#network_driver}.
        :param no_proxy: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#no_proxy ContainerinfraClustertemplateV1#no_proxy}.
        :param public: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#public ContainerinfraClustertemplateV1#public}.
        :param region: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#region ContainerinfraClustertemplateV1#region}.
        :param registry_enabled: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#registry_enabled ContainerinfraClustertemplateV1#registry_enabled}.
        :param server_type: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#server_type ContainerinfraClustertemplateV1#server_type}.
        :param timeouts: (experimental) timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#timeouts ContainerinfraClustertemplateV1#timeouts}
        :param tls_disabled: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#tls_disabled ContainerinfraClustertemplateV1#tls_disabled}.
        :param volume_driver: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#volume_driver ContainerinfraClustertemplateV1#volume_driver}.
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
            type_hints = typing.get_type_hints(_typecheckingstub__a920fbb7923d11d7551bcda0b6f3221d5a3e07f03afe4eb2d80bfe3fd870280b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ContainerinfraClustertemplateV1Config(
            coe=coe,
            image=image,
            name=name,
            apiserver_port=apiserver_port,
            cluster_distro=cluster_distro,
            dns_nameserver=dns_nameserver,
            docker_storage_driver=docker_storage_driver,
            docker_volume_size=docker_volume_size,
            external_network_id=external_network_id,
            fixed_network=fixed_network,
            fixed_subnet=fixed_subnet,
            flavor=flavor,
            floating_ip_enabled=floating_ip_enabled,
            hidden=hidden,
            http_proxy=http_proxy,
            https_proxy=https_proxy,
            id=id,
            insecure_registry=insecure_registry,
            keypair_id=keypair_id,
            labels=labels,
            master_flavor=master_flavor,
            master_lb_enabled=master_lb_enabled,
            network_driver=network_driver,
            no_proxy=no_proxy,
            public=public,
            region=region,
            registry_enabled=registry_enabled,
            server_type=server_type,
            timeouts=timeouts,
            tls_disabled=tls_disabled,
            volume_driver=volume_driver,
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
        '''(experimental) Generates CDKTF code for importing a ContainerinfraClustertemplateV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ContainerinfraClustertemplateV1 to import.
        :param import_from_id: The id of the existing ContainerinfraClustertemplateV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ContainerinfraClustertemplateV1 to import is found.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84593fb71fd6925442ade906a817a7518ac267e6799d64429486f16beafb32d5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#create ContainerinfraClustertemplateV1#create}.
        :param delete: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#delete ContainerinfraClustertemplateV1#delete}.

        :stability: experimental
        '''
        value = ContainerinfraClustertemplateV1Timeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetApiserverPort")
    def reset_apiserver_port(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetApiserverPort", []))

    @jsii.member(jsii_name="resetClusterDistro")
    def reset_cluster_distro(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetClusterDistro", []))

    @jsii.member(jsii_name="resetDnsNameserver")
    def reset_dns_nameserver(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetDnsNameserver", []))

    @jsii.member(jsii_name="resetDockerStorageDriver")
    def reset_docker_storage_driver(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetDockerStorageDriver", []))

    @jsii.member(jsii_name="resetDockerVolumeSize")
    def reset_docker_volume_size(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetDockerVolumeSize", []))

    @jsii.member(jsii_name="resetExternalNetworkId")
    def reset_external_network_id(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetExternalNetworkId", []))

    @jsii.member(jsii_name="resetFixedNetwork")
    def reset_fixed_network(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetFixedNetwork", []))

    @jsii.member(jsii_name="resetFixedSubnet")
    def reset_fixed_subnet(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetFixedSubnet", []))

    @jsii.member(jsii_name="resetFlavor")
    def reset_flavor(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetFlavor", []))

    @jsii.member(jsii_name="resetFloatingIpEnabled")
    def reset_floating_ip_enabled(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetFloatingIpEnabled", []))

    @jsii.member(jsii_name="resetHidden")
    def reset_hidden(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetHidden", []))

    @jsii.member(jsii_name="resetHttpProxy")
    def reset_http_proxy(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetHttpProxy", []))

    @jsii.member(jsii_name="resetHttpsProxy")
    def reset_https_proxy(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetHttpsProxy", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInsecureRegistry")
    def reset_insecure_registry(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetInsecureRegistry", []))

    @jsii.member(jsii_name="resetKeypairId")
    def reset_keypair_id(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetKeypairId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMasterFlavor")
    def reset_master_flavor(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetMasterFlavor", []))

    @jsii.member(jsii_name="resetMasterLbEnabled")
    def reset_master_lb_enabled(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetMasterLbEnabled", []))

    @jsii.member(jsii_name="resetNetworkDriver")
    def reset_network_driver(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetNetworkDriver", []))

    @jsii.member(jsii_name="resetNoProxy")
    def reset_no_proxy(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetNoProxy", []))

    @jsii.member(jsii_name="resetPublic")
    def reset_public(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetPublic", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRegistryEnabled")
    def reset_registry_enabled(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetRegistryEnabled", []))

    @jsii.member(jsii_name="resetServerType")
    def reset_server_type(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetServerType", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTlsDisabled")
    def reset_tls_disabled(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetTlsDisabled", []))

    @jsii.member(jsii_name="resetVolumeDriver")
    def reset_volume_driver(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetVolumeDriver", []))

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
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ContainerinfraClustertemplateV1TimeoutsOutputReference":
        '''
        :stability: experimental
        '''
        return typing.cast("ContainerinfraClustertemplateV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="userId")
    def user_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "userId"))

    @builtins.property
    @jsii.member(jsii_name="apiserverPortInput")
    def apiserver_port_input(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "apiserverPortInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterDistroInput")
    def cluster_distro_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterDistroInput"))

    @builtins.property
    @jsii.member(jsii_name="coeInput")
    def coe_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "coeInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsNameserverInput")
    def dns_nameserver_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dnsNameserverInput"))

    @builtins.property
    @jsii.member(jsii_name="dockerStorageDriverInput")
    def docker_storage_driver_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dockerStorageDriverInput"))

    @builtins.property
    @jsii.member(jsii_name="dockerVolumeSizeInput")
    def docker_volume_size_input(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dockerVolumeSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="externalNetworkIdInput")
    def external_network_id_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalNetworkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="fixedNetworkInput")
    def fixed_network_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fixedNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="fixedSubnetInput")
    def fixed_subnet_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fixedSubnetInput"))

    @builtins.property
    @jsii.member(jsii_name="flavorInput")
    def flavor_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flavorInput"))

    @builtins.property
    @jsii.member(jsii_name="floatingIpEnabledInput")
    def floating_ip_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "floatingIpEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="hiddenInput")
    def hidden_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "hiddenInput"))

    @builtins.property
    @jsii.member(jsii_name="httpProxyInput")
    def http_proxy_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpProxyInput"))

    @builtins.property
    @jsii.member(jsii_name="httpsProxyInput")
    def https_proxy_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpsProxyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="insecureRegistryInput")
    def insecure_registry_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "insecureRegistryInput"))

    @builtins.property
    @jsii.member(jsii_name="keypairIdInput")
    def keypair_id_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keypairIdInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="masterFlavorInput")
    def master_flavor_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "masterFlavorInput"))

    @builtins.property
    @jsii.member(jsii_name="masterLbEnabledInput")
    def master_lb_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "masterLbEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkDriverInput")
    def network_driver_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkDriverInput"))

    @builtins.property
    @jsii.member(jsii_name="noProxyInput")
    def no_proxy_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "noProxyInput"))

    @builtins.property
    @jsii.member(jsii_name="publicInput")
    def public_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publicInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="registryEnabledInput")
    def registry_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "registryEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="serverTypeInput")
    def server_type_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ContainerinfraClustertemplateV1Timeouts"]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ContainerinfraClustertemplateV1Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsDisabledInput")
    def tls_disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tlsDisabledInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeDriverInput")
    def volume_driver_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeDriverInput"))

    @builtins.property
    @jsii.member(jsii_name="apiserverPort")
    def apiserver_port(self) -> jsii.Number:
        '''
        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "apiserverPort"))

    @apiserver_port.setter
    def apiserver_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__608afce71006ba877dbf28ffdf2a60615d975ced6a4f13fb81a2867af909b3b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiserverPort", value)

    @builtins.property
    @jsii.member(jsii_name="clusterDistro")
    def cluster_distro(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "clusterDistro"))

    @cluster_distro.setter
    def cluster_distro(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1afee77cd4498303def78daf2d2b8d82b665ab1139001836f2e882d18d4e1b2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterDistro", value)

    @builtins.property
    @jsii.member(jsii_name="coe")
    def coe(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "coe"))

    @coe.setter
    def coe(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbbe856d89ff2e40b0d91f2f1c2696bf7c833bcf562c8dd0b2297910a2d92a96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coe", value)

    @builtins.property
    @jsii.member(jsii_name="dnsNameserver")
    def dns_nameserver(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "dnsNameserver"))

    @dns_nameserver.setter
    def dns_nameserver(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b0075c853bae41e5b8dab9facc426d125b16d3e70001ccc3d6a554ae37f8177)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsNameserver", value)

    @builtins.property
    @jsii.member(jsii_name="dockerStorageDriver")
    def docker_storage_driver(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "dockerStorageDriver"))

    @docker_storage_driver.setter
    def docker_storage_driver(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d955a30d97c4abe14c2cc89a05e01378cb78940553d28eb820a436e2d27c5e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerStorageDriver", value)

    @builtins.property
    @jsii.member(jsii_name="dockerVolumeSize")
    def docker_volume_size(self) -> jsii.Number:
        '''
        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "dockerVolumeSize"))

    @docker_volume_size.setter
    def docker_volume_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc542040a1d0de3816dc34489c28cbb92752f6ce9d635f34b938f52791c5d20e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerVolumeSize", value)

    @builtins.property
    @jsii.member(jsii_name="externalNetworkId")
    def external_network_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "externalNetworkId"))

    @external_network_id.setter
    def external_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8baf6eaa12e769185c89c3cd5218545eb745c4913f2bb3646af5420430741d19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalNetworkId", value)

    @builtins.property
    @jsii.member(jsii_name="fixedNetwork")
    def fixed_network(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "fixedNetwork"))

    @fixed_network.setter
    def fixed_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc1110d7002d0f284559ee56249391d340ab9277abf3cfa4d42ca8b7403b5e86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixedNetwork", value)

    @builtins.property
    @jsii.member(jsii_name="fixedSubnet")
    def fixed_subnet(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "fixedSubnet"))

    @fixed_subnet.setter
    def fixed_subnet(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0221326ea36b381020e657c74452b25593c7d36b6113501784e27e6bc0d0010)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixedSubnet", value)

    @builtins.property
    @jsii.member(jsii_name="flavor")
    def flavor(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "flavor"))

    @flavor.setter
    def flavor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9666f9d1bae79f1b0225d110340a4508f8821fe80cc0fa0bbb0f52fba6c8e923)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flavor", value)

    @builtins.property
    @jsii.member(jsii_name="floatingIpEnabled")
    def floating_ip_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "floatingIpEnabled"))

    @floating_ip_enabled.setter
    def floating_ip_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf706282017a9443df2583dd5de459ac80508defbe1c2ddc81bb70c06877fce7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "floatingIpEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="hidden")
    def hidden(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "hidden"))

    @hidden.setter
    def hidden(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52dfbb215a0cf1a6692db5817bb657c46c04b8513369900ce44b4aa953f2afc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hidden", value)

    @builtins.property
    @jsii.member(jsii_name="httpProxy")
    def http_proxy(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "httpProxy"))

    @http_proxy.setter
    def http_proxy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b17cd32dc289b0f0d81342bbd1b86c4a843db265db39653f939ff2d5024b683b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpProxy", value)

    @builtins.property
    @jsii.member(jsii_name="httpsProxy")
    def https_proxy(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "httpsProxy"))

    @https_proxy.setter
    def https_proxy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e96f2d57ab785375b1dceee59518d165a5f52998e9a272fde94444e5baf7f5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsProxy", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__b6a505ae201d59c4bff5c7d42f1e61e8441c5ed0d049948b11ec713de51b77df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8831c1e647d4889fd81e8f9c62a2c07e43361b0a568a728d7451b71c80c6b789)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value)

    @builtins.property
    @jsii.member(jsii_name="insecureRegistry")
    def insecure_registry(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "insecureRegistry"))

    @insecure_registry.setter
    def insecure_registry(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48f8ae22134b3aad0ccd4574bec67c3a1bbdd6b387e15dcf6d25bbb03637c8c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insecureRegistry", value)

    @builtins.property
    @jsii.member(jsii_name="keypairId")
    def keypair_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "keypairId"))

    @keypair_id.setter
    def keypair_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf534bc36b883b7a9a06b0f24bee94e819a2178560b89fe85ea05e09098f0a72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keypairId", value)

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3978bdc7bdf80bbe67866a9199f11574edf9f234e85c6498ca62384b01c4729)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value)

    @builtins.property
    @jsii.member(jsii_name="masterFlavor")
    def master_flavor(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "masterFlavor"))

    @master_flavor.setter
    def master_flavor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b3a2ef0dcb09a86f6938b2dd286d2d4b0eba7b8df81ca3495475664d7affe6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "masterFlavor", value)

    @builtins.property
    @jsii.member(jsii_name="masterLbEnabled")
    def master_lb_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "masterLbEnabled"))

    @master_lb_enabled.setter
    def master_lb_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__928b3a756370575436fe7d484e1c4173b392f8bec92085333de2dce40a066cf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "masterLbEnabled", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__580a9f45192eea08e1f1450fcfa02c6c6e3bc7a8b96973828b736d60eb1850fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="networkDriver")
    def network_driver(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "networkDriver"))

    @network_driver.setter
    def network_driver(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__026b530d53b8042b4f35cfc8344b457166e71137d9edd23ca88b380a343e25ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkDriver", value)

    @builtins.property
    @jsii.member(jsii_name="noProxy")
    def no_proxy(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "noProxy"))

    @no_proxy.setter
    def no_proxy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3556e4f92ccd3672d862ded8014340c8ff73d93170a35b7e1d9d601916f71ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noProxy", value)

    @builtins.property
    @jsii.member(jsii_name="public")
    def public(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "public"))

    @public.setter
    def public(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a1d93877057702bd7c931198f07eca7ee24c95239c6a5b918e2ba0e8dfa6eff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "public", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__3b647a22c9819d3126ff1249f3b4bd8d3b55729918360991fac254d04fb60c62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value)

    @builtins.property
    @jsii.member(jsii_name="registryEnabled")
    def registry_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "registryEnabled"))

    @registry_enabled.setter
    def registry_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b5666804b493a6550e7975b4a1219775842091986cd8e4f001b5ba480df973c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registryEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="serverType")
    def server_type(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "serverType"))

    @server_type.setter
    def server_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc751a3fa9bca5e671b5d14d75e9e8d1c2b89eb817711b09ad6202f670fe3c18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverType", value)

    @builtins.property
    @jsii.member(jsii_name="tlsDisabled")
    def tls_disabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tlsDisabled"))

    @tls_disabled.setter
    def tls_disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51a1ab15a0a55696a6ef3debd52c901c5c27aac01773b5ae1b78316ebf5ff8ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsDisabled", value)

    @builtins.property
    @jsii.member(jsii_name="volumeDriver")
    def volume_driver(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "volumeDriver"))

    @volume_driver.setter
    def volume_driver(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c9829722d2345c6f70466751f92560b7c83f0fcb51cb4e85ced5a2eb4d6572d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeDriver", value)


@jsii.data_type(
    jsii_type="@ithings/cdktf-provider-openstack.containerinfraClustertemplateV1.ContainerinfraClustertemplateV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "coe": "coe",
        "image": "image",
        "name": "name",
        "apiserver_port": "apiserverPort",
        "cluster_distro": "clusterDistro",
        "dns_nameserver": "dnsNameserver",
        "docker_storage_driver": "dockerStorageDriver",
        "docker_volume_size": "dockerVolumeSize",
        "external_network_id": "externalNetworkId",
        "fixed_network": "fixedNetwork",
        "fixed_subnet": "fixedSubnet",
        "flavor": "flavor",
        "floating_ip_enabled": "floatingIpEnabled",
        "hidden": "hidden",
        "http_proxy": "httpProxy",
        "https_proxy": "httpsProxy",
        "id": "id",
        "insecure_registry": "insecureRegistry",
        "keypair_id": "keypairId",
        "labels": "labels",
        "master_flavor": "masterFlavor",
        "master_lb_enabled": "masterLbEnabled",
        "network_driver": "networkDriver",
        "no_proxy": "noProxy",
        "public": "public",
        "region": "region",
        "registry_enabled": "registryEnabled",
        "server_type": "serverType",
        "timeouts": "timeouts",
        "tls_disabled": "tlsDisabled",
        "volume_driver": "volumeDriver",
    },
)
class ContainerinfraClustertemplateV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        coe: builtins.str,
        image: builtins.str,
        name: builtins.str,
        apiserver_port: typing.Optional[jsii.Number] = None,
        cluster_distro: typing.Optional[builtins.str] = None,
        dns_nameserver: typing.Optional[builtins.str] = None,
        docker_storage_driver: typing.Optional[builtins.str] = None,
        docker_volume_size: typing.Optional[jsii.Number] = None,
        external_network_id: typing.Optional[builtins.str] = None,
        fixed_network: typing.Optional[builtins.str] = None,
        fixed_subnet: typing.Optional[builtins.str] = None,
        flavor: typing.Optional[builtins.str] = None,
        floating_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hidden: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        http_proxy: typing.Optional[builtins.str] = None,
        https_proxy: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        insecure_registry: typing.Optional[builtins.str] = None,
        keypair_id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        master_flavor: typing.Optional[builtins.str] = None,
        master_lb_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        network_driver: typing.Optional[builtins.str] = None,
        no_proxy: typing.Optional[builtins.str] = None,
        public: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        registry_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        server_type: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ContainerinfraClustertemplateV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        tls_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        volume_driver: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param coe: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#coe ContainerinfraClustertemplateV1#coe}.
        :param image: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#image ContainerinfraClustertemplateV1#image}.
        :param name: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#name ContainerinfraClustertemplateV1#name}.
        :param apiserver_port: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#apiserver_port ContainerinfraClustertemplateV1#apiserver_port}.
        :param cluster_distro: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#cluster_distro ContainerinfraClustertemplateV1#cluster_distro}.
        :param dns_nameserver: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#dns_nameserver ContainerinfraClustertemplateV1#dns_nameserver}.
        :param docker_storage_driver: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#docker_storage_driver ContainerinfraClustertemplateV1#docker_storage_driver}.
        :param docker_volume_size: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#docker_volume_size ContainerinfraClustertemplateV1#docker_volume_size}.
        :param external_network_id: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#external_network_id ContainerinfraClustertemplateV1#external_network_id}.
        :param fixed_network: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#fixed_network ContainerinfraClustertemplateV1#fixed_network}.
        :param fixed_subnet: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#fixed_subnet ContainerinfraClustertemplateV1#fixed_subnet}.
        :param flavor: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#flavor ContainerinfraClustertemplateV1#flavor}.
        :param floating_ip_enabled: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#floating_ip_enabled ContainerinfraClustertemplateV1#floating_ip_enabled}.
        :param hidden: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#hidden ContainerinfraClustertemplateV1#hidden}.
        :param http_proxy: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#http_proxy ContainerinfraClustertemplateV1#http_proxy}.
        :param https_proxy: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#https_proxy ContainerinfraClustertemplateV1#https_proxy}.
        :param id: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#id ContainerinfraClustertemplateV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param insecure_registry: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#insecure_registry ContainerinfraClustertemplateV1#insecure_registry}.
        :param keypair_id: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#keypair_id ContainerinfraClustertemplateV1#keypair_id}.
        :param labels: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#labels ContainerinfraClustertemplateV1#labels}.
        :param master_flavor: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#master_flavor ContainerinfraClustertemplateV1#master_flavor}.
        :param master_lb_enabled: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#master_lb_enabled ContainerinfraClustertemplateV1#master_lb_enabled}.
        :param network_driver: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#network_driver ContainerinfraClustertemplateV1#network_driver}.
        :param no_proxy: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#no_proxy ContainerinfraClustertemplateV1#no_proxy}.
        :param public: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#public ContainerinfraClustertemplateV1#public}.
        :param region: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#region ContainerinfraClustertemplateV1#region}.
        :param registry_enabled: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#registry_enabled ContainerinfraClustertemplateV1#registry_enabled}.
        :param server_type: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#server_type ContainerinfraClustertemplateV1#server_type}.
        :param timeouts: (experimental) timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#timeouts ContainerinfraClustertemplateV1#timeouts}
        :param tls_disabled: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#tls_disabled ContainerinfraClustertemplateV1#tls_disabled}.
        :param volume_driver: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#volume_driver ContainerinfraClustertemplateV1#volume_driver}.

        :stability: experimental
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = ContainerinfraClustertemplateV1Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a490ad5c9f918417cbeccfcdd8c1e4ae58221f9370d712b155729cf721146deb)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument coe", value=coe, expected_type=type_hints["coe"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument apiserver_port", value=apiserver_port, expected_type=type_hints["apiserver_port"])
            check_type(argname="argument cluster_distro", value=cluster_distro, expected_type=type_hints["cluster_distro"])
            check_type(argname="argument dns_nameserver", value=dns_nameserver, expected_type=type_hints["dns_nameserver"])
            check_type(argname="argument docker_storage_driver", value=docker_storage_driver, expected_type=type_hints["docker_storage_driver"])
            check_type(argname="argument docker_volume_size", value=docker_volume_size, expected_type=type_hints["docker_volume_size"])
            check_type(argname="argument external_network_id", value=external_network_id, expected_type=type_hints["external_network_id"])
            check_type(argname="argument fixed_network", value=fixed_network, expected_type=type_hints["fixed_network"])
            check_type(argname="argument fixed_subnet", value=fixed_subnet, expected_type=type_hints["fixed_subnet"])
            check_type(argname="argument flavor", value=flavor, expected_type=type_hints["flavor"])
            check_type(argname="argument floating_ip_enabled", value=floating_ip_enabled, expected_type=type_hints["floating_ip_enabled"])
            check_type(argname="argument hidden", value=hidden, expected_type=type_hints["hidden"])
            check_type(argname="argument http_proxy", value=http_proxy, expected_type=type_hints["http_proxy"])
            check_type(argname="argument https_proxy", value=https_proxy, expected_type=type_hints["https_proxy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument insecure_registry", value=insecure_registry, expected_type=type_hints["insecure_registry"])
            check_type(argname="argument keypair_id", value=keypair_id, expected_type=type_hints["keypair_id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument master_flavor", value=master_flavor, expected_type=type_hints["master_flavor"])
            check_type(argname="argument master_lb_enabled", value=master_lb_enabled, expected_type=type_hints["master_lb_enabled"])
            check_type(argname="argument network_driver", value=network_driver, expected_type=type_hints["network_driver"])
            check_type(argname="argument no_proxy", value=no_proxy, expected_type=type_hints["no_proxy"])
            check_type(argname="argument public", value=public, expected_type=type_hints["public"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument registry_enabled", value=registry_enabled, expected_type=type_hints["registry_enabled"])
            check_type(argname="argument server_type", value=server_type, expected_type=type_hints["server_type"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument tls_disabled", value=tls_disabled, expected_type=type_hints["tls_disabled"])
            check_type(argname="argument volume_driver", value=volume_driver, expected_type=type_hints["volume_driver"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "coe": coe,
            "image": image,
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
        if apiserver_port is not None:
            self._values["apiserver_port"] = apiserver_port
        if cluster_distro is not None:
            self._values["cluster_distro"] = cluster_distro
        if dns_nameserver is not None:
            self._values["dns_nameserver"] = dns_nameserver
        if docker_storage_driver is not None:
            self._values["docker_storage_driver"] = docker_storage_driver
        if docker_volume_size is not None:
            self._values["docker_volume_size"] = docker_volume_size
        if external_network_id is not None:
            self._values["external_network_id"] = external_network_id
        if fixed_network is not None:
            self._values["fixed_network"] = fixed_network
        if fixed_subnet is not None:
            self._values["fixed_subnet"] = fixed_subnet
        if flavor is not None:
            self._values["flavor"] = flavor
        if floating_ip_enabled is not None:
            self._values["floating_ip_enabled"] = floating_ip_enabled
        if hidden is not None:
            self._values["hidden"] = hidden
        if http_proxy is not None:
            self._values["http_proxy"] = http_proxy
        if https_proxy is not None:
            self._values["https_proxy"] = https_proxy
        if id is not None:
            self._values["id"] = id
        if insecure_registry is not None:
            self._values["insecure_registry"] = insecure_registry
        if keypair_id is not None:
            self._values["keypair_id"] = keypair_id
        if labels is not None:
            self._values["labels"] = labels
        if master_flavor is not None:
            self._values["master_flavor"] = master_flavor
        if master_lb_enabled is not None:
            self._values["master_lb_enabled"] = master_lb_enabled
        if network_driver is not None:
            self._values["network_driver"] = network_driver
        if no_proxy is not None:
            self._values["no_proxy"] = no_proxy
        if public is not None:
            self._values["public"] = public
        if region is not None:
            self._values["region"] = region
        if registry_enabled is not None:
            self._values["registry_enabled"] = registry_enabled
        if server_type is not None:
            self._values["server_type"] = server_type
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if tls_disabled is not None:
            self._values["tls_disabled"] = tls_disabled
        if volume_driver is not None:
            self._values["volume_driver"] = volume_driver

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
    def coe(self) -> builtins.str:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#coe ContainerinfraClustertemplateV1#coe}.

        :stability: experimental
        '''
        result = self._values.get("coe")
        assert result is not None, "Required property 'coe' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image(self) -> builtins.str:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#image ContainerinfraClustertemplateV1#image}.

        :stability: experimental
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#name ContainerinfraClustertemplateV1#name}.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def apiserver_port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#apiserver_port ContainerinfraClustertemplateV1#apiserver_port}.

        :stability: experimental
        '''
        result = self._values.get("apiserver_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cluster_distro(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#cluster_distro ContainerinfraClustertemplateV1#cluster_distro}.

        :stability: experimental
        '''
        result = self._values.get("cluster_distro")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns_nameserver(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#dns_nameserver ContainerinfraClustertemplateV1#dns_nameserver}.

        :stability: experimental
        '''
        result = self._values.get("dns_nameserver")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docker_storage_driver(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#docker_storage_driver ContainerinfraClustertemplateV1#docker_storage_driver}.

        :stability: experimental
        '''
        result = self._values.get("docker_storage_driver")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docker_volume_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#docker_volume_size ContainerinfraClustertemplateV1#docker_volume_size}.

        :stability: experimental
        '''
        result = self._values.get("docker_volume_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def external_network_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#external_network_id ContainerinfraClustertemplateV1#external_network_id}.

        :stability: experimental
        '''
        result = self._values.get("external_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fixed_network(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#fixed_network ContainerinfraClustertemplateV1#fixed_network}.

        :stability: experimental
        '''
        result = self._values.get("fixed_network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fixed_subnet(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#fixed_subnet ContainerinfraClustertemplateV1#fixed_subnet}.

        :stability: experimental
        '''
        result = self._values.get("fixed_subnet")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def flavor(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#flavor ContainerinfraClustertemplateV1#flavor}.

        :stability: experimental
        '''
        result = self._values.get("flavor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def floating_ip_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#floating_ip_enabled ContainerinfraClustertemplateV1#floating_ip_enabled}.

        :stability: experimental
        '''
        result = self._values.get("floating_ip_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def hidden(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#hidden ContainerinfraClustertemplateV1#hidden}.

        :stability: experimental
        '''
        result = self._values.get("hidden")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def http_proxy(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#http_proxy ContainerinfraClustertemplateV1#http_proxy}.

        :stability: experimental
        '''
        result = self._values.get("http_proxy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def https_proxy(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#https_proxy ContainerinfraClustertemplateV1#https_proxy}.

        :stability: experimental
        '''
        result = self._values.get("https_proxy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#id ContainerinfraClustertemplateV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.

        :stability: experimental
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insecure_registry(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#insecure_registry ContainerinfraClustertemplateV1#insecure_registry}.

        :stability: experimental
        '''
        result = self._values.get("insecure_registry")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keypair_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#keypair_id ContainerinfraClustertemplateV1#keypair_id}.

        :stability: experimental
        '''
        result = self._values.get("keypair_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#labels ContainerinfraClustertemplateV1#labels}.

        :stability: experimental
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def master_flavor(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#master_flavor ContainerinfraClustertemplateV1#master_flavor}.

        :stability: experimental
        '''
        result = self._values.get("master_flavor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_lb_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#master_lb_enabled ContainerinfraClustertemplateV1#master_lb_enabled}.

        :stability: experimental
        '''
        result = self._values.get("master_lb_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def network_driver(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#network_driver ContainerinfraClustertemplateV1#network_driver}.

        :stability: experimental
        '''
        result = self._values.get("network_driver")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def no_proxy(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#no_proxy ContainerinfraClustertemplateV1#no_proxy}.

        :stability: experimental
        '''
        result = self._values.get("no_proxy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#public ContainerinfraClustertemplateV1#public}.

        :stability: experimental
        '''
        result = self._values.get("public")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#region ContainerinfraClustertemplateV1#region}.

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def registry_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#registry_enabled ContainerinfraClustertemplateV1#registry_enabled}.

        :stability: experimental
        '''
        result = self._values.get("registry_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def server_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#server_type ContainerinfraClustertemplateV1#server_type}.

        :stability: experimental
        '''
        result = self._values.get("server_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ContainerinfraClustertemplateV1Timeouts"]:
        '''(experimental) timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#timeouts ContainerinfraClustertemplateV1#timeouts}

        :stability: experimental
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ContainerinfraClustertemplateV1Timeouts"], result)

    @builtins.property
    def tls_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#tls_disabled ContainerinfraClustertemplateV1#tls_disabled}.

        :stability: experimental
        '''
        result = self._values.get("tls_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def volume_driver(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#volume_driver ContainerinfraClustertemplateV1#volume_driver}.

        :stability: experimental
        '''
        result = self._values.get("volume_driver")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerinfraClustertemplateV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@ithings/cdktf-provider-openstack.containerinfraClustertemplateV1.ContainerinfraClustertemplateV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class ContainerinfraClustertemplateV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#create ContainerinfraClustertemplateV1#create}.
        :param delete: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#delete ContainerinfraClustertemplateV1#delete}.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d05b016c9e06bf79590499d8aa67222f42a1103bf0d0ae8eb254eab4f4e676f)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#create ContainerinfraClustertemplateV1#create}.

        :stability: experimental
        '''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs/resources/containerinfra_clustertemplate_v1#delete ContainerinfraClustertemplateV1#delete}.

        :stability: experimental
        '''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerinfraClustertemplateV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerinfraClustertemplateV1TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@ithings/cdktf-provider-openstack.containerinfraClustertemplateV1.ContainerinfraClustertemplateV1TimeoutsOutputReference",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3100f77e273336f19f639d8e30e27180150114b863b593175268c5b8d40cc134)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01cb368abbcd1e41c94b1bcb4cab96e768a4a68f5ac249a4642768ad75ec35a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19d3eea0aa9dd974e04eb5da7eda76d9ce21d8800237c297b8125e2af135d49b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerinfraClustertemplateV1Timeouts]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerinfraClustertemplateV1Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerinfraClustertemplateV1Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08fdac2677953740ba503c7a632eead0852e58052ce2bb8364db0676ce8d1df9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "ContainerinfraClustertemplateV1",
    "ContainerinfraClustertemplateV1Config",
    "ContainerinfraClustertemplateV1Timeouts",
    "ContainerinfraClustertemplateV1TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__a920fbb7923d11d7551bcda0b6f3221d5a3e07f03afe4eb2d80bfe3fd870280b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    coe: builtins.str,
    image: builtins.str,
    name: builtins.str,
    apiserver_port: typing.Optional[jsii.Number] = None,
    cluster_distro: typing.Optional[builtins.str] = None,
    dns_nameserver: typing.Optional[builtins.str] = None,
    docker_storage_driver: typing.Optional[builtins.str] = None,
    docker_volume_size: typing.Optional[jsii.Number] = None,
    external_network_id: typing.Optional[builtins.str] = None,
    fixed_network: typing.Optional[builtins.str] = None,
    fixed_subnet: typing.Optional[builtins.str] = None,
    flavor: typing.Optional[builtins.str] = None,
    floating_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hidden: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    http_proxy: typing.Optional[builtins.str] = None,
    https_proxy: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    insecure_registry: typing.Optional[builtins.str] = None,
    keypair_id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    master_flavor: typing.Optional[builtins.str] = None,
    master_lb_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    network_driver: typing.Optional[builtins.str] = None,
    no_proxy: typing.Optional[builtins.str] = None,
    public: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    registry_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    server_type: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ContainerinfraClustertemplateV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    tls_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    volume_driver: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__84593fb71fd6925442ade906a817a7518ac267e6799d64429486f16beafb32d5(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__608afce71006ba877dbf28ffdf2a60615d975ced6a4f13fb81a2867af909b3b5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1afee77cd4498303def78daf2d2b8d82b665ab1139001836f2e882d18d4e1b2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbbe856d89ff2e40b0d91f2f1c2696bf7c833bcf562c8dd0b2297910a2d92a96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b0075c853bae41e5b8dab9facc426d125b16d3e70001ccc3d6a554ae37f8177(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d955a30d97c4abe14c2cc89a05e01378cb78940553d28eb820a436e2d27c5e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc542040a1d0de3816dc34489c28cbb92752f6ce9d635f34b938f52791c5d20e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8baf6eaa12e769185c89c3cd5218545eb745c4913f2bb3646af5420430741d19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc1110d7002d0f284559ee56249391d340ab9277abf3cfa4d42ca8b7403b5e86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0221326ea36b381020e657c74452b25593c7d36b6113501784e27e6bc0d0010(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9666f9d1bae79f1b0225d110340a4508f8821fe80cc0fa0bbb0f52fba6c8e923(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf706282017a9443df2583dd5de459ac80508defbe1c2ddc81bb70c06877fce7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52dfbb215a0cf1a6692db5817bb657c46c04b8513369900ce44b4aa953f2afc5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b17cd32dc289b0f0d81342bbd1b86c4a843db265db39653f939ff2d5024b683b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e96f2d57ab785375b1dceee59518d165a5f52998e9a272fde94444e5baf7f5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6a505ae201d59c4bff5c7d42f1e61e8441c5ed0d049948b11ec713de51b77df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8831c1e647d4889fd81e8f9c62a2c07e43361b0a568a728d7451b71c80c6b789(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48f8ae22134b3aad0ccd4574bec67c3a1bbdd6b387e15dcf6d25bbb03637c8c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf534bc36b883b7a9a06b0f24bee94e819a2178560b89fe85ea05e09098f0a72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3978bdc7bdf80bbe67866a9199f11574edf9f234e85c6498ca62384b01c4729(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b3a2ef0dcb09a86f6938b2dd286d2d4b0eba7b8df81ca3495475664d7affe6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__928b3a756370575436fe7d484e1c4173b392f8bec92085333de2dce40a066cf9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__580a9f45192eea08e1f1450fcfa02c6c6e3bc7a8b96973828b736d60eb1850fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__026b530d53b8042b4f35cfc8344b457166e71137d9edd23ca88b380a343e25ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3556e4f92ccd3672d862ded8014340c8ff73d93170a35b7e1d9d601916f71ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a1d93877057702bd7c931198f07eca7ee24c95239c6a5b918e2ba0e8dfa6eff(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b647a22c9819d3126ff1249f3b4bd8d3b55729918360991fac254d04fb60c62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b5666804b493a6550e7975b4a1219775842091986cd8e4f001b5ba480df973c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc751a3fa9bca5e671b5d14d75e9e8d1c2b89eb817711b09ad6202f670fe3c18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51a1ab15a0a55696a6ef3debd52c901c5c27aac01773b5ae1b78316ebf5ff8ac(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c9829722d2345c6f70466751f92560b7c83f0fcb51cb4e85ced5a2eb4d6572d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a490ad5c9f918417cbeccfcdd8c1e4ae58221f9370d712b155729cf721146deb(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    coe: builtins.str,
    image: builtins.str,
    name: builtins.str,
    apiserver_port: typing.Optional[jsii.Number] = None,
    cluster_distro: typing.Optional[builtins.str] = None,
    dns_nameserver: typing.Optional[builtins.str] = None,
    docker_storage_driver: typing.Optional[builtins.str] = None,
    docker_volume_size: typing.Optional[jsii.Number] = None,
    external_network_id: typing.Optional[builtins.str] = None,
    fixed_network: typing.Optional[builtins.str] = None,
    fixed_subnet: typing.Optional[builtins.str] = None,
    flavor: typing.Optional[builtins.str] = None,
    floating_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hidden: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    http_proxy: typing.Optional[builtins.str] = None,
    https_proxy: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    insecure_registry: typing.Optional[builtins.str] = None,
    keypair_id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    master_flavor: typing.Optional[builtins.str] = None,
    master_lb_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    network_driver: typing.Optional[builtins.str] = None,
    no_proxy: typing.Optional[builtins.str] = None,
    public: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    registry_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    server_type: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ContainerinfraClustertemplateV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    tls_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    volume_driver: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d05b016c9e06bf79590499d8aa67222f42a1103bf0d0ae8eb254eab4f4e676f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3100f77e273336f19f639d8e30e27180150114b863b593175268c5b8d40cc134(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01cb368abbcd1e41c94b1bcb4cab96e768a4a68f5ac249a4642768ad75ec35a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19d3eea0aa9dd974e04eb5da7eda76d9ce21d8800237c297b8125e2af135d49b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08fdac2677953740ba503c7a632eead0852e58052ce2bb8364db0676ce8d1df9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerinfraClustertemplateV1Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
