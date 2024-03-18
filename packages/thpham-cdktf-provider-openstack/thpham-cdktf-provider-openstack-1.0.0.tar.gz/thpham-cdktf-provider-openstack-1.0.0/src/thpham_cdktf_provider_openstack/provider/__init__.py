'''
# `provider`

Refer to the Terraform Registry for docs: [`openstack`](https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs).
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


class OpenstackProvider(
    _cdktf_9a9027ec.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@ithings/cdktf-provider-openstack.provider.OpenstackProvider",
):
    '''(experimental) Represents a {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs openstack}.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        alias: typing.Optional[builtins.str] = None,
        allow_reauth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        application_credential_id: typing.Optional[builtins.str] = None,
        application_credential_name: typing.Optional[builtins.str] = None,
        application_credential_secret: typing.Optional[builtins.str] = None,
        auth_url: typing.Optional[builtins.str] = None,
        cacert_file: typing.Optional[builtins.str] = None,
        cert: typing.Optional[builtins.str] = None,
        cloud: typing.Optional[builtins.str] = None,
        default_domain: typing.Optional[builtins.str] = None,
        delayed_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_no_cache_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        domain_id: typing.Optional[builtins.str] = None,
        domain_name: typing.Optional[builtins.str] = None,
        enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        endpoint_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        endpoint_type: typing.Optional[builtins.str] = None,
        insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key: typing.Optional[builtins.str] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        password: typing.Optional[builtins.str] = None,
        project_domain_id: typing.Optional[builtins.str] = None,
        project_domain_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        swauth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        system_scope: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        tenant_name: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        use_octavia: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        user_domain_id: typing.Optional[builtins.str] = None,
        user_domain_name: typing.Optional[builtins.str] = None,
        user_id: typing.Optional[builtins.str] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Create a new {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs openstack} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param alias: (experimental) Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#alias OpenstackProvider#alias}
        :param allow_reauth: (experimental) If set to ``false``, OpenStack authorization won't be perfomed automatically, if the initial auth token get expired. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#allow_reauth OpenstackProvider#allow_reauth}
        :param application_credential_id: (experimental) Application Credential ID to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#application_credential_id OpenstackProvider#application_credential_id}
        :param application_credential_name: (experimental) Application Credential name to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#application_credential_name OpenstackProvider#application_credential_name}
        :param application_credential_secret: (experimental) Application Credential secret to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#application_credential_secret OpenstackProvider#application_credential_secret}
        :param auth_url: (experimental) The Identity authentication URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#auth_url OpenstackProvider#auth_url}
        :param cacert_file: (experimental) A Custom CA certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#cacert_file OpenstackProvider#cacert_file}
        :param cert: (experimental) A client certificate to authenticate with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#cert OpenstackProvider#cert}
        :param cloud: (experimental) An entry in a ``clouds.yaml`` file to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#cloud OpenstackProvider#cloud}
        :param default_domain: (experimental) The name of the Domain ID to scope to if no other domain is specified. Defaults to ``default`` (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#default_domain OpenstackProvider#default_domain}
        :param delayed_auth: (experimental) If set to ``false``, OpenStack authorization will be perfomed, every time the service provider client is called. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#delayed_auth OpenstackProvider#delayed_auth}
        :param disable_no_cache_header: (experimental) If set to ``true``, the HTTP ``Cache-Control: no-cache`` header will not be added by default to all API requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#disable_no_cache_header OpenstackProvider#disable_no_cache_header}
        :param domain_id: (experimental) The ID of the Domain to scope to (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#domain_id OpenstackProvider#domain_id}
        :param domain_name: (experimental) The name of the Domain to scope to (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#domain_name OpenstackProvider#domain_name}
        :param enable_logging: (experimental) Outputs very verbose logs with all calls made to and responses from OpenStack. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#enable_logging OpenstackProvider#enable_logging}
        :param endpoint_overrides: (experimental) A map of services with an endpoint to override what was from the Keystone catalog. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#endpoint_overrides OpenstackProvider#endpoint_overrides}
        :param endpoint_type: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#endpoint_type OpenstackProvider#endpoint_type}.
        :param insecure: (experimental) Trust self-signed certificates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#insecure OpenstackProvider#insecure}
        :param key: (experimental) A client private key to authenticate with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#key OpenstackProvider#key}
        :param max_retries: (experimental) How many times HTTP connection should be retried until giving up. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#max_retries OpenstackProvider#max_retries}
        :param password: (experimental) Password to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#password OpenstackProvider#password}
        :param project_domain_id: (experimental) The ID of the domain where the proejct resides (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#project_domain_id OpenstackProvider#project_domain_id}
        :param project_domain_name: (experimental) The name of the domain where the project resides (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#project_domain_name OpenstackProvider#project_domain_name}
        :param region: (experimental) The OpenStack region to connect to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#region OpenstackProvider#region}
        :param swauth: (experimental) Use Swift's authentication system instead of Keystone. Only used for interaction with Swift. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#swauth OpenstackProvider#swauth}
        :param system_scope: (experimental) If set to ``true``, system scoped authorization will be enabled. Defaults to ``false`` (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#system_scope OpenstackProvider#system_scope}
        :param tenant_id: (experimental) The ID of the Tenant (Identity v2) or Project (Identity v3) to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#tenant_id OpenstackProvider#tenant_id}
        :param tenant_name: (experimental) The name of the Tenant (Identity v2) or Project (Identity v3) to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#tenant_name OpenstackProvider#tenant_name}
        :param token: (experimental) Authentication token to use as an alternative to username/password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#token OpenstackProvider#token}
        :param use_octavia: (experimental) If set to ``true``, API requests will go the Load Balancer service (Octavia) instead of the Networking service (Neutron). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#use_octavia OpenstackProvider#use_octavia}
        :param user_domain_id: (experimental) The ID of the domain where the user resides (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#user_domain_id OpenstackProvider#user_domain_id}
        :param user_domain_name: (experimental) The name of the domain where the user resides (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#user_domain_name OpenstackProvider#user_domain_name}
        :param user_id: (experimental) User ID to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#user_id OpenstackProvider#user_id}
        :param user_name: (experimental) Username to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#user_name OpenstackProvider#user_name}

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa7766783b81be27a420676a4163309be334ed16397314bfaf17c99028f5bf3d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = OpenstackProviderConfig(
            alias=alias,
            allow_reauth=allow_reauth,
            application_credential_id=application_credential_id,
            application_credential_name=application_credential_name,
            application_credential_secret=application_credential_secret,
            auth_url=auth_url,
            cacert_file=cacert_file,
            cert=cert,
            cloud=cloud,
            default_domain=default_domain,
            delayed_auth=delayed_auth,
            disable_no_cache_header=disable_no_cache_header,
            domain_id=domain_id,
            domain_name=domain_name,
            enable_logging=enable_logging,
            endpoint_overrides=endpoint_overrides,
            endpoint_type=endpoint_type,
            insecure=insecure,
            key=key,
            max_retries=max_retries,
            password=password,
            project_domain_id=project_domain_id,
            project_domain_name=project_domain_name,
            region=region,
            swauth=swauth,
            system_scope=system_scope,
            tenant_id=tenant_id,
            tenant_name=tenant_name,
            token=token,
            use_octavia=use_octavia,
            user_domain_id=user_domain_id,
            user_domain_name=user_domain_name,
            user_id=user_id,
            user_name=user_name,
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
        '''(experimental) Generates CDKTF code for importing a OpenstackProvider resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the OpenstackProvider to import.
        :param import_from_id: The id of the existing OpenstackProvider that should be imported. Refer to the {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the OpenstackProvider to import is found.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b94610c93d90785393b28410c4b91395e9e1ae3b6190f63f6452f3bc3e39f3f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="resetAllowReauth")
    def reset_allow_reauth(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetAllowReauth", []))

    @jsii.member(jsii_name="resetApplicationCredentialId")
    def reset_application_credential_id(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetApplicationCredentialId", []))

    @jsii.member(jsii_name="resetApplicationCredentialName")
    def reset_application_credential_name(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetApplicationCredentialName", []))

    @jsii.member(jsii_name="resetApplicationCredentialSecret")
    def reset_application_credential_secret(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetApplicationCredentialSecret", []))

    @jsii.member(jsii_name="resetAuthUrl")
    def reset_auth_url(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetAuthUrl", []))

    @jsii.member(jsii_name="resetCacertFile")
    def reset_cacert_file(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetCacertFile", []))

    @jsii.member(jsii_name="resetCert")
    def reset_cert(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetCert", []))

    @jsii.member(jsii_name="resetCloud")
    def reset_cloud(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetCloud", []))

    @jsii.member(jsii_name="resetDefaultDomain")
    def reset_default_domain(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetDefaultDomain", []))

    @jsii.member(jsii_name="resetDelayedAuth")
    def reset_delayed_auth(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetDelayedAuth", []))

    @jsii.member(jsii_name="resetDisableNoCacheHeader")
    def reset_disable_no_cache_header(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetDisableNoCacheHeader", []))

    @jsii.member(jsii_name="resetDomainId")
    def reset_domain_id(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetDomainId", []))

    @jsii.member(jsii_name="resetDomainName")
    def reset_domain_name(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetDomainName", []))

    @jsii.member(jsii_name="resetEnableLogging")
    def reset_enable_logging(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetEnableLogging", []))

    @jsii.member(jsii_name="resetEndpointOverrides")
    def reset_endpoint_overrides(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetEndpointOverrides", []))

    @jsii.member(jsii_name="resetEndpointType")
    def reset_endpoint_type(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetEndpointType", []))

    @jsii.member(jsii_name="resetInsecure")
    def reset_insecure(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetInsecure", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetMaxRetries")
    def reset_max_retries(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetMaxRetries", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetProjectDomainId")
    def reset_project_domain_id(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetProjectDomainId", []))

    @jsii.member(jsii_name="resetProjectDomainName")
    def reset_project_domain_name(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetProjectDomainName", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSwauth")
    def reset_swauth(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetSwauth", []))

    @jsii.member(jsii_name="resetSystemScope")
    def reset_system_scope(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetSystemScope", []))

    @jsii.member(jsii_name="resetTenantId")
    def reset_tenant_id(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetTenantId", []))

    @jsii.member(jsii_name="resetTenantName")
    def reset_tenant_name(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetTenantName", []))

    @jsii.member(jsii_name="resetToken")
    def reset_token(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetToken", []))

    @jsii.member(jsii_name="resetUseOctavia")
    def reset_use_octavia(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetUseOctavia", []))

    @jsii.member(jsii_name="resetUserDomainId")
    def reset_user_domain_id(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetUserDomainId", []))

    @jsii.member(jsii_name="resetUserDomainName")
    def reset_user_domain_name(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetUserDomainName", []))

    @jsii.member(jsii_name="resetUserId")
    def reset_user_id(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetUserId", []))

    @jsii.member(jsii_name="resetUserName")
    def reset_user_name(self) -> None:
        '''
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "resetUserName", []))

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
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property
    @jsii.member(jsii_name="allowReauthInput")
    def allow_reauth_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowReauthInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationCredentialIdInput")
    def application_credential_id_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationCredentialIdInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationCredentialNameInput")
    def application_credential_name_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationCredentialNameInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationCredentialSecretInput")
    def application_credential_secret_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationCredentialSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="authUrlInput")
    def auth_url_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="cacertFileInput")
    def cacert_file_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacertFileInput"))

    @builtins.property
    @jsii.member(jsii_name="certInput")
    def cert_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudInput")
    def cloud_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultDomainInput")
    def default_domain_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="delayedAuthInput")
    def delayed_auth_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "delayedAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="disableNoCacheHeaderInput")
    def disable_no_cache_header_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableNoCacheHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="domainIdInput")
    def domain_id_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainIdInput"))

    @builtins.property
    @jsii.member(jsii_name="domainNameInput")
    def domain_name_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enableLoggingInput")
    def enable_logging_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableLoggingInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointOverridesInput")
    def endpoint_overrides_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "endpointOverridesInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointTypeInput")
    def endpoint_type_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="insecureInput")
    def insecure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "insecureInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRetriesInput")
    def max_retries_input(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRetriesInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="projectDomainIdInput")
    def project_domain_id_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectDomainIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectDomainNameInput")
    def project_domain_name_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectDomainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="swauthInput")
    def swauth_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "swauthInput"))

    @builtins.property
    @jsii.member(jsii_name="systemScopeInput")
    def system_scope_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "systemScopeInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantIdInput")
    def tenant_id_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantNameInput")
    def tenant_name_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenInput")
    def token_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenInput"))

    @builtins.property
    @jsii.member(jsii_name="useOctaviaInput")
    def use_octavia_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useOctaviaInput"))

    @builtins.property
    @jsii.member(jsii_name="userDomainIdInput")
    def user_domain_id_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userDomainIdInput"))

    @builtins.property
    @jsii.member(jsii_name="userDomainNameInput")
    def user_domain_name_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userDomainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="userIdInput")
    def user_id_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userIdInput"))

    @builtins.property
    @jsii.member(jsii_name="userNameInput")
    def user_name_input(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userNameInput"))

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a08fda273619419d4f717969c888e64079b23c3938bc3f3e5ea1f7637cc5acd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value)

    @builtins.property
    @jsii.member(jsii_name="allowReauth")
    def allow_reauth(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowReauth"))

    @allow_reauth.setter
    def allow_reauth(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d556fd3ae6656bd3f083c0ee04018f54dda0fabf7707bcf6f88ec09a4ad9e845)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowReauth", value)

    @builtins.property
    @jsii.member(jsii_name="applicationCredentialId")
    def application_credential_id(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationCredentialId"))

    @application_credential_id.setter
    def application_credential_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cc3000752f18bdd6fd564810b58ff4173464f69347a1ecf3f8ff3cfc2ff9c73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationCredentialId", value)

    @builtins.property
    @jsii.member(jsii_name="applicationCredentialName")
    def application_credential_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationCredentialName"))

    @application_credential_name.setter
    def application_credential_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__215e63597ccf5df07c7b6dd07122e51344a7839a03108962a005b4623ddd42be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationCredentialName", value)

    @builtins.property
    @jsii.member(jsii_name="applicationCredentialSecret")
    def application_credential_secret(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationCredentialSecret"))

    @application_credential_secret.setter
    def application_credential_secret(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d2a335bcb3eea8239c2efc94f03f362c1b498d741b78689de35c21cbbf457f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationCredentialSecret", value)

    @builtins.property
    @jsii.member(jsii_name="authUrl")
    def auth_url(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authUrl"))

    @auth_url.setter
    def auth_url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c42eeddd45420130839ce2fcce3e396019f9c2a8879c6e56feec2e6f20edcb6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authUrl", value)

    @builtins.property
    @jsii.member(jsii_name="cacertFile")
    def cacert_file(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacertFile"))

    @cacert_file.setter
    def cacert_file(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c4ffaca3088b4b747ff0abb1841ebd0be296bdde0a3d92b9a09f245d9ab5ef0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacertFile", value)

    @builtins.property
    @jsii.member(jsii_name="cert")
    def cert(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cert"))

    @cert.setter
    def cert(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56f19770a3c7b180d3decd8bc844d093ef585dc4e7fb52077e859fb31e381215)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cert", value)

    @builtins.property
    @jsii.member(jsii_name="cloud")
    def cloud(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloud"))

    @cloud.setter
    def cloud(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd76619f9f1a0210695f02eda5e2189a7cfbb000d63729ddb826fa766241e1de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloud", value)

    @builtins.property
    @jsii.member(jsii_name="defaultDomain")
    def default_domain(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultDomain"))

    @default_domain.setter
    def default_domain(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcdad966f1f58aeca8b3c7c6f8583ed3cb8ace9e019a7017698e11a1e6f75ac7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultDomain", value)

    @builtins.property
    @jsii.member(jsii_name="delayedAuth")
    def delayed_auth(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "delayedAuth"))

    @delayed_auth.setter
    def delayed_auth(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eb1cfdff12a5586dcfcd21c941e702912435d8832cf214018425c6c538a7b3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delayedAuth", value)

    @builtins.property
    @jsii.member(jsii_name="disableNoCacheHeader")
    def disable_no_cache_header(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableNoCacheHeader"))

    @disable_no_cache_header.setter
    def disable_no_cache_header(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a40d975be6a60e255a013b5deab99370795fc3c19129159569e9abfe430bd25d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableNoCacheHeader", value)

    @builtins.property
    @jsii.member(jsii_name="domainId")
    def domain_id(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainId"))

    @domain_id.setter
    def domain_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ad163016b5d6cc45f5f2564b5447d3bf2c29467fb1a64aa39e78afb5c3ffa98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainId", value)

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c03b27d6d2bed2344e6874041826c66c6786ebbbd5662e4cd77a8d7b712a65c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value)

    @builtins.property
    @jsii.member(jsii_name="enableLogging")
    def enable_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableLogging"))

    @enable_logging.setter
    def enable_logging(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__914d8ef5b8fb43873da90ee941c23081be2d2c2c4e700e268588c1f1824060d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableLogging", value)

    @builtins.property
    @jsii.member(jsii_name="endpointOverrides")
    def endpoint_overrides(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "endpointOverrides"))

    @endpoint_overrides.setter
    def endpoint_overrides(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7903876c1659551ff3a61292e00a3eb7b9931cd1206dbeab1e2b5925afc071c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointOverrides", value)

    @builtins.property
    @jsii.member(jsii_name="endpointType")
    def endpoint_type(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointType"))

    @endpoint_type.setter
    def endpoint_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21cdaf9b618e903633f2eda774d3fd45e39f424e8c9dbb873dc1fabf048b0eca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointType", value)

    @builtins.property
    @jsii.member(jsii_name="insecure")
    def insecure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "insecure"))

    @insecure.setter
    def insecure(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93ea6989ed5c5c6242dc0702eef53fd5f7adf91769245895983e054de6950cdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insecure", value)

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "key"))

    @key.setter
    def key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad56c5128e44b39529669d4697f8259e2b5c62cb822729a80077f0b4bfe2071f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="maxRetries")
    def max_retries(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRetries"))

    @max_retries.setter
    def max_retries(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72783e15d6b3c63b55b2896925764d865c55a7a4ab2d7410c84d7ac253e27495)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRetries", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "password"))

    @password.setter
    def password(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a3e69f3580e37ef20388d064715663c6d3696d92a5a6ddddd9faaf59616cf5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="projectDomainId")
    def project_domain_id(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectDomainId"))

    @project_domain_id.setter
    def project_domain_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a44a49c5b42abc9fd1d415fb57bdda20d0e006f75653b62e365085e142f019f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectDomainId", value)

    @builtins.property
    @jsii.member(jsii_name="projectDomainName")
    def project_domain_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectDomainName"))

    @project_domain_name.setter
    def project_domain_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a52b817b130d830c7db2086da12e3a2a1568e072afa31ae478bcf782a1d1957e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectDomainName", value)

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "region"))

    @region.setter
    def region(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2762e3d5632ec1940dc1c332e82ba7bbe6457c48cf3bb4d22021a71f66426bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value)

    @builtins.property
    @jsii.member(jsii_name="swauth")
    def swauth(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "swauth"))

    @swauth.setter
    def swauth(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b1d70d846c2f5060f27e1f01c9c869d852310b30b3de0f77a2b63626ef6a2ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "swauth", value)

    @builtins.property
    @jsii.member(jsii_name="systemScope")
    def system_scope(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "systemScope"))

    @system_scope.setter
    def system_scope(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95d88d362d7a4282380f5d586ccde6a496f5cd429735b3e21c8b3592a2e35ee9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "systemScope", value)

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e031c7f368fa0a4184653a55bb40ffb538c5e1a94bf980fa69a41f0a0dde2c52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantId", value)

    @builtins.property
    @jsii.member(jsii_name="tenantName")
    def tenant_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantName"))

    @tenant_name.setter
    def tenant_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dccd8f99e4c38108f4e288551d222bd26d44eb19bc1565ec5ac9d1af479a73b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantName", value)

    @builtins.property
    @jsii.member(jsii_name="token")
    def token(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "token"))

    @token.setter
    def token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6d23e5c35fee62e09f8e2d4ea7177442af8c64f0010359bf79f0b9c78a3ce31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "token", value)

    @builtins.property
    @jsii.member(jsii_name="useOctavia")
    def use_octavia(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useOctavia"))

    @use_octavia.setter
    def use_octavia(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3125f2ac0b478e9d94c4cc223442fa74ebc6a8cb8e76a89a8e4a5cb8426e2274)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useOctavia", value)

    @builtins.property
    @jsii.member(jsii_name="userDomainId")
    def user_domain_id(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userDomainId"))

    @user_domain_id.setter
    def user_domain_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cb9cb5c891d986274f2b148a0635f7743308438436b372d5c5040d4ad936216)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userDomainId", value)

    @builtins.property
    @jsii.member(jsii_name="userDomainName")
    def user_domain_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userDomainName"))

    @user_domain_name.setter
    def user_domain_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19bf68d2acf4100dd063f0e5e423df583a5349b2a58bb8b4eeca3cefb50ad85d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userDomainName", value)

    @builtins.property
    @jsii.member(jsii_name="userId")
    def user_id(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userId"))

    @user_id.setter
    def user_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5184e715936b953e5262d1dee5a7e5f88dbb536150d67ba9929f697ccba08669)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userId", value)

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userName"))

    @user_name.setter
    def user_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90bc7e6973d2b47a00bc0ab1daa554e457c780eae8946b94483ab6f5c3171dab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userName", value)


@jsii.data_type(
    jsii_type="@ithings/cdktf-provider-openstack.provider.OpenstackProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "alias": "alias",
        "allow_reauth": "allowReauth",
        "application_credential_id": "applicationCredentialId",
        "application_credential_name": "applicationCredentialName",
        "application_credential_secret": "applicationCredentialSecret",
        "auth_url": "authUrl",
        "cacert_file": "cacertFile",
        "cert": "cert",
        "cloud": "cloud",
        "default_domain": "defaultDomain",
        "delayed_auth": "delayedAuth",
        "disable_no_cache_header": "disableNoCacheHeader",
        "domain_id": "domainId",
        "domain_name": "domainName",
        "enable_logging": "enableLogging",
        "endpoint_overrides": "endpointOverrides",
        "endpoint_type": "endpointType",
        "insecure": "insecure",
        "key": "key",
        "max_retries": "maxRetries",
        "password": "password",
        "project_domain_id": "projectDomainId",
        "project_domain_name": "projectDomainName",
        "region": "region",
        "swauth": "swauth",
        "system_scope": "systemScope",
        "tenant_id": "tenantId",
        "tenant_name": "tenantName",
        "token": "token",
        "use_octavia": "useOctavia",
        "user_domain_id": "userDomainId",
        "user_domain_name": "userDomainName",
        "user_id": "userId",
        "user_name": "userName",
    },
)
class OpenstackProviderConfig:
    def __init__(
        self,
        *,
        alias: typing.Optional[builtins.str] = None,
        allow_reauth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        application_credential_id: typing.Optional[builtins.str] = None,
        application_credential_name: typing.Optional[builtins.str] = None,
        application_credential_secret: typing.Optional[builtins.str] = None,
        auth_url: typing.Optional[builtins.str] = None,
        cacert_file: typing.Optional[builtins.str] = None,
        cert: typing.Optional[builtins.str] = None,
        cloud: typing.Optional[builtins.str] = None,
        default_domain: typing.Optional[builtins.str] = None,
        delayed_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_no_cache_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        domain_id: typing.Optional[builtins.str] = None,
        domain_name: typing.Optional[builtins.str] = None,
        enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        endpoint_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        endpoint_type: typing.Optional[builtins.str] = None,
        insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key: typing.Optional[builtins.str] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        password: typing.Optional[builtins.str] = None,
        project_domain_id: typing.Optional[builtins.str] = None,
        project_domain_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        swauth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        system_scope: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        tenant_name: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        use_octavia: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        user_domain_id: typing.Optional[builtins.str] = None,
        user_domain_name: typing.Optional[builtins.str] = None,
        user_id: typing.Optional[builtins.str] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param alias: (experimental) Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#alias OpenstackProvider#alias}
        :param allow_reauth: (experimental) If set to ``false``, OpenStack authorization won't be perfomed automatically, if the initial auth token get expired. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#allow_reauth OpenstackProvider#allow_reauth}
        :param application_credential_id: (experimental) Application Credential ID to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#application_credential_id OpenstackProvider#application_credential_id}
        :param application_credential_name: (experimental) Application Credential name to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#application_credential_name OpenstackProvider#application_credential_name}
        :param application_credential_secret: (experimental) Application Credential secret to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#application_credential_secret OpenstackProvider#application_credential_secret}
        :param auth_url: (experimental) The Identity authentication URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#auth_url OpenstackProvider#auth_url}
        :param cacert_file: (experimental) A Custom CA certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#cacert_file OpenstackProvider#cacert_file}
        :param cert: (experimental) A client certificate to authenticate with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#cert OpenstackProvider#cert}
        :param cloud: (experimental) An entry in a ``clouds.yaml`` file to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#cloud OpenstackProvider#cloud}
        :param default_domain: (experimental) The name of the Domain ID to scope to if no other domain is specified. Defaults to ``default`` (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#default_domain OpenstackProvider#default_domain}
        :param delayed_auth: (experimental) If set to ``false``, OpenStack authorization will be perfomed, every time the service provider client is called. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#delayed_auth OpenstackProvider#delayed_auth}
        :param disable_no_cache_header: (experimental) If set to ``true``, the HTTP ``Cache-Control: no-cache`` header will not be added by default to all API requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#disable_no_cache_header OpenstackProvider#disable_no_cache_header}
        :param domain_id: (experimental) The ID of the Domain to scope to (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#domain_id OpenstackProvider#domain_id}
        :param domain_name: (experimental) The name of the Domain to scope to (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#domain_name OpenstackProvider#domain_name}
        :param enable_logging: (experimental) Outputs very verbose logs with all calls made to and responses from OpenStack. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#enable_logging OpenstackProvider#enable_logging}
        :param endpoint_overrides: (experimental) A map of services with an endpoint to override what was from the Keystone catalog. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#endpoint_overrides OpenstackProvider#endpoint_overrides}
        :param endpoint_type: (experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#endpoint_type OpenstackProvider#endpoint_type}.
        :param insecure: (experimental) Trust self-signed certificates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#insecure OpenstackProvider#insecure}
        :param key: (experimental) A client private key to authenticate with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#key OpenstackProvider#key}
        :param max_retries: (experimental) How many times HTTP connection should be retried until giving up. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#max_retries OpenstackProvider#max_retries}
        :param password: (experimental) Password to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#password OpenstackProvider#password}
        :param project_domain_id: (experimental) The ID of the domain where the proejct resides (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#project_domain_id OpenstackProvider#project_domain_id}
        :param project_domain_name: (experimental) The name of the domain where the project resides (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#project_domain_name OpenstackProvider#project_domain_name}
        :param region: (experimental) The OpenStack region to connect to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#region OpenstackProvider#region}
        :param swauth: (experimental) Use Swift's authentication system instead of Keystone. Only used for interaction with Swift. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#swauth OpenstackProvider#swauth}
        :param system_scope: (experimental) If set to ``true``, system scoped authorization will be enabled. Defaults to ``false`` (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#system_scope OpenstackProvider#system_scope}
        :param tenant_id: (experimental) The ID of the Tenant (Identity v2) or Project (Identity v3) to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#tenant_id OpenstackProvider#tenant_id}
        :param tenant_name: (experimental) The name of the Tenant (Identity v2) or Project (Identity v3) to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#tenant_name OpenstackProvider#tenant_name}
        :param token: (experimental) Authentication token to use as an alternative to username/password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#token OpenstackProvider#token}
        :param use_octavia: (experimental) If set to ``true``, API requests will go the Load Balancer service (Octavia) instead of the Networking service (Neutron). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#use_octavia OpenstackProvider#use_octavia}
        :param user_domain_id: (experimental) The ID of the domain where the user resides (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#user_domain_id OpenstackProvider#user_domain_id}
        :param user_domain_name: (experimental) The name of the domain where the user resides (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#user_domain_name OpenstackProvider#user_domain_name}
        :param user_id: (experimental) User ID to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#user_id OpenstackProvider#user_id}
        :param user_name: (experimental) Username to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#user_name OpenstackProvider#user_name}

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdd7a9f0ace1ef8b2d4ad8486b5ce64d3fc3b55ff5207ff74106d4831e4060a3)
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument allow_reauth", value=allow_reauth, expected_type=type_hints["allow_reauth"])
            check_type(argname="argument application_credential_id", value=application_credential_id, expected_type=type_hints["application_credential_id"])
            check_type(argname="argument application_credential_name", value=application_credential_name, expected_type=type_hints["application_credential_name"])
            check_type(argname="argument application_credential_secret", value=application_credential_secret, expected_type=type_hints["application_credential_secret"])
            check_type(argname="argument auth_url", value=auth_url, expected_type=type_hints["auth_url"])
            check_type(argname="argument cacert_file", value=cacert_file, expected_type=type_hints["cacert_file"])
            check_type(argname="argument cert", value=cert, expected_type=type_hints["cert"])
            check_type(argname="argument cloud", value=cloud, expected_type=type_hints["cloud"])
            check_type(argname="argument default_domain", value=default_domain, expected_type=type_hints["default_domain"])
            check_type(argname="argument delayed_auth", value=delayed_auth, expected_type=type_hints["delayed_auth"])
            check_type(argname="argument disable_no_cache_header", value=disable_no_cache_header, expected_type=type_hints["disable_no_cache_header"])
            check_type(argname="argument domain_id", value=domain_id, expected_type=type_hints["domain_id"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument enable_logging", value=enable_logging, expected_type=type_hints["enable_logging"])
            check_type(argname="argument endpoint_overrides", value=endpoint_overrides, expected_type=type_hints["endpoint_overrides"])
            check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
            check_type(argname="argument insecure", value=insecure, expected_type=type_hints["insecure"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument project_domain_id", value=project_domain_id, expected_type=type_hints["project_domain_id"])
            check_type(argname="argument project_domain_name", value=project_domain_name, expected_type=type_hints["project_domain_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument swauth", value=swauth, expected_type=type_hints["swauth"])
            check_type(argname="argument system_scope", value=system_scope, expected_type=type_hints["system_scope"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
            check_type(argname="argument tenant_name", value=tenant_name, expected_type=type_hints["tenant_name"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
            check_type(argname="argument use_octavia", value=use_octavia, expected_type=type_hints["use_octavia"])
            check_type(argname="argument user_domain_id", value=user_domain_id, expected_type=type_hints["user_domain_id"])
            check_type(argname="argument user_domain_name", value=user_domain_name, expected_type=type_hints["user_domain_name"])
            check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alias is not None:
            self._values["alias"] = alias
        if allow_reauth is not None:
            self._values["allow_reauth"] = allow_reauth
        if application_credential_id is not None:
            self._values["application_credential_id"] = application_credential_id
        if application_credential_name is not None:
            self._values["application_credential_name"] = application_credential_name
        if application_credential_secret is not None:
            self._values["application_credential_secret"] = application_credential_secret
        if auth_url is not None:
            self._values["auth_url"] = auth_url
        if cacert_file is not None:
            self._values["cacert_file"] = cacert_file
        if cert is not None:
            self._values["cert"] = cert
        if cloud is not None:
            self._values["cloud"] = cloud
        if default_domain is not None:
            self._values["default_domain"] = default_domain
        if delayed_auth is not None:
            self._values["delayed_auth"] = delayed_auth
        if disable_no_cache_header is not None:
            self._values["disable_no_cache_header"] = disable_no_cache_header
        if domain_id is not None:
            self._values["domain_id"] = domain_id
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if enable_logging is not None:
            self._values["enable_logging"] = enable_logging
        if endpoint_overrides is not None:
            self._values["endpoint_overrides"] = endpoint_overrides
        if endpoint_type is not None:
            self._values["endpoint_type"] = endpoint_type
        if insecure is not None:
            self._values["insecure"] = insecure
        if key is not None:
            self._values["key"] = key
        if max_retries is not None:
            self._values["max_retries"] = max_retries
        if password is not None:
            self._values["password"] = password
        if project_domain_id is not None:
            self._values["project_domain_id"] = project_domain_id
        if project_domain_name is not None:
            self._values["project_domain_name"] = project_domain_name
        if region is not None:
            self._values["region"] = region
        if swauth is not None:
            self._values["swauth"] = swauth
        if system_scope is not None:
            self._values["system_scope"] = system_scope
        if tenant_id is not None:
            self._values["tenant_id"] = tenant_id
        if tenant_name is not None:
            self._values["tenant_name"] = tenant_name
        if token is not None:
            self._values["token"] = token
        if use_octavia is not None:
            self._values["use_octavia"] = use_octavia
        if user_domain_id is not None:
            self._values["user_domain_id"] = user_domain_id
        if user_domain_name is not None:
            self._values["user_domain_name"] = user_domain_name
        if user_id is not None:
            self._values["user_id"] = user_id
        if user_name is not None:
            self._values["user_name"] = user_name

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''(experimental) Alias name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#alias OpenstackProvider#alias}

        :stability: experimental
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allow_reauth(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''(experimental) If set to ``false``, OpenStack authorization won't be perfomed automatically, if the initial auth token get expired. Defaults to ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#allow_reauth OpenstackProvider#allow_reauth}

        :stability: experimental
        '''
        result = self._values.get("allow_reauth")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def application_credential_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Application Credential ID to login with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#application_credential_id OpenstackProvider#application_credential_id}

        :stability: experimental
        '''
        result = self._values.get("application_credential_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_credential_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Application Credential name to login with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#application_credential_name OpenstackProvider#application_credential_name}

        :stability: experimental
        '''
        result = self._values.get("application_credential_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_credential_secret(self) -> typing.Optional[builtins.str]:
        '''(experimental) Application Credential secret to login with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#application_credential_secret OpenstackProvider#application_credential_secret}

        :stability: experimental
        '''
        result = self._values.get("application_credential_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auth_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) The Identity authentication URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#auth_url OpenstackProvider#auth_url}

        :stability: experimental
        '''
        result = self._values.get("auth_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cacert_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) A Custom CA certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#cacert_file OpenstackProvider#cacert_file}

        :stability: experimental
        '''
        result = self._values.get("cacert_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cert(self) -> typing.Optional[builtins.str]:
        '''(experimental) A client certificate to authenticate with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#cert OpenstackProvider#cert}

        :stability: experimental
        '''
        result = self._values.get("cert")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud(self) -> typing.Optional[builtins.str]:
        '''(experimental) An entry in a ``clouds.yaml`` file to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#cloud OpenstackProvider#cloud}

        :stability: experimental
        '''
        result = self._values.get("cloud")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_domain(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the Domain ID to scope to if no other domain is specified.

        Defaults to ``default`` (Identity v3).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#default_domain OpenstackProvider#default_domain}

        :stability: experimental
        '''
        result = self._values.get("default_domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delayed_auth(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''(experimental) If set to ``false``, OpenStack authorization will be perfomed, every time the service provider client is called. Defaults to ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#delayed_auth OpenstackProvider#delayed_auth}

        :stability: experimental
        '''
        result = self._values.get("delayed_auth")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_no_cache_header(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''(experimental) If set to ``true``, the HTTP ``Cache-Control: no-cache`` header will not be added by default to all API requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#disable_no_cache_header OpenstackProvider#disable_no_cache_header}

        :stability: experimental
        '''
        result = self._values.get("disable_no_cache_header")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def domain_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ID of the Domain to scope to (Identity v3).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#domain_id OpenstackProvider#domain_id}

        :stability: experimental
        '''
        result = self._values.get("domain_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the Domain to scope to (Identity v3).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#domain_name OpenstackProvider#domain_name}

        :stability: experimental
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''(experimental) Outputs very verbose logs with all calls made to and responses from OpenStack.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#enable_logging OpenstackProvider#enable_logging}

        :stability: experimental
        '''
        result = self._values.get("enable_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def endpoint_overrides(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) A map of services with an endpoint to override what was from the Keystone catalog.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#endpoint_overrides OpenstackProvider#endpoint_overrides}

        :stability: experimental
        '''
        result = self._values.get("endpoint_overrides")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def endpoint_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#endpoint_type OpenstackProvider#endpoint_type}.

        :stability: experimental
        '''
        result = self._values.get("endpoint_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insecure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''(experimental) Trust self-signed certificates.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#insecure OpenstackProvider#insecure}

        :stability: experimental
        '''
        result = self._values.get("insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''(experimental) A client private key to authenticate with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#key OpenstackProvider#key}

        :stability: experimental
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        '''(experimental) How many times HTTP connection should be retried until giving up.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#max_retries OpenstackProvider#max_retries}

        :stability: experimental
        '''
        result = self._values.get("max_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''(experimental) Password to login with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#password OpenstackProvider#password}

        :stability: experimental
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_domain_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ID of the domain where the proejct resides (Identity v3).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#project_domain_id OpenstackProvider#project_domain_id}

        :stability: experimental
        '''
        result = self._values.get("project_domain_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_domain_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the domain where the project resides (Identity v3).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#project_domain_name OpenstackProvider#project_domain_name}

        :stability: experimental
        '''
        result = self._values.get("project_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The OpenStack region to connect to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#region OpenstackProvider#region}

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def swauth(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''(experimental) Use Swift's authentication system instead of Keystone. Only used for interaction with Swift.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#swauth OpenstackProvider#swauth}

        :stability: experimental
        '''
        result = self._values.get("swauth")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def system_scope(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''(experimental) If set to ``true``, system scoped authorization will be enabled. Defaults to ``false`` (Identity v3).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#system_scope OpenstackProvider#system_scope}

        :stability: experimental
        '''
        result = self._values.get("system_scope")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tenant_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ID of the Tenant (Identity v2) or Project (Identity v3) to login with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#tenant_id OpenstackProvider#tenant_id}

        :stability: experimental
        '''
        result = self._values.get("tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tenant_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the Tenant (Identity v2) or Project (Identity v3) to login with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#tenant_name OpenstackProvider#tenant_name}

        :stability: experimental
        '''
        result = self._values.get("tenant_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''(experimental) Authentication token to use as an alternative to username/password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#token OpenstackProvider#token}

        :stability: experimental
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_octavia(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''(experimental) If set to ``true``, API requests will go the Load Balancer service (Octavia) instead of the Networking service (Neutron).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#use_octavia OpenstackProvider#use_octavia}

        :stability: experimental
        '''
        result = self._values.get("use_octavia")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def user_domain_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ID of the domain where the user resides (Identity v3).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#user_domain_id OpenstackProvider#user_domain_id}

        :stability: experimental
        '''
        result = self._values.get("user_domain_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_domain_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the domain where the user resides (Identity v3).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#user_domain_name OpenstackProvider#user_domain_name}

        :stability: experimental
        '''
        result = self._values.get("user_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) User ID to login with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#user_id OpenstackProvider#user_id}

        :stability: experimental
        '''
        result = self._values.get("user_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Username to login with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.54.1/docs#user_name OpenstackProvider#user_name}

        :stability: experimental
        '''
        result = self._values.get("user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OpenstackProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "OpenstackProvider",
    "OpenstackProviderConfig",
]

publication.publish()

def _typecheckingstub__aa7766783b81be27a420676a4163309be334ed16397314bfaf17c99028f5bf3d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    alias: typing.Optional[builtins.str] = None,
    allow_reauth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    application_credential_id: typing.Optional[builtins.str] = None,
    application_credential_name: typing.Optional[builtins.str] = None,
    application_credential_secret: typing.Optional[builtins.str] = None,
    auth_url: typing.Optional[builtins.str] = None,
    cacert_file: typing.Optional[builtins.str] = None,
    cert: typing.Optional[builtins.str] = None,
    cloud: typing.Optional[builtins.str] = None,
    default_domain: typing.Optional[builtins.str] = None,
    delayed_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_no_cache_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    domain_id: typing.Optional[builtins.str] = None,
    domain_name: typing.Optional[builtins.str] = None,
    enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    endpoint_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    endpoint_type: typing.Optional[builtins.str] = None,
    insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key: typing.Optional[builtins.str] = None,
    max_retries: typing.Optional[jsii.Number] = None,
    password: typing.Optional[builtins.str] = None,
    project_domain_id: typing.Optional[builtins.str] = None,
    project_domain_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    swauth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    system_scope: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tenant_id: typing.Optional[builtins.str] = None,
    tenant_name: typing.Optional[builtins.str] = None,
    token: typing.Optional[builtins.str] = None,
    use_octavia: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    user_domain_id: typing.Optional[builtins.str] = None,
    user_domain_name: typing.Optional[builtins.str] = None,
    user_id: typing.Optional[builtins.str] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b94610c93d90785393b28410c4b91395e9e1ae3b6190f63f6452f3bc3e39f3f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a08fda273619419d4f717969c888e64079b23c3938bc3f3e5ea1f7637cc5acd8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d556fd3ae6656bd3f083c0ee04018f54dda0fabf7707bcf6f88ec09a4ad9e845(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cc3000752f18bdd6fd564810b58ff4173464f69347a1ecf3f8ff3cfc2ff9c73(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__215e63597ccf5df07c7b6dd07122e51344a7839a03108962a005b4623ddd42be(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d2a335bcb3eea8239c2efc94f03f362c1b498d741b78689de35c21cbbf457f9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c42eeddd45420130839ce2fcce3e396019f9c2a8879c6e56feec2e6f20edcb6c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c4ffaca3088b4b747ff0abb1841ebd0be296bdde0a3d92b9a09f245d9ab5ef0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56f19770a3c7b180d3decd8bc844d093ef585dc4e7fb52077e859fb31e381215(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd76619f9f1a0210695f02eda5e2189a7cfbb000d63729ddb826fa766241e1de(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcdad966f1f58aeca8b3c7c6f8583ed3cb8ace9e019a7017698e11a1e6f75ac7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eb1cfdff12a5586dcfcd21c941e702912435d8832cf214018425c6c538a7b3c(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a40d975be6a60e255a013b5deab99370795fc3c19129159569e9abfe430bd25d(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad163016b5d6cc45f5f2564b5447d3bf2c29467fb1a64aa39e78afb5c3ffa98(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c03b27d6d2bed2344e6874041826c66c6786ebbbd5662e4cd77a8d7b712a65c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__914d8ef5b8fb43873da90ee941c23081be2d2c2c4e700e268588c1f1824060d4(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7903876c1659551ff3a61292e00a3eb7b9931cd1206dbeab1e2b5925afc071c8(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21cdaf9b618e903633f2eda774d3fd45e39f424e8c9dbb873dc1fabf048b0eca(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93ea6989ed5c5c6242dc0702eef53fd5f7adf91769245895983e054de6950cdb(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad56c5128e44b39529669d4697f8259e2b5c62cb822729a80077f0b4bfe2071f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72783e15d6b3c63b55b2896925764d865c55a7a4ab2d7410c84d7ac253e27495(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a3e69f3580e37ef20388d064715663c6d3696d92a5a6ddddd9faaf59616cf5d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a44a49c5b42abc9fd1d415fb57bdda20d0e006f75653b62e365085e142f019f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a52b817b130d830c7db2086da12e3a2a1568e072afa31ae478bcf782a1d1957e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2762e3d5632ec1940dc1c332e82ba7bbe6457c48cf3bb4d22021a71f66426bf(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b1d70d846c2f5060f27e1f01c9c869d852310b30b3de0f77a2b63626ef6a2ad(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95d88d362d7a4282380f5d586ccde6a496f5cd429735b3e21c8b3592a2e35ee9(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e031c7f368fa0a4184653a55bb40ffb538c5e1a94bf980fa69a41f0a0dde2c52(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dccd8f99e4c38108f4e288551d222bd26d44eb19bc1565ec5ac9d1af479a73b5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d23e5c35fee62e09f8e2d4ea7177442af8c64f0010359bf79f0b9c78a3ce31(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3125f2ac0b478e9d94c4cc223442fa74ebc6a8cb8e76a89a8e4a5cb8426e2274(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cb9cb5c891d986274f2b148a0635f7743308438436b372d5c5040d4ad936216(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19bf68d2acf4100dd063f0e5e423df583a5349b2a58bb8b4eeca3cefb50ad85d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5184e715936b953e5262d1dee5a7e5f88dbb536150d67ba9929f697ccba08669(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90bc7e6973d2b47a00bc0ab1daa554e457c780eae8946b94483ab6f5c3171dab(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdd7a9f0ace1ef8b2d4ad8486b5ce64d3fc3b55ff5207ff74106d4831e4060a3(
    *,
    alias: typing.Optional[builtins.str] = None,
    allow_reauth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    application_credential_id: typing.Optional[builtins.str] = None,
    application_credential_name: typing.Optional[builtins.str] = None,
    application_credential_secret: typing.Optional[builtins.str] = None,
    auth_url: typing.Optional[builtins.str] = None,
    cacert_file: typing.Optional[builtins.str] = None,
    cert: typing.Optional[builtins.str] = None,
    cloud: typing.Optional[builtins.str] = None,
    default_domain: typing.Optional[builtins.str] = None,
    delayed_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_no_cache_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    domain_id: typing.Optional[builtins.str] = None,
    domain_name: typing.Optional[builtins.str] = None,
    enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    endpoint_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    endpoint_type: typing.Optional[builtins.str] = None,
    insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key: typing.Optional[builtins.str] = None,
    max_retries: typing.Optional[jsii.Number] = None,
    password: typing.Optional[builtins.str] = None,
    project_domain_id: typing.Optional[builtins.str] = None,
    project_domain_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    swauth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    system_scope: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tenant_id: typing.Optional[builtins.str] = None,
    tenant_name: typing.Optional[builtins.str] = None,
    token: typing.Optional[builtins.str] = None,
    use_octavia: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    user_domain_id: typing.Optional[builtins.str] = None,
    user_domain_name: typing.Optional[builtins.str] = None,
    user_id: typing.Optional[builtins.str] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
