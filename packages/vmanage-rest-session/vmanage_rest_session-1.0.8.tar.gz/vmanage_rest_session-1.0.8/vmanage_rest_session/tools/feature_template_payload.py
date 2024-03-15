class FeatureTemplatePayload():
    @classmethod
    def tenant_resource_profile_payload(cls):
        payload = {
            "natSessionLimit": 15000,
            "vpn": 30,
            "ipv4RouteLimit": 15000,
            "ipv6RouteLimit": 15000,
            "ipv4RouteLimitThreshold": 80,
            "ipv6RouteLimitThreshold": 80,
            "ipv4RouteLimitType": "warning-threshold",
            "ipv6RouteLimitType": "warning-threshold",
            "tierName": "tenant_rp",
            "tlocs":
            [
                {
                    "color": "lte",
                    "encapsulation": "ipsec"
                },
                {
                    "color": "3g",
                    "encapsulation": "ipsec"
                },
                {
                    "color": "biz-internet",
                    "encapsulation": "ipsec"
                },
                {
                    "color": "blue",
                    "encapsulation": "ipsec"
                },
                {
                    "color": "bronze",
                    "encapsulation": "ipsec"
                },
                {
                    "color": "custom1",
                    "encapsulation": "ipsec"
                },
                {
                    "color": "custom2",
                    "encapsulation": "ipsec"
                },
                {
                    "color": "default",
                    "encapsulation": "ipsec"
                },
                {
                    "color": "gold",
                    "encapsulation": "ipsec"
                },
                {
                    "color": "green",
                    "encapsulation": "ipsec"
                },
                {
                    "color": "metro-ethernet",
                    "encapsulation": "ipsec"
                },
                {
                    "color": "mpls",
                    "encapsulation": "ipsec"
                },
                {
                    "color": "public-internet",
                    "encapsulation": "ipsec"
                },
                {
                    "color": "red",
                    "encapsulation": "ipsec"
                },
                {
                    "color": "silver",
                    "encapsulation": "ipsec"
                },
                {
                    "color": "private1",
                    "encapsulation": "ipsec"
                }
            ]
        }

        return payload

    @classmethod
    def cisco_system_payload(cls):
        payload = {
            "templateName": "name",
            "templateDescription": "desc",
            "templateType": "cisco_system",
            "deviceType": [],
            "templateMinVersion": "15.0.0",
            "templateDefinition":
            {
                "clock":
                {
                    "timezone":
                    {
                        "vipObjectType": "object",
                        "vipType": "ignore",
                        "vipValue": "UTC",
                        "vipVariableName": "system_timezone"
                    }
                },
                "gps-location":
                {
                    "latitude":
                    {
                        "vipObjectType": "object",
                        "vipType": "ignore",
                        "vipVariableName": "system_latitude"
                    },
                    "longitude":
                    {
                        "vipObjectType": "object",
                        "vipType": "ignore",
                        "vipVariableName": "system_longitude"
                    },
                    "geo-fencing":
                    {
                        "enable":
                        {
                            "vipObjectType": "object",
                            "vipType": "ignore",
                            "vipValue": "false"
                        },
                        "range":
                        {},
                        "sms":
                        {
                            "enable":
                            {},
                            "mobile-number":
                            {
                                "vipType": "ignore",
                                "vipValue":
                                []
                            }
                        }
                    }
                },
                "location":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipVariableName": "system_location"
                },
                "track-transport":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipValue": "true",
                    "vipVariableName": "system_track_transport"
                },
                "track-interface-tag":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipVariableName": "system_track_interface_tag"
                },
                "port-offset":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipValue": 0,
                    "vipVariableName": "system_port_offset"
                },
                "port-hop":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipValue": "true",
                    "vipVariableName": "system_port_hop"
                },
                "control-session-pps":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipValue": 300,
                    "vipVariableName": "system_control_session_pps"
                },
                "description":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipVariableName": "system_description"
                },
                "device-groups":
                {
                    "vipObjectType": "list",
                    "vipType": "ignore",
                    "vipVariableName": "system_device_groups"
                },
                "controller-group-list":
                {
                    "vipObjectType": "list",
                    "vipType": "ignore",
                    "vipVariableName": "system_controller_group_list"
                },
                "site-id":
                {
                    "vipObjectType": "object",
                    "vipType": "constant",
                    "vipValue": 0,
                    "vipVariableName": "system_site_id"
                },
                "overlay-id":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipValue": 1,
                    "vipVariableName": "system_overlay_id"
                },
                "system-ip":
                {
                    "vipObjectType": "object",
                    "vipType": "variableName",
                    "vipValue": "",
                    "vipVariableName": "system_system_ip"
                },
                "host-name":
                {
                    "vipObjectType": "object",
                    "vipType": "variableName",
                    "vipValue": "",
                    "vipVariableName": "system_host_name"
                },
                "console-baud-rate":
                {
                    "vipObjectType": "object",
                    "vipType": "notIgnore",
                    "vipValue": "9600",
                    "vipVariableName": "system_console_baud_rate"
                },
                "max-omp-sessions":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipVariableName": "system_max_omp_sessions"
                },
                "track-default-gateway":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipValue": "true",
                    "vipVariableName": "system_track_default_gateway"
                },
                "idle-timeout":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipVariableName": "system_idle-timeout"
                },
                "admin-tech-on-failure":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipValue": "true",
                    "vipVariableName": "system_admin_tech_on_failure"
                },
                "site-type":
                {
                    "vipObjectType": "list",
                    "vipType": "ignore",
                    "vipVariableName": "system_site_type"
                },
                "multi-tenant":
                {
                    "vipObjectType": "node-only",
                    "vipType": "constant",
                    "vipValue": "true",
                    "vipVariableName": "system_multi-tenant"
                },
                "on-demand":
                {
                    "enable":
                    {
                        "vipObjectType": "object",
                        "vipType": "ignore",
                        "vipValue": "false",
                        "vipVariableName": "system_on-demand-enable"
                    },
                    "idle-timeout":
                    {
                        "vipObjectType": "object",
                        "vipType": "ignore",
                        "vipValue": 10,
                        "vipVariableName": "system_on-demand-idle-timeout"
                    }
                },
                "region-id":
                {},
                "secondary-region":
                {},
                "role":
                {},
                "affinity-group":
                {
                    "affinity-group-number":
                    {
                        "vipObjectType": "object",
                        "vipType": "ignore",
                        "vipVariableName": "system_affinity_group_number"
                    },
                    "preference":
                    {
                        "vipObjectType": "list",
                        "vipType": "ignore",
                        "vipVariableName": "system_affinity_group_preference"
                    },
                    "preference-auto":
                    {
                        "vipObjectType": "object",
                        "vipType": "ignore",
                        "vipValue": "false",
                        "vipVariableName": "system_affinity_group_preference_auto"
                    },
                    "affinity-per-vrf":
                    {
                        "vipObjectType": "tree",
                        "vipType": "ignore",
                        "vipValue":
                        [],
                        "vipPrimaryKey":
                        [
                            "affinity-group-number"
                        ]
                    }
                },
                "transport-gateway":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipValue": "false",
                    "vipVariableName": "system_transport_gateway"
                },
                "enable-mrf-migration":
                {},
                "migration-bgp-community":
                {},
                "enable-management-region":
                {},
                "management-region":
                {
                    "vrf":
                    {
                        "vipObjectType": "tree",
                        "vipType": "ignore",
                        "vipValue":
                        [],
                        "vipPrimaryKey":
                        [
                            "vrf-id"
                        ]
                    }
                },
                "management-gateway":
                {},
                "epfr":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipValue": "disabled",
                    "vipVariableName": "system_epfr"
                },
                "tracker":
                {
                    "vipType": "ignore",
                    "vipValue":
                    [],
                    "vipObjectType": "tree",
                    "vipPrimaryKey":
                    [
                        "name"
                    ]
                },
                "object-track":
                {
                    "vipType": "ignore",
                    "vipValue":
                    [],
                    "vipObjectType": "tree",
                    "vipPrimaryKey":
                    [
                        "object-number"
                    ]
                }
            },
            "factoryDefault": False
        }

        return payload

    @classmethod
    def cisco_tenant_payload(cls):
        payload = {
            "templateName": "name",
            "templateDescription": "desc",
            "templateType": "tenant",
            "deviceType": [],
            "templateMinVersion": "15.0.0",
            "templateDefinition":
            {
                "tenant":
                {
                    "vipType": "constant",
                    "vipValue": [],
                    "vipObjectType": "tree",
                    "vipPrimaryKey":
                    [
                        "org-name"
                    ]
                }
            },
            "factoryDefault": False
        }

        return payload
    
    @classmethod
    def _cisco_tenant_payload(cls):
        payload = {
            "org-name":
            {
                "vipObjectType": "object",
                "vipType": "constant",
                "vipValue": "name",
                "vipVariableName": "tenantOrgName_login"
            },
            "universal-unique-id":
            {
                "vipType": "constant",
                "vipValue": "id",
                "vipObjectType": "object"
            },
            "global-tenant-id":
            {
                "vipType": "constant",
                "vipValue": "id",
                "vipObjectType": "object"
            },
            "tier":
            {
                "tier-name":
                {
                    "vipObjectType": "object",
                    "vipType": "constant",
                    "vipValue": "tenant_rp"
                },
                "max-vpn":
                {
                    "vipType": "constant",
                    "vipValue": 30,
                    "vipObjectType": "object"
                },
                "max":
                {
                    "routes":
                    {
                        "address-family":
                        {
                            "ipv4":
                            {
                                "unicast-route-limit":
                                {
                                    "route-limit":
                                    {
                                        "vipType": "constant",
                                        "vipValue": 15000,
                                        "vipObjectType": "object"
                                    },
                                    "warning-only":
                                    {
                                        "vipType": "ignore",
                                        "vipValue": False,
                                        "vipObjectType": "node-only"
                                    },
                                    "warning-threshold":
                                    {
                                        "vipType": "constant",
                                        "vipValue": 80,
                                        "vipObjectType": "object"
                                    }
                                }
                            },
                            "ipv6":
                            {
                                "unicast-route-limit":
                                {
                                    "route-limit":
                                    {
                                        "vipType": "constant",
                                        "vipValue": 15000,
                                        "vipObjectType": "object"
                                    },
                                    "warning-only":
                                    {
                                        "vipType": "ignore",
                                        "vipValue": False,
                                        "vipObjectType": "node-only"
                                    },
                                    "warning-threshold":
                                    {
                                        "vipType": "constant",
                                        "vipValue": 80,
                                        "vipObjectType": "object"
                                    }
                                }
                            }
                        }
                    },
                    "nat-session":
                    {
                        "limit":
                        {
                            "key": "limit",
                            "description": "Maximum nat sessions allowed",
                            "details": "Maximum nat sessions allowed",
                            "optionType":
                            [
                                {
                                    "value": "constant",
                                    "display": "Global",
                                    "iconClass": "language",
                                    "iconColor": "icon-global"
                                }
                            ],
                            "originalDefaultOption": "constant",
                            "defaultOption": "constant",
                            "dataType":
                            {
                                "type": "number",
                                "min": 1,
                                "max": 4294967294
                            },
                            "dataPath":
                            [
                                "nat-session"
                            ],
                            "vipObjectType": "object",
                            "objectType": "object",
                            "deleteFlag": False,
                            "vipType": "constant",
                            "vipValue": 15000
                        }
                    }
                }
            },
            "tenant-tloc":
            {
                "vipType": "constant",
                "vipValue": 
                [
                    {
                        "color":
                        {
                            "vipType": "constant",
                            "vipValue": "lte",
                            "vipObjectType": "object"
                        },
                        "encap":
                        {
                            "vipType": "constant",
                            "vipValue": "ipsec",
                            "vipObjectType": "object"
                        },
                        "priority-order":
                        [
                            "color",
                            "encap"
                        ]
                    },
                    {
                        "color":
                        {
                            "vipType": "constant",
                            "vipValue": "3g",
                            "vipObjectType": "object"
                        },
                        "encap":
                        {
                            "vipType": "constant",
                            "vipValue": "ipsec",
                            "vipObjectType": "object"
                        },
                        "priority-order":
                        [
                            "color",
                            "encap"
                        ]
                    },
                    {
                        "color":
                        {
                            "vipType": "constant",
                            "vipValue": "biz-internet",
                            "vipObjectType": "object"
                        },
                        "encap":
                        {
                            "vipType": "constant",
                            "vipValue": "ipsec",
                            "vipObjectType": "object"
                        },
                        "priority-order":
                        [
                            "color",
                            "encap"
                        ]
                    },
                    {
                        "color":
                        {
                            "vipType": "constant",
                            "vipValue": "blue",
                            "vipObjectType": "object"
                        },
                        "encap":
                        {
                            "vipType": "constant",
                            "vipValue": "ipsec",
                            "vipObjectType": "object"
                        },
                        "priority-order":
                        [
                            "color",
                            "encap"
                        ]
                    },
                    {
                        "color":
                        {
                            "vipType": "constant",
                            "vipValue": "bronze",
                            "vipObjectType": "object"
                        },
                        "encap":
                        {
                            "vipType": "constant",
                            "vipValue": "ipsec",
                            "vipObjectType": "object"
                        },
                        "priority-order":
                        [
                            "color",
                            "encap"
                        ]
                    },
                    {
                        "color":
                        {
                            "vipType": "constant",
                            "vipValue": "custom1",
                            "vipObjectType": "object"
                        },
                        "encap":
                        {
                            "vipType": "constant",
                            "vipValue": "ipsec",
                            "vipObjectType": "object"
                        },
                        "priority-order":
                        [
                            "color",
                            "encap"
                        ]
                    },
                    {
                        "color":
                        {
                            "vipType": "constant",
                            "vipValue": "custom2",
                            "vipObjectType": "object"
                        },
                        "encap":
                        {
                            "vipType": "constant",
                            "vipValue": "ipsec",
                            "vipObjectType": "object"
                        },
                        "priority-order":
                        [
                            "color",
                            "encap"
                        ]
                    },
                    {
                        "color":
                        {
                            "vipType": "constant",
                            "vipValue": "default",
                            "vipObjectType": "object"
                        },
                        "encap":
                        {
                            "vipType": "constant",
                            "vipValue": "ipsec",
                            "vipObjectType": "object"
                        },
                        "priority-order":
                        [
                            "color",
                            "encap"
                        ]
                    },
                    {
                        "color":
                        {
                            "vipType": "constant",
                            "vipValue": "gold",
                            "vipObjectType": "object"
                        },
                        "encap":
                        {
                            "vipType": "constant",
                            "vipValue": "ipsec",
                            "vipObjectType": "object"
                        },
                        "priority-order":
                        [
                            "color",
                            "encap"
                        ]
                    },
                    {
                        "color":
                        {
                            "vipType": "constant",
                            "vipValue": "green",
                            "vipObjectType": "object"
                        },
                        "encap":
                        {
                            "vipType": "constant",
                            "vipValue": "ipsec",
                            "vipObjectType": "object"
                        },
                        "priority-order":
                        [
                            "color",
                            "encap"
                        ]
                    },
                    {
                        "color":
                        {
                            "vipType": "constant",
                            "vipValue": "metro-ethernet",
                            "vipObjectType": "object"
                        },
                        "encap":
                        {
                            "vipType": "constant",
                            "vipValue": "ipsec",
                            "vipObjectType": "object"
                        },
                        "priority-order":
                        [
                            "color",
                            "encap"
                        ]
                    },
                    {
                        "color":
                        {
                            "vipType": "constant",
                            "vipValue": "mpls",
                            "vipObjectType": "object"
                        },
                        "encap":
                        {
                            "vipType": "constant",
                            "vipValue": "ipsec",
                            "vipObjectType": "object"
                        },
                        "priority-order":
                        [
                            "color",
                            "encap"
                        ]
                    },
                    {
                        "color":
                        {
                            "vipType": "constant",
                            "vipValue": "public-internet",
                            "vipObjectType": "object"
                        },
                        "encap":
                        {
                            "vipType": "constant",
                            "vipValue": "ipsec",
                            "vipObjectType": "object"
                        },
                        "priority-order":
                        [
                            "color",
                            "encap"
                        ]
                    },
                    {
                        "color":
                        {
                            "vipType": "constant",
                            "vipValue": "red",
                            "vipObjectType": "object"
                        },
                        "encap":
                        {
                            "vipType": "constant",
                            "vipValue": "ipsec",
                            "vipObjectType": "object"
                        },
                        "priority-order":
                        [
                            "color",
                            "encap"
                        ]
                    },
                    {
                        "color":
                        {
                            "vipType": "constant",
                            "vipValue": "silver",
                            "vipObjectType": "object"
                        },
                        "encap":
                        {
                            "vipType": "constant",
                            "vipValue": "ipsec",
                            "vipObjectType": "object"
                        },
                        "priority-order":
                        [
                            "color",
                            "encap"
                        ]
                    },
                    {
                        "color":
                        {
                            "vipType": "constant",
                            "vipValue": "private1",
                            "vipObjectType": "object"
                        },
                        "encap":
                        {
                            "vipType": "constant",
                            "vipValue": "ipsec",
                            "vipObjectType": "object"
                        },
                        "priority-order":
                        [
                            "color",
                            "encap"
                        ]
                    },
                ],
                "vipPrimaryKey":
                [
                    "color",
                    "encap"
                ],
                "vipObjectType": "tree"
            },
            "priority-order":
            [
                "org-name",
                "universal-unique-id",
                "global-tenant-id",
                "tenant-tloc",
                "tier"
            ]
        }
        
        return payload

    @classmethod
    def _cisco_tenant_tloc_payload(cls):
        payload = {
            "color":
            {
                "vipType": "constant",
                "vipValue": "color",
                "vipObjectType": "object"
            },
            "encap":
            {
                "vipType": "constant",
                "vipValue": "ipsec",
                "vipObjectType": "object"
            },
            "priority-order":
            [
                "color",
                "encap"
            ]
        }
        
        return payload

    @classmethod
    def cisco_vpn_payload(cls):
        payload = {
            "templateName": "templateName",
            "templateDescription": "templateName",
            "templateType": "cisco_vpn",
            "deviceType": [],
            "templateMinVersion": "15.0.0",
            "templateDefinition":
            {
                "vpn-id":
                {
                    "vipObjectType": "object",
                    "vipType": "constant",
                    "vipValue": 0
                },
                "name":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipVariableName": "vpn_name"
                },
                "ecmp-hash-key":
                {
                    "layer4":
                    {
                        "vipObjectType": "object",
                        "vipType": "ignore",
                        "vipValue": "false",
                        "vipVariableName": "vpn_layer4"
                    }
                },
                "nat64-global":
                {
                    "prefix":
                    {
                        "stateful":
                        {}
                    }
                },
                "nat64":
                {
                    "v4":
                    {
                        "pool":
                        {
                            "vipType": "ignore",
                            "vipValue":
                            [],
                            "vipObjectType": "tree",
                            "vipPrimaryKey":
                            [
                                "name"
                            ]
                        }
                    }
                },
                "tenant-vpn-id":
                {
                    "vipObjectType": "object",
                    "vipType": "constant",
                    "vipValue": 1
                },
                "org-name":
                {
                    "vipObjectType": "object",
                    "vipType": "constant",
                    "vipValue": "tenantname"
                },
                "omp-admin-distance-ipv4":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipVariableName": "vpn_omp-admin-distance-ipv4"
                },
                "omp-admin-distance-ipv6":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipVariableName": "vpn_omp-admin-distance-ipv6"
                },
                "nat":
                {
                    "natpool":
                    {
                        "vipType": "ignore",
                        "vipValue":
                        [],
                        "vipObjectType": "tree",
                        "vipPrimaryKey":
                        [
                            "name"
                        ]
                    },
                    "port-forward":
                    {
                        "vipType": "ignore",
                        "vipValue":
                        [],
                        "vipObjectType": "tree",
                        "vipPrimaryKey":
                        [
                            "source-port",
                            "translate-port",
                            "source-ip",
                            "translate-ip",
                            "proto"
                        ]
                    },
                    "static":
                    {
                        "vipType": "ignore",
                        "vipValue":
                        [],
                        "vipObjectType": "tree",
                        "vipPrimaryKey":
                        [
                            "source-ip",
                            "translate-ip"
                        ]
                    },
                    "subnet-static":
                    {
                        "vipType": "ignore",
                        "vipValue":
                        [],
                        "vipObjectType": "tree",
                        "vipPrimaryKey":
                        [
                            "source-ip-subnet",
                            "translate-ip-subnet"
                        ]
                    }
                },
                "route-import-from":
                {
                    "vipType": "ignore",
                    "vipValue":
                    [],
                    "vipObjectType": "tree",
                    "vipPrimaryKey":
                    [
                        "protocol",
                        "source-vpn"
                    ]
                },
                "route-import":
                {
                    "vipType": "ignore",
                    "vipValue":
                    [],
                    "vipObjectType": "tree",
                    "vipPrimaryKey":
                    [
                        "protocol"
                    ]
                },
                "route-export":
                {
                    "vipType": "ignore",
                    "vipValue":
                    [],
                    "vipObjectType": "tree",
                    "vipPrimaryKey":
                    [
                        "protocol"
                    ]
                },
                "host":
                {
                    "vipType": "ignore",
                    "vipValue":
                    [],
                    "vipObjectType": "tree",
                    "vipPrimaryKey":
                    [
                        "hostname"
                    ]
                },
                "service":
                {
                    "vipType": "ignore",
                    "vipValue":
                    [],
                    "vipObjectType": "tree",
                    "vipPrimaryKey":
                    [
                        "svc-type"
                    ]
                },
                "ip":
                {
                    "route": 
                    {
                        "vipType": "constant",
                        "vipValue":
                        [
                            {
                                "prefix":
                                {
                                    "vipObjectType": "object",
                                    "vipType": "constant",
                                    "vipValue": "0.0.0.0/0",
                                    "vipVariableName": "vpn_ipv4_ip_prefix"
                                },
                                "next-hop":
                                {
                                    "vipType": "constant",
                                    "vipValue":
                                    [
                                        {
                                            "address":
                                            {
                                                "vipObjectType": "object",
                                                "vipType": "constant",
                                                "vipValue": "next_hop",
                                                "vipVariableName": "vpn_next_hop_ip_address_0"
                                            },
                                            "distance":
                                            {
                                                "vipObjectType": "object",
                                                "vipType": "ignore",
                                                "vipValue": 1,
                                                "vipVariableName": "vpn_next_hop_ip_distance_0"
                                            },
                                            "priority-order":
                                            [
                                                "address",
                                                "distance"
                                            ]
                                        }
                                    ],
                                    "vipObjectType": "tree",
                                    "vipPrimaryKey":
                                    [
                                        "address"
                                    ]
                                },
                                "priority-order":
                                [
                                    "prefix",
                                    "next-hop",
                                    "next-hop-with-track"
                                ]
                            }
                        ],
                        "vipObjectType": "tree",
                        "vipPrimaryKey":
                        [
                            "prefix"
                        ]
                    },
                    "gre-route":
                    {},
                    "ipsec-route":
                    {},
                    "service-route":
                    {}
                },
                "ipv6":
                {},
                "omp":
                {
                    "advertise":
                    {
                        "vipType": "ignore",
                        "vipValue":
                        [],
                        "vipObjectType": "tree",
                        "vipPrimaryKey":
                        [
                            "protocol"
                        ]
                    },
                    "ipv6-advertise":
                    {
                        "vipType": "ignore",
                        "vipValue":
                        [],
                        "vipObjectType": "tree",
                        "vipPrimaryKey":
                        [
                            "protocol"
                        ]
                    }
                }
            },
            "factoryDefault": False
        }

        return payload

    @classmethod
    def _ip_host_payload(cls):
        payload = {
            "hostname":
            {
                "vipObjectType": "object",
                "vipType": "constant",
                "vipValue": "vbond",
                "vipVariableName": "vpn_host_hostname"
            },
            "ip":
            {
                "vipObjectType": "list",
                "vipType": "constant",
                "vipValue": [],
                "vipVariableName": "vpn_host_ip"
            },
            "priority-order":
            [
                "hostname",
                "ip"
            ]
        }

        return payload

    @classmethod
    def cisco_vpn_interface_payload(cls):
        payload = {
            "templateName": "templateName",
            "templateDescription": "templateDescription",
            "templateType": "cisco_vpn_interface",
            "deviceType": [],
            "templateMinVersion": "15.0.0",
            "templateDefinition":
            {
                "if-name":
                {
                    "vipObjectType": "object",
                    "vipType": "constant",
                    "vipValue": "if-name",
                    "vipVariableName": "vpn_if_name"
                },
                "description":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipVariableName": "vpn_if_description"
                },
                "ip":
                {
                    "address":
                    {
                        "vipObjectType": "object",
                        "vipType": "constant",
                        "vipVariableName": "vpn_if_ipv4_address"
                    },
                    "secondary-address":
                    {
                        "vipType": "ignore",
                        "vipValue":
                        [],
                        "vipObjectType": "tree",
                        "vipPrimaryKey":
                        [
                            "address"
                        ]
                    }
                },
                "dhcp-helper":
                {
                    "vipObjectType": "list",
                    "vipType": "ignore",
                    "vipVariableName": "vpn_if_dhcp_helper"
                },
                "mtu":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipValue": 1500,
                    "vipVariableName": "vpn_if_ip_mtu"
                },
                "tcp-mss-adjust":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipVariableName": "vpn_if_tcp_mss_adjust"
                },
                "mac-address":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipVariableName": "vpn_if_mac_address"
                },
                "speed":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipValue": "_empty",
                    "vipVariableName": "vpn_if_speed"
                },
                "duplex":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipValue": "_empty",
                    "vipVariableName": "vpn_if_duplex"
                },
                "shutdown":
                {
                    "vipObjectType": "object",
                    "vipType": "constant",
                    "vipValue": "false",
                    "vipVariableName": "vpn_if_shutdown"
                },
                "arp-timeout":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipValue": 1200,
                    "vipVariableName": "vpn_if_arp_timeout"
                },
                "autonegotiate":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipVariableName": "vpn_if_autonegotiate"
                },
                "shaping-rate":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipVariableName": "rewrite_shaping_rate"
                },
                "qos-map":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipVariableName": "qos_map"
                },
                "qos-map-vpn":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipVariableName": "vpn-qos_map"
                },
                "tracker":
                {
                    "vipObjectType": "list",
                    "vipType": "ignore",
                    "vipVariableName": "vpn_if_tracker"
                },
                "bandwidth-upstream":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipVariableName": "vpn_if_bandwidth_upstream"
                },
                "bandwidth-downstream":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipVariableName": "vpn_if_bandwidth_downstream"
                },
                "block-non-source-ip":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipValue": "false",
                    "vipVariableName": "vpn_if_block_non_source_ip"
                },
                "rewrite-rule":
                {
                    "rule-name":
                    {
                        "vipObjectType": "object",
                        "vipType": "ignore",
                        "vipVariableName": "rewrite_rule_name"
                    }
                },
                "tloc-extension":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipVariableName": "vpn_if_tloc_extension"
                },
                "load-interval":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipValue": 30,
                    "vipVariableName": "vpn_if_load_interval"
                },
                "icmp-redirect-disable":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipValue": "true",
                    "vipVariableName": "vpn_if_icmp_redirect_disable"
                },
                "tloc-extension-gre-from":
                {
                    "src-ip":
                    {
                        "vipObjectType": "object",
                        "vipType": "ignore",
                        "vipVariableName": "vpn_if_tloc-ext_gre_from_src_ip"
                    },
                    "xconnect":
                    {
                        "vipObjectType": "object",
                        "vipType": "ignore",
                        "vipVariableName": "vpn_if_tloc-ext_gre_from_xconnect"
                    }
                },
                "access-list":
                {
                    "vipType": "ignore",
                    "vipValue":
                    [],
                    "vipObjectType": "tree",
                    "vipPrimaryKey":
                    [
                        "direction"
                    ]
                },
                "tunnel-interface":
                {
                    "encapsulation":
                    {
                        "vipType": "constant",
                        "vipValue":
                        [
                            {
                                "preference":
                                {
                                    "vipObjectType": "object",
                                    "vipType": "ignore",
                                    "vipVariableName": "vpn_if_tunnel_ipsec_preference"
                                },
                                "weight":
                                {
                                    "vipObjectType": "object",
                                    "vipType": "ignore",
                                    "vipValue": 1,
                                    "vipVariableName": "vpn_if_tunnel_ipsec_weight"
                                },
                                "encap":
                                {
                                    "vipType": "constant",
                                    "vipValue": "ipsec",
                                    "vipObjectType": "object"
                                },
                                "priority-order":
                                [
                                    "encap",
                                    "preference",
                                    "weight"
                                ]
                            }
                        ],
                        "vipObjectType": "tree",
                        "vipPrimaryKey":
                        [
                            "encap"
                        ]
                    },
                    "group":
                    {
                        "vipObjectType": "list",
                        "vipType": "ignore",
                        "vipVariableName": "vpn_if_tunnel_group"
                    },
                    "border":
                    {
                        "vipObjectType": "object",
                        "vipType": "ignore",
                        "vipValue": "false",
                        "vipVariableName": "vpn_if_tunnel_border"
                    },
                    "color":
                    {
                        "value":
                        {
                            "vipObjectType": "object",
                            "vipType": "constant",
                            "vipValue": "lte",
                            "vipVariableName": "vpn_if_tunnel_color_value"
                        },
                        "restrict":
                        {
                            "vipObjectType": "node-only",
                            "vipType": "ignore",
                            "vipValue": "false",
                            "vipVariableName": "vpn_if_tunnel_color_restrict"
                        }
                    },
                    "carrier":
                    {
                        "vipObjectType": "object",
                        "vipType": "ignore",
                        "vipValue": "default",
                        "vipVariableName": "vpn_if_tunnel_carrier"
                    },
                    "bind":
                    {
                        "vipObjectType": "object",
                        "vipType": "ignore",
                        "vipVariableName": "vpn_if_tunnel_bind"
                    },
                    "allow-service":
                    {
                        "dhcp":
                        {
                            "vipObjectType": "object",
                            "vipType": "ignore",
                            "vipValue": "true",
                            "vipVariableName": "vpn_if_tunnel_dhcp"
                        },
                        "dns":
                        {
                            "vipObjectType": "object",
                            "vipType": "ignore",
                            "vipValue": "true",
                            "vipVariableName": "vpn_if_tunnel_dns"
                        },
                        "icmp":
                        {
                            "vipObjectType": "object",
                            "vipType": "ignore",
                            "vipValue": "true",
                            "vipVariableName": "vpn_if_tunnel_icmp"
                        },
                        "sshd":
                        {
                            "vipObjectType": "object",
                            "vipType": "ignore",
                            "vipValue": "false",
                            "vipVariableName": "vpn_if_tunnel_sshd"
                        },
                        "ntp":
                        {
                            "vipObjectType": "object",
                            "vipType": "ignore",
                            "vipValue": "false",
                            "vipVariableName": "vpn_if_tunnel_ntp"
                        },
                        "stun":
                        {
                            "vipObjectType": "object",
                            "vipType": "ignore",
                            "vipValue": "false",
                            "vipVariableName": "vpn_if_tunnel_stun"
                        },
                        "all":
                        {
                            "vipObjectType": "object",
                            "vipType": "ignore",
                            "vipValue": "false",
                            "vipVariableName": "vpn_if_tunnel_all"
                        },
                        "bgp":
                        {
                            "vipObjectType": "object",
                            "vipType": "ignore",
                            "vipValue": "false",
                            "vipVariableName": "vpn_if_tunnel_bgp"
                        },
                        "ospf":
                        {
                            "vipObjectType": "object",
                            "vipType": "ignore",
                            "vipValue": "false",
                            "vipVariableName": "vpn_if_tunnel_ospf"
                        },
                        "netconf":
                        {
                            "vipObjectType": "object",
                            "vipType": "ignore",
                            "vipValue": "false",
                            "vipVariableName": "vpn_if_tunnel_netconf"
                        },
                        "snmp":
                        {
                            "vipObjectType": "object",
                            "vipType": "ignore",
                            "vipValue": "false",
                            "vipVariableName": "vpn_if_tunnel_snmp"
                        },
                        "https":
                        {
                            "vipObjectType": "object",
                            "vipType": "ignore",
                            "vipValue": "true",
                            "vipVariableName": "vpn_if_tunnel_https"
                        }
                    },
                    "max-control-connections":
                    {
                        "vipObjectType": "object",
                        "vipType": "ignore",
                        "vipVariableName": "vpn_if_tunnel_max_control_connections"
                    },
                    "vbond-as-stun-server":
                    {
                        "vipObjectType": "object",
                        "vipType": "ignore",
                        "vipValue": "false",
                        "vipVariableName": "vpn_if_tunnel_vbond_as_stun_server"
                    },
                    "exclude-controller-group-list":
                    {
                        "vipObjectType": "list",
                        "vipType": "ignore",
                        "vipVariableName": "vpn_if_tunnel_exclude_controller_group_list"
                    },
                    "vmanage-connection-preference":
                    {
                        "vipObjectType": "object",
                        "vipType": "ignore",
                        "vipValue": 5,
                        "vipVariableName": "vpn_if_tunnel_vmanage_connection_preference"
                    },
                    "port-hop":
                    {
                        "vipObjectType": "object",
                        "vipType": "ignore",
                        "vipValue": "true",
                        "vipVariableName": "vpn_if_tunnel_port_hop"
                    },
                    "low-bandwidth-link":
                    {
                        "vipObjectType": "object",
                        "vipType": "ignore",
                        "vipValue": "false",
                        "vipVariableName": "vpn_if_tunnel_low_bandwidth_link"
                    },
                    "last-resort-circuit":
                    {
                        "vipObjectType": "object",
                        "vipType": "ignore",
                        "vipValue": "false",
                        "vipVariableName": "vpn_if_tunnel_last_resort_circuit"
                    },
                    "nat-refresh-interval":
                    {
                        "vipObjectType": "object",
                        "vipType": "ignore",
                        "vipValue": 5,
                        "vipVariableName": "vpn_if_tunnel_nat_refresh_interval"
                    },
                    "hello-interval":
                    {
                        "vipObjectType": "object",
                        "vipType": "ignore",
                        "vipValue": 1000,
                        "vipVariableName": "vpn_if_tunnel_hello_interval"
                    },
                    "hello-tolerance":
                    {
                        "vipObjectType": "object",
                        "vipType": "ignore",
                        "vipValue": 12,
                        "vipVariableName": "vpn_if_tunnel_hello_tolerance"
                    },
                    "tloc-extension-gre-to":
                    {
                        "dst-ip":
                        {
                            "vipObjectType": "object",
                            "vipType": "ignore",
                            "vipVariableName": "vpn_if_tunnel_tloc_ext_gre_to_dst_ip"
                        }
                    },
                    "enable-core-region":
                    {
                        "vipObjectType": "object",
                        "vipType": "ignore",
                        "vipValue": "false"
                    },
                    "core-region":
                    {
                        "vipObjectType": "object",
                        "vipType": "ignore",
                        "vipValue": "core"
                    },
                    "secondary-region":
                    {
                        "vipObjectType": "object",
                        "vipType": "ignore",
                        "vipValue": "off"
                    },
                    "tunnel-tcp-mss-adjust":
                    {
                        "vipObjectType": "object",
                        "vipType": "ignore",
                        "vipVariableName": "vpn_if_tunnel_tunnel_tcp_mss_adjust"
                    },
                    "clear-dont-fragment":
                    {
                        "vipObjectType": "object",
                        "vipType": "ignore",
                        "vipValue": "false",
                        "vipVariableName": "vpn_if_tunnel_tunnel_clear_dont_fragment"
                    },
                    "propagate-sgt":
                    {
                        "vipObjectType": "object",
                        "vipType": "ignore",
                        "vipValue": "false",
                        "vipVariableName": "vpn_if_tunnel_tunnel_propagate_sgt"
                    },
                    "network-broadcast":
                    {
                        "vipObjectType": "object",
                        "vipType": "ignore",
                        "vipValue": "false",
                        "vipVariableName": "vpn_if_tunnel_tunnel_network_broadcast"
                    }
                },
                "auto-bandwidth-detect":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipValue": "false",
                    "vipVariableName": "vpn_if_auto_bandwidth_detect"
                },
                "iperf-server":
                {
                    "vipType": "ignore"
                },
                "media-type":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipValue": "_empty",
                    "vipVariableName": "vpn_if_media-type"
                },
                "intrf-mtu":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipValue": 1500,
                    "vipVariableName": "vpn_if_intrf_mtu"
                },
                "ip-directed-broadcast":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipValue": "false",
                    "vipVariableName": "vpn_if_ip-directed-broadcast"
                },
                "service-provider":
                {
                    "vipObjectType": "object",
                    "vipType": "ignore",
                    "vipVariableName": "vpn_if_service_provider"
                },
                "trustsec":
                {
                    "enforcement":
                    {
                        "enable":
                        {
                            "vipObjectType": "object",
                            "vipType": "ignore"
                        },
                        "sgt":
                        {
                            "vipObjectType": "object",
                            "vipType": "ignore",
                            "vipVariableName": "trusted_enforcement_sgt"
                        }
                    }
                },
                "ipv6":
                {
                    "access-list":
                    {
                        "vipType": "ignore",
                        "vipValue":
                        [],
                        "vipObjectType": "tree",
                        "vipPrimaryKey":
                        [
                            "direction"
                        ]
                    },
                    "address":
                    {
                        "vipObjectType": "object",
                        "vipType": "ignore",
                        "vipValue": "",
                        "vipVariableName": "vpn_if_ipv6_ipv6_address"
                    },
                    "dhcp-helper-v6":
                    {
                        "vipType": "ignore",
                        "vipValue":
                        [],
                        "vipObjectType": "tree",
                        "vipPrimaryKey":
                        [
                            "address"
                        ]
                    },
                    "secondary-address":
                    {
                        "vipType": "ignore",
                        "vipValue":
                        [],
                        "vipObjectType": "tree",
                        "vipPrimaryKey":
                        [
                            "address"
                        ]
                    }
                },
                "arp":
                {
                    "ip":
                    {
                        "vipType": "ignore",
                        "vipValue":
                        [],
                        "vipObjectType": "tree",
                        "vipPrimaryKey":
                        [
                            "addr"
                        ]
                    }
                },
                "vrrp":
                {
                    "vipType": "ignore",
                    "vipValue":
                    [],
                    "vipObjectType": "tree",
                    "vipPrimaryKey":
                    [
                        "grp-id"
                    ]
                },
                "ipv6-vrrp":
                {
                    "vipType": "ignore",
                    "vipValue":
                    [],
                    "vipObjectType": "tree",
                    "vipPrimaryKey":
                    [
                        "grp-id"
                    ]
                }
            },
            "factoryDefault": False
        }

        return payload

    @classmethod
    def device_template_payload(cls):
        payload = {
            "templateName": "test",
            "templateDescription": "test",
            "deviceType": "vedge-C8000V",
            "deviceRole": "sdwan-edge",
            "configType": "template",
            "factoryDefault": False,
            "policyId": "",
            "featureTemplateUidRange":
            [],
            "connectionPreferenceRequired": True,
            "connectionPreference": True,
            "generalTemplates":
            [
                {
                    "templateId": "f3706496-fb0a-4a69-b07b-736f54f4b8fa",
                    "templateType": "cedge_aaa"
                },
                {
                    "templateId": "b7ad3690-d66a-4395-a186-ec4e61d83041",
                    "templateType": "cisco_bfd"
                },
                {
                    "templateId": "ec9b102d-e1ef-44db-92af-667abaf5eb80",
                    "templateType": "cisco_omp"
                },
                {
                    "templateId": "c52de5c6-45b1-476a-92f2-8d67ecf43b32",
                    "templateType": "cisco_security"
                },
                #{
                #    "templateId": "38f5c0a7-b4c8-45d3-a86c-b53d52a7f26a",
                #    "templateType": "cisco_system",
                #    "subTemplates":
                #    [
                #        {
                #            "templateId": "1d77259b-0e17-49d2-9c64-93572a77ba48",
                #            "templateType": "cisco_logging"
                #        }
                #    ]
                #},
                #{
                #    "templateId": "92a0bd3f-27bc-4782-8186-019df753e44d",
                #    "templateType": "cisco_vpn",
                #    "subTemplates":
                #    [
                #        {
                #            "templateId": "81335119-ab5d-4bc6-af0c-0086117766d9",
                #            "templateType": "cisco_vpn_interface"
                #        }
                #    ]
                #},
                {
                    "templateId": "90497395-95ed-4002-ab68-a8b3d023a7cf",
                    "templateType": "cedge_global"
                },
                {
                    "templateId": "4484d3e3-ab77-42be-8d87-7b30d7070ce1",
                    "templateType": "cisco_banner"
                }
            ]
        }

        return payload

    @classmethod
    def template_with_subTemplate_payload(cls):
        payload = {
            "templateId": "6e5ba8e0-08d6-411a-affb-eccb41c5c81d",
            "templateType": "cisco_vpn",
            "subTemplates": []
        }

        return payload

    @classmethod
    def c8000v_default_feature_template(cls):
        ft_defatul_dict = {
            "cedge_aaa": 'Factory_Default_AAA_CISCO_Template',
            "cisco_bfd": 'Default_BFD_Cisco_V01',
            "cisco_omp": 'Default_AWS_TGW_CSR_OMP_IPv46_V01',
            "cisco_security": 'Default_Security_Cisco_V01',
            "cedge_global": 'Default_EQUINIX_C8000V_GLOBAL_CISCO_V01',
            "cisco_banner": 'Factory_Default_Retail_Banner',
            "cisco_logging": 'Default_Logging_Cisco_V01'
        }

        return ft_defatul_dict


