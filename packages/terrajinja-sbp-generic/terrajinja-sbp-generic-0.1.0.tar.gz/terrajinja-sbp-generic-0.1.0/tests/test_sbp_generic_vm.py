import pytest

from src.terrajinja.sbp.generic.vm import SbpGenericVmPlacementPolicy, SbpGenericVm, InvalidVmPlacementPolicy
from .helper import stack


class TestSbpGenericVmPlacementPolicy:
    def test_vm_policy_one_per_zone_loop(self, stack):
        policy = SbpGenericVmPlacementPolicy(
            strategy="one_per_zone",
            placements=[
                {'zone': 1, 'name': 'zone1'},
                {'zone': 2, 'name': 'zone2'},
                {'zone': 3, 'name': 'zone3'}
            ]
        )

        # policy should be a never ending loop in order
        for zone in [1, 2, 3, 1, 2, 3, 1, 2, 3]:
            next(policy)
            assert policy.zone == zone
            assert policy.name == f'zone{zone}'

    def test_vm(self, stack):
        policy = SbpGenericVmPlacementPolicy(
            strategy="one_per_zone",
            placements=[
                {'zone': 1, 'name': 'zone1'},
                {'zone': 2, 'name': 'zone2'},
                {'zone': 3, 'name': 'zone3'}
            ]
        )

        count = 10
        vms = SbpGenericVm(
            placement_policy=policy,
            name="dummy",
            ip_addresses=[f"127.0.0.{digit}" for digit in range(count)],
            count=count
        )

        expected = [
            {'name': 'dummy100', 'zone_id': 1, 'zone_name': 'zone1', 'ip': '127.0.0.0'},
            {'name': 'dummy200', 'zone_id': 2, 'zone_name': 'zone2', 'ip': '127.0.0.1'},
            {'name': 'dummy300', 'zone_id': 3, 'zone_name': 'zone3', 'ip': '127.0.0.2'},
            {'name': 'dummy101', 'zone_id': 1, 'zone_name': 'zone1', 'ip': '127.0.0.3'},
            {'name': 'dummy201', 'zone_id': 2, 'zone_name': 'zone2', 'ip': '127.0.0.4'},
            {'name': 'dummy301', 'zone_id': 3, 'zone_name': 'zone3', 'ip': '127.0.0.5'},
            {'name': 'dummy102', 'zone_id': 1, 'zone_name': 'zone1', 'ip': '127.0.0.6'},
            {'name': 'dummy202', 'zone_id': 2, 'zone_name': 'zone2', 'ip': '127.0.0.7'},
            {'name': 'dummy302', 'zone_id': 3, 'zone_name': 'zone3', 'ip': '127.0.0.8'},
            {'name': 'dummy103', 'zone_id': 1, 'zone_name': 'zone1', 'ip': '127.0.0.9'}
        ]
        vm = [vm for vm in vms]

        # check with expectations
        for nr, expectation in enumerate(expected):
            assert vm[nr].name == expectation['name']
            assert vm[nr].zone_id == expectation['zone_id']
            assert vm[nr].zone_name == expectation['zone_name']
            assert vm[nr].ip == expectation['ip']

    def test_vm_alternate_naming(self, stack):
        policy = SbpGenericVmPlacementPolicy(
            strategy="one_per_zone",
            placements=[
                {'zone': 1, 'name': 'zone1'},
                {'zone': 2, 'name': 'zone2'},
            ]
        )

        count = 10
        vms = SbpGenericVm(
            placement_policy=policy,
            name="dummy",
            ip_addresses=[f"127.0.0.{digit}" for digit in range(count)],
            formatting=["%s-%s-%03d", "name", "zone_name", "nr"],
            first_digit=1,
            count=count
        )

        expected = [
            {'name': 'dummy-zone1-001', 'zone_id': 1, 'zone_name': 'zone1', 'ip': '127.0.0.0'},
            {'name': 'dummy-zone2-002', 'zone_id': 2, 'zone_name': 'zone2', 'ip': '127.0.0.1'},
            {'name': 'dummy-zone1-003', 'zone_id': 1, 'zone_name': 'zone1', 'ip': '127.0.0.2'},
            {'name': 'dummy-zone2-004', 'zone_id': 2, 'zone_name': 'zone2', 'ip': '127.0.0.3'},
            {'name': 'dummy-zone1-005', 'zone_id': 1, 'zone_name': 'zone1', 'ip': '127.0.0.4'},
            {'name': 'dummy-zone2-006', 'zone_id': 2, 'zone_name': 'zone2', 'ip': '127.0.0.5'},
            {'name': 'dummy-zone1-007', 'zone_id': 1, 'zone_name': 'zone1', 'ip': '127.0.0.6'},
            {'name': 'dummy-zone2-008', 'zone_id': 2, 'zone_name': 'zone2', 'ip': '127.0.0.7'},
            {'name': 'dummy-zone1-009', 'zone_id': 1, 'zone_name': 'zone1', 'ip': '127.0.0.8'},
            {'name': 'dummy-zone2-010', 'zone_id': 2, 'zone_name': 'zone2', 'ip': '127.0.0.9'}
        ]
        vm = [vm for vm in vms]

        # check with expectations
        for nr, expectation in enumerate(expected):
            assert vm[nr].name == expectation['name']
            assert vm[nr].zone_id == expectation['zone_id']
            assert vm[nr].zone_name == expectation['zone_name']
            assert vm[nr].ip == expectation['ip']

    def test_placement_policy_invalid_strategy(self, stack):
        with pytest.raises(InvalidVmPlacementPolicy) as context:
            policy = SbpGenericVmPlacementPolicy(
                strategy="invalid",
                placements=[
                    {'zone': 1, 'name': 'zone1'},
                    {'zone': 2, 'name': 'zone2'},
                    {'zone': 3, 'name': 'zone3'}
                ]
            )

        assert f"unknown vm placement strategy" in str(context.value)


if __name__ == "__main__":
    pytest.main()
