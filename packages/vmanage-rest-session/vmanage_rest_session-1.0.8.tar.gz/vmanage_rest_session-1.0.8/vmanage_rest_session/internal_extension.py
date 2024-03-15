from .extension.others_health_check import HealthCheck
from .extension.administration_settings import AdministrationSettings
from .extension.administration_tenantManagement import AdministrationTenantManagement
from .extension.configuration_devices import ConfigurationDevices
from .extension.configuration_certificates import ConfigurationCertificates
from .extension.monitor_devices import MonitorDevices
from .extension.monitor_overview import MonitorOverview
from .extension.others_vmanage_internal import VmanageInternal
from .extension.tools_rediscoveryNetwork import ToolsRediscoverNetwork
from .extension.configuration_templates_deviceTemplates_createTemplates_cliTemplate import ConfigurationTemplatesCliTemplate
from .extension.configuration_templates_deviceTemplates_createTemplates_deviceTemplate import ConfigurationTemplatesDeviceTemplate

module_class_list = [
    HealthCheck,
    AdministrationSettings,
    AdministrationTenantManagement,
    ConfigurationDevices,
    ConfigurationCertificates,
    MonitorDevices,
    MonitorOverview,
    VmanageInternal,
    ToolsRediscoverNetwork,
    ConfigurationTemplatesCliTemplate,
    ConfigurationTemplatesDeviceTemplate,
]
