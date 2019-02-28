from __future__ import (absolute_import, division, print_function)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


HAS_SPOTINST_SDK = False
__metaclass__ = type

import os
import time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import env_fallback

try:
    import spotinst_sdk2 as spotinst
    from spotinst_sdk2.client import SpotinstClientException

    HAS_SPOTINST_SDK = True

except ImportError:
    pass

# region Request Builder Funcitons
def expand_elasitgroup_request(module, is_update):
    do_not_update = module.params.get('do_not_update') or []

    name = module.params.get('name')
    description = module.params.get('description')

    capacity = module.params.get('capacity')
    strategy = module.params.get('strategy')
    scaling = module.params.get('scaling')
    third_parties_integration = module.params.get('third_parties_integration')
    compute = module.params.get('compute')

    elastigroup = spotinst.models.elastigroup.gcp.Elastigroup()

    if name is not None:
        if is_update:
            if 'name' not in do_not_update:
                elastigroup.name = name
        else:
            elastigroup.name = name

    if description is not None:
        if is_update:
            if 'description' not in do_not_update:
                elastigroup.description = description
        else:
            elastigroup.description = description

    # Capacity
    if capacity is not None:
        if is_update:
            if 'capacity' not in do_not_update:
                expand_capacity(elastigroup=elastigroup, capacity=capacity)
        else:
            expand_capacity(elastigroup=elastigroup, capacity=capacity)
    # Strategy
    if strategy is not None:
        if is_update:
            if 'strategy' not in do_not_update:
                expand_strategy(elastigroup=elastigroup, strategy=strategy)
        else:
            expand_strategy(elastigroup=elastigroup, strategy=strategy)
    # Scaling
    if scaling is not None:
        if is_update:
            if 'scaling' not in do_not_update:
                expand_scaling(elastigroup=elastigroup, scaling=scaling)
        else:
            expand_scaling(elastigroup=elastigroup, scaling=scaling)
    # Third Parties Integration
    if third_parties_integration is not None:
        if is_update:
            if 'third_parties_integration' not in do_not_update:
                expand_third_parties_integration(elastigroup=elastigroup, third_parties_integration=third_parties_integration)
        else:
            expand_third_parties_integration(elastigroup=elastigroup, third_parties_integration=third_parties_integration)
    # Compute
    if compute is not None:
        if is_update:
            if 'compute' not in do_not_update:
                expand_compute(elastigroup=elastigroup, compute=compute)
        else:
            expand_compute(elastigroup=elastigroup, compute=compute)

    return ocean

# region expand_capacity
def expand_capacity(elastigroup, capacity):
    eg_capacity = spotinst.models.elastigroup.gcp.Capacity()

    minimum = capacity.get('minimum')
    maximum = capacity.get('maximum')
    target = capacity.get('target')

    if minimum is not None:
        eg_capacity.minimum = minimum
    if maximum is not None:
        eg_capacity.maximum = maximum
    if target is not None:
        eg_capacity.target = target

    elastigroup.capacity = eg_capacity
# endregion

# region expand_strategy
def expand_strategy(elastigroup, strategy):
    eg_strategy = spotinst.models.elastigroup.gcp.Strategy()

    preemptible_percentage = strategy.get('preemptible_percentage')
    on_demand_count = strategy.get('on_demand_count')
    draining_timeout = strategy.get('draining_timeout')
    fallback_to_od = strategy.get('fallback_to_od')

    if preemptible_percentage is not None:
        eg_strategy.preemptible_percentage = preemptible_percentage
    if on_demand_count is not None:
        eg_strategy.on_demand_count = on_demand_count
    if draining_timeout is not None:
        eg_strategy.draining_timeout = draining_timeout
    if fallback_to_od is not None:
        eg_strategy.fallback_to_od = fallback_to_od

    elastigroup.strategy = eg_strategy
# endregion

# region expand_scaling
def expand_scaling(elastigroup, scaling):
    eg_scaling = spotinst.models.elastigroup.gcp.Scaling()

    up = scaling.get('up')
    down = scaling.get('down')

    if up is not None:
        temp_up = []
        for single_up in up:
            temp_up.append(expand_policy(policy=single_up))
        eg_scaling.up = temp_up
    if down is not None:
        temp_down = []
        for single_down in down:
            temp_down.append(expand_policy(policy=single_down))
        eg_scaling.down = temp_down


def expand_policy(policy):
    eg_scaling_policy = spotinst.models.elastigroup.gcp.ScalingPolicy()

    source = policy.get('source')
    policy_name = policy.get('policy_name')
    namespace = policy.get('namespace')
    metric_name = policy.get('metric_name')
    dimensions = policy.get('dimensions')
    statistic = policy.get('statistic')
    unit = policy.get('unit')
    threshold = policy.get('threshold')
    period = policy.get('period')
    evaluation_periods = policy.get('evaluation_periods')
    cooldown = policy.get('cooldown')
    action = policy.get('action')
    operator = policy.get('operator')

    if source is not None:
        eg_scaling_policy.source = source
    if policy_name is not None:
        eg_scaling_policy.policy_name = policy_name
    if namespace is not None:
        eg_scaling_policy.namespace = namespace
    if metric_name is not None:
        eg_scaling_policy.metric_name = metric_name
    if dimensions is not None:
       expand_dimensions(eg_scaling_policy=eg_scaling_policy, dimensions=dimensions)
    if statistic is not None:
        eg_scaling_policy.statistic = statistic
    if unit is not None:
        eg_scaling_policy.unit = unit
    if threshold is not None:
        eg_scaling_policy.threshold = threshold
    if period is not None:
        eg_scaling_policy.period = period
    if evaluation_periods is not None:
        eg_scaling_policy.evaluation_periods = evaluation_periods
    if cooldown is not None:
        eg_scaling_policy.cooldown = cooldown
    if action is not None:
        expand_action(eg_scaling_policy=eg_scaling_policy, action=action)
    if operator is not None:
        eg_scaling_policy.operator = operator

    return eg_scaling_policy


def expand_dimensions(eg_scaling_policy, dimensions):
    dim_list = []

    for single_dim in dimensions:
        temp_dim = spotinst.models.elastigroup.gcp.ScalingPolicyDimension()

        name = single_dim.get('name')
        value = single_dim.get('value')

        if name is not None:
            temp_dim.name = name
        if value is not None:
            temp_dim.value = value

        dim_list.append(temp_dim)

    eg_scaling_policy.dimensions = dim_list


def expand_action(eg_scaling_policy, action):
    eg_scaling_action = spotinst.models.elastigroup.gcp.ScalingPolicyAction()

    scaling_type = action.get('scaling_type')
    adjustment = action.get('adjustment')

    if scaling_type is not None:
        eg_scaling_action.scaling_type = scaling_type
    if adjustment is not None:
        eg_scaling_action.adjustment = adjustment

    eg_scaling_policy.action = eg_scaling_action
# endregion

# region expand_third_parties_integration
def expand_third_parties_integration(elastigroup, third_parties_integration):
    eg_integration = spotinst.models.elastigroup.gcp.ThirdPartiesIntegration()

    docker_swarm = third_parties_integration.get('docker_swarm')
    gke = third_parties_integration.get('gke')

    if docker_swarm is not None:
        expand_docker_swarm(eg_integration=eg_integration, docker_swarm=docker_swarm)
    if gke is not None:
        expand_gke(eg_integration=eg_integration, gke=gke)


def expand_docker_swarm(eg_integration=eg_integration, docker_swarm=docker_swarm):
    eg_docker_swarm_integration = spotinst.models.elastigroup.gcp.DockerSwarmConfiguration()

    master_host = docker_swarm.get('master_host')
    master_port = docker_swarm.get('master_port')

    if master_host is not None:
        eg_docker_swarm_integration.master_host = master_host
    if master_port is not None:
        eg_docker_swarm_integration.master_port = master_port

    eg_integration.docker_swarm = eg_docker_swarm_integration


def expand_gke(eg_integration=eg_integration, gke=gke):
    eg_gke_integration = spotinst.models.elastigroup.gcp.GKE()

    auto_update = gke.get('auto_update')
    auto_scale = gke.get('auto_scale')

    if auto_update is not None:
        eg_gke_integration.auto_update = auto_update
    if auto_scale is not None:
        expand_auto_scale(eg_gke_integration=eg_gke_integration, auto_scale=auto_scale)

    eg_integration.gke = eg_gke_integration


def expand_auto_scale(eg_gke_integration, auto_scale):
    eg_gke_auto_scale = spotinst.models.elastigroup.gcp.AutoScale()

    is_enabled = auto_scale.get('is_enabled')
    is_auto_config = auto_scale.get('is_auto_config')
    cooldown = auto_scale.get('cooldown')
    headroom = auto_scale.get('headroom')
    labels = auto_scale.get('labels')
    down = auto_scale.get('down')

    if is_enabled is not None:
        is_enabled = is_enabled
    if is_auto_config is not None:
        is_auto_config = is_auto_config
    if cooldown is not None:
        cooldown = cooldown
    if headroom is not None:
        expand_headroom(eg_gke_auto_scale=eg_gke_auto_scale, headroom=headroom)
    if labels is not None:
        expand_labels(service=eg_gke_auto_scale, labels=labels)
    if down is not None:
        expand_down(eg_gke_auto_scale=eg_gke_auto_scale, down=down)

    eg_gke_integration.auto_scale = eg_gke_auto_scale


def expand_headroom(eg_gke_auto_scale, headroom):
    eg_gke_headroom = spotinst.models.elastigroup.gcp.Headroom()

    cpu_per_unit = headroom.get('cpu_per_unit')
    memory_per_unit = headroom.get('memory_per_unit')
    num_of_units = headroom.get('num_of_units')

    if cpu_per_unit is not None:
        eg_gke_headroom.cpu_per_unit = cpu_per_unit
    if memory_per_unit is not None:
        eg_gke_headroom.memory_per_unit = memory_per_unit
    if num_of_units is not None:
        eg_gke_headroom.num_of_units = num_of_units

    eg_gke_auto_scale.headroom = eg_gke_headroom


def expand_labels(service, labels):
    label_list = []
    for single_label in labels:
        temp_label = spotinst.models.elastigroup.gcp.Label()

        key = single_label.get('key')
        value = single_label.get('value')

        if key is not None:
            temp_label.key = key
        if value is not None:
            temp_label.value = value

        label_list.append(temp_label)

    service.labels = label_list


def expand_down(eg_gke_auto_scale, down):
    eg_gke_down = spotinst.models.elastigroup.gcp.Down()
    evaluation_periods = down.get('evaluation_periods')

    if evaluation_periods is not None:
        eg_gke_down.evaluation_periods = evaluation_periods

    eg_gke_auto_scale.down = eg_gke_down
# endregion

# region expand_compute
def expand_compute(elastigroup, compute):
    eg_copmute = spotinst.models.elastigroup.gcp.Copmute()

    launch_specification = compue.get('launch_specification')
    instance_types = compue.get('instance_types')
    gpu = compue.get('gpu')
    health = compue.get('health')
    availability_zones = compue.get('availability_zones')
    subnets = compue.get('subnets')

    if launch_specification is not None:
        expand_launch_specification(eg_copmute=eg_copmute, launch_specification=launch_specification)
    if instance_types is not None:
        expand_instance_types(eg_copmute=eg_copmute, instance_types=instance_types)
    if gpu is not None:
        expand_gpu(eg_copmute=eg_copmute, gpu=gpu)
    if health is not None:
        expand_health(eg_copmute=eg_copmute, health=health)
    if availability_zones is not None:
        eg_copmute.availability_zones = availability_zones
    if subnets is not None:
        expand_subnets(eg_copmute=eg_copmute, subnets=subnets)


def expand_launch_specification(eg_copmute, launch_specification):
    eg_launch_spec = spotinst.models.elastigroup.gcp.LaunchSpecification()

    labels = launch_specification.get('labels')
    metadata = launch_specification.get('metadata')
    tags = launch_specification.get('tags')
    backend_service_config = launch_specification.get('backend_service_config')
    startup_script = launch_specification.get('startup_script')
    disks = launch_specification.get('disks')
    network_interfaces = launch_specification.get('network_interfaces')
    service_account = launch_specification.get('service_account')
    ip_forwarding = launch_specification.get('ip_forwarding')

    if labels is not None:
        expand_labels(service=eg_launch_spec, labels=labels)
    if metadata is not None:
        expand_metadata(eg_launch_spec=eg_launch_spec, metadata=metadata)
    if tags is not None:
        eg_launch_spec.tags = tags
    if backend_service_config is not None:
        expand_backend_service_config(eg_launch_spec=eg_launch_spec, backend_service_config=backend_service_config)
    if startup_script is not None:
        eg_launch_spec.startup_script = startup_script
    if disks is not None:
        expand_disks(eg_launch_spec=eg_launch_spec, disks=disks)
    if network_interfaces is not None:
        expand_network_interfaces(eg_launch_spec=eg_launch_spec, network_interfaces=network_interfaces)
    if service_account is not None:
        eg_launch_spec.service_account = service_account
    if ip_forwarding is not None:
        eg_launch_spec.ip_forwarding = ip_forwarding

    eg_copmute.launch_specification = eg_launch_spec


def expand_metadata(eg_launch_spec, metadata):
    metadata_list = []

    for single_meta in metadata:
        temp_metadata = spotinst.models.elastigroup.gcp.Metadata()

        key = metadata.get('key')
        value = metadata.get('value')

        if key is not None:
            temp_metadata.key = key
        if value is not None:
            temp_metadata.value = value

        metadata_list.append(temp_metadata)

    eg_launch_spec.metadata = metadata_list


def expand_backend_service_config(eg_launch_spec, backend_service_config):
    eg_backend_service = spotinst.models.elastigroup.gcp.BackendServiceConfig()
    backend_services = backend_service_config.get('backend_services')

    if backend_services is not None:
        service_list = []
        for single_service in backend_services:
            service_list.append(expand_backend_service(single_service=single_service))
        eg_backend_service.backend_services = service_list


def expand_backend_service(single_service):
    eg_single_service = spotinst.models.elastigroup.gcp.BackendServices()

    backend_service_name = single_service.get('backend_service_name')
    location_type = single_service.get('location_type')
    scheme = single_service.get('scheme')
    named_ports = single_service.get('named_ports')

    if backend_service_name is not None:
        eg_single_service.backend_service_name = backend_service_name
    if location_type is not None:
        eg_single_service.location_type = location_type
    if scheme is not None:
        eg_single_service.scheme = scheme
    if named_ports is not None:
        expand_named_ports(eg_single_service=eg_single_service, named_ports=named_ports)

    return eg_single_service


def expand_named_ports(eg_single_service, named_ports):
    eg_named_ports = spotinst.models.elastigroup.gcp.NamedPorts()

    name = name_ports.get('name')
    ports = named_ports.get('ports')

    if name is not None:
        eg_named_ports.name = name
    if ports is not None:
        eg_named_ports.ports = ports

    eg_single_service.named_ports = eg_named_ports


def expand_disks(eg_launch_spec, disks):
    list_disk = []

    for single_disk in disks:
        temp_disk = spotinst.models.elastigroup.gcp.Disk()

        auto_delete = single_disk.get('auto_delete')
        boot = single_disk.get('boot')
        device_name = single_disk.get('device_name')
        initialize_params = single_disk.get('initialize_params')
        interface = single_disk.get('interface')
        mode = single_disk.get('mode')
        source = single_disk.get('source')
        disk_type = single_disk.get('disk_type')

        if auto_delete is not None:
            temp_disk.auto_delete = auto_delete
        if boot is not None:
            temp_disk.boot = boot
        if device_name is not None: 
            temp_disk.device_name = device_name
        if initialize_params is not None:
            expand_initialize_params(disk=temp_disk, initialize_params=initialize_params)
        if interface is not None:
            temp_disk.interface = interface
        if mode is not None:
            temp_disk.mode = mode
        if source is not None:
            temp_disk.source = source
        if disk_type is not None:
            temp_disk.disk_type = disk_type

        list_disk.append(temp_disk)

    eg_launch_spec.disks = list_disk


def expand_initialize_params(disk, initialize_params):
    eg_initialize_params = spotinst.models.elastigroup.gcp.InitializeParams()

    disk_size_gb = initialize_params.get('disk_size_gb')
    disk_type = initialize_params.get('disk_type')
    source_image = initialize_params.get('source_image')

    if disk_size_gb is not None:
        eg_initialize_params.disk_size_gb = disk_size_gb
    if disk_type is not None:
        eg_initialize_params.disk_type = disk_type
    if source_image is not None:
        eg_initialize_params.source_image = source_image

    disk.initialize_params = eg_initialize_params


def expand_network_interfaces(eg_launch_spec, network_interfaces):
    eg_network_interface = spotinst.models.elastigroup.gcp.NetworkInterface()

    network = network_interfaces.get('network') 
    access_configs = network_interfaces.get('access_configs') #list[AccessConfig]
    alias_ip_ranges = network_interfaces.get('alias_ip_ranges') #list[AliasIpRange]

    if network is not None:
        eg_network_interface.network = network
    if access_configs is not None:
        expand_access_configs(eg_network_interface=eg_network_interface, access_configs=access_configs)
    if alias_ip_ranges is not None:
        expand_alias_ip_ranges(eg_network_interface=eg_network_interface, alias_ip_ranges=alias_ip_ranges)

    eg_launch_spec.network_interfaces = eg_network_interface


def expand_access_configs(eg_network_interface, access_configs):
    access_configs_list = []

    for single_config in access_configs:
        temp_config = spotinst.models.elastigroup.gcp.AccessConfig()
        name = access_configs.get('name')
        access_type = access_configs.get('access_type')

        if name is not None:
            temp_config.name = name
        if access_type is not None:
            temp_config.access_type = access_type

        access_configs_list.append(temp_config)

    eg_network_interface.access_configs = access_configs_list


def expand_alias_ip_ranges(eg_network_interface, alias_ip_ranges):
    alias_range_list = []

    for single_range in alias_ip_ranges:
        temp_range = spotinst.models.elastigroup.gcp.AliasIpRange()

        ip_cidr_range = alias_ip_ranges.get('ip_cidr_range')
        subnetwork_range_name = alias_ip_ranges.get('subnetwork_range_name')

        if ip_cidr_range is not None:
            temp_range.ip_cidr_range = ip_cidr_range
        if subnetwork_range_name is not None:
            temp_range.subnetwork_range_name = subnetwork_range_name

        alias_range_list.append(temp_range)

    eg_network_interface.alias_ip_ranges = alias_range_list


def expand_instance_types(eg_copmute, instance_types):
    eg_instance_types = spotinst.models.elastigroup.gcp.InstanceTypes()

    ondemand = instance_types.get('ondemand') 
    preemptible = instance_types.get('preemptible') 
    custom = instance_types.get('custom') 

    if ondemand is not None:
        eg_instance_types.ondemand = ondemand
    if preemptible is not None:
        eg_instance_types.preemptible = preemptible
    if custom is not None:
        expand_custom(eg_instance_types=eg_instance_types, custom=custom)

    eg_copmute.instance_types = eg_instance_types


def expand_custom(eg_instance_types, custom):
    custom_list = []
    for single_custom in custom:
        temp_custom = spotinst.models.elastigroup.gcp.CustomInstanceTypes()

        v_cpu = single_custom.get('v_cpu')
        memory_gib = single_custom.get('memory_gib')

        if v_cpu is not None:
            temp_custom.v_cpu = v_cpu
        if memory_gib is not None:
            temp_custom.memory_gib = memory_gib

        custom_list.append(temp_custom)

    eg_instance_types.custom = custom_list


def expand_gpu(eg_copmute, gpu):
    eg_gpu = spotinst.models.elastigroup.gcp.Gpu()

    gpu_type = gpu.get('gpu_type')
    count = gpu.get('')

    if gpu_type is not None:
        eg_gpu.gpu_type = gpu_type
    if count is not None:
        eg_gpu.count = count

    eg_copmute.gpu = eg_gpu


def expand_health(eg_copmute, health):
    eg_health = spotinst.models.elastigroup.gcp.Health()
    grace_period = health.get('grace_period')

    if grace_period is not None:
        eg_health.grace_period = grace_period

    eg_copmute.health = eg_health


def expand_subnets(eg_copmute, subnets):
    subnet_list = []
    for single_subnet in subnets:
        temp_subnet = spotinst.models.elastigroup.gcp.Subnet()

        region = single_subnet.get('region')
        subnet_names = single_subnet.get('subnet_names')

        if region is not None:
            temp_subnet.region = region
        if subnet_names is not None:
            temp_subnet.subnet_names = subnet_names

        subnet_list.append(temp_subnet)

    eg_copmute.subnets = subnet_list
# endregion
# endregion

# region Util Functions
def handle_elastigroup(client, module):
    request_type, eg_id = get_request_type_and_id(client=client, module=module)

    group_id = None
    message = None
    has_changed = False

    if request_type == "create":
        group_id, message, has_changed = handle_create(client=client, module=module)
    elif request_type == "update":
        group_id, message, has_changed = handle_update(client=client, module=module, group_id=eg_id)
    elif request_type == "delete":
        group_id, message, has_changed = handle_delete(client=client, module=module, group_id=eg_id)
    else:
        module.fail_json(msg="Action Not Allowed")

    return group_id, message, has_changed


def get_request_type_and_id(client, module):
    request_type = None
    group_id = "None"
    should_create = False

    name = module.params.get('name')
    state = module.params.get('state')
    uniqueness_by = module.params.get('uniqueness_by')
    external_group_id = module.params.get('id')

    if uniqueness_by == 'id':
        if external_group_id is None:
            should_create = True
        else:
            group_id = external_group_id
    else:
        groups = client.get_elastigroups()
        should_create, group_id = find_group_with_same_name(groups=groups, name=name)

    if should_create is True:
        if state == 'present':
            request_type = "create"

        elif state == 'absent':
            request_type = None

    else:
        if state == 'present':
            request_type = "update"

        elif state == 'absent':
            request_type = "delete"

    return request_type, group_id


def find_group_with_same_name(groups, name):
    for group in groups:
        if group['name'] == name:
            return False, group['id']

    return True, None


def get_client(module):
    # Retrieve creds file variables
    creds_file_loaded_vars = dict()

    credentials_path = module.params.get('credentials_path')

    if credentials_path is not None:
        try:
            with open(credentials_path, "r") as creds:
                for line in creds:
                    eq_index = line.find('=')
                    var_name = line[:eq_index].strip()
                    string_value = line[eq_index + 1:].strip()
                    creds_file_loaded_vars[var_name] = string_value
        except IOError:
            pass
    # End of creds file retrieval

    token = module.params.get('token')
    if not token:
        token = creds_file_loaded_vars.get("token")

    account = module.params.get('account_id')
    if not account:
        account = creds_file_loaded_vars.get("account")

    if account is not None:
        session = spotinst.SpotinstSession(auth_token=token, account_id=account)
    else:
        session = spotinst.SpotinstSession(auth_token=token)

    client = session.client("elastigroup_gcp")

    return client
# endregion


# region Request Functions
def handle_create(client, module):
    group_request = expand_elastigroup_request(module=module, is_update=False)
    group = client.create_elastigroup(group=group_request)

    group_id = group['id']
    message = 'Created Elastigroup Cluster successfully'
    has_changed = True

    return group_id, message, has_changed


def handle_update(client, module, group_id):
    group_request = expand_elastigroup_request(module=module, is_update=True)
    client.update_elastigroup(group_id=group_id, group=group_request)

    message = 'Updated Elastigroup Cluster successfully'
    has_changed = True

    return group_id, message, has_changed


def handle_delete(client, module, group_id):
    client.delete_elastigroup(group_id=group_id)

    message = 'Deleted Elastigroup Cluster successfully'
    has_changed = True

    return group_id, message, has_changed
# endregion


def main():
    fields = dict(
        account_id=dict(type='str', fallback=(env_fallback, ['SPOTINST_ACCOUNT_ID', 'ACCOUNT'])),
        token=dict(type='str', fallback=(env_fallback, ['SPOTINST_TOKEN'])),
        state=dict(type='str', default='present', choices=['present', 'absent']),
        id=dict(type='str'),
        uniqueness_by=dict(type='str', default='name', choices=['name', 'id']),
        credentials_path=dict(type='path', default="~/.spotinst/credentials"),

        name=dict(type='str'),
        description=dict(type='str'),
        capacity=dict(type='dict'),
        strategy=dict(type='dict'),
        scaling=dict(type='dict'),
        third_parties_integration=dict(type='dict'),
        compute=dict(type='dict'))

    module = AnsibleModule(argument_spec=fields)

    if not HAS_SPOTINST_SDK:
        module.fail_json(msg="the Spotinst SDK library is required. (pip install spotinst_sdk)")

    client = get_client(module=module)

    group_id, message, has_changed = handle_elastigroup(client=client, module=module)

    module.exit_json(changed=has_changed, group_id=group_id, message=message, instances=[])


if __name__ == '__main__':
    main()