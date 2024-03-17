# terrajinja-sbp-generic

python helper functions for other terrajinja resources

### human_read_to_megabyte
converts human readable numbers (e.g. "10TB") to a size in MB (int)
    
    def human_read_to_megabyte(size: str) -> int:
        Convert human formatted size to megabytes value.

        Args:
            size: string of human formatted size

        Returns:
            megabytes represented in the initial human format

### placement policies
various commands to control the placement policy of a vm

        # create a placement polict based on placements and strategy
        placement_policy = SbpGenericVmPlacementPolicy(strategy=placement_strategy, placements=placements)
        # create a vm iteration that combines placement policy and naming policy
        vms = SbpGenericVm(placement_policy=placement_policy, name=name, count=count, first_digit=first_digit,
                           formatting=naming_format, ip_addresses=ip_addresses)

        # list all vm's in policy
        for vm in vms:
            print(f'- host: {vm.name} in zone: {vm.zone_name} ip: {vm.ip}')

            # return the placement policy id for the creation of the vm in the correct place
            placement_policy_id = SbpDataVcdVmPlacementPolicy(scope=scope, id_='', name=vms.placement_policy.name,
                                                              urn=vdc_urn).id
