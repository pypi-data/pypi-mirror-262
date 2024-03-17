from dataclasses import dataclass, field


class InvalidVmPlacementPolicy(Exception):
    """The placement polict does not exist"""


@dataclass
class SbpGenericVmPlacement:
    """Placement zone and name for a VM"""
    zone: int
    name: str


class SbpGenericVmPlacementPolicy:

    def __init__(self, strategy: str, placements: list[dict]):
        self.placements = [SbpGenericVmPlacement(**placement) for placement in placements]
        strategies = {
            'one_per_zone': self.one_per_zone
        }
        self.strategy = strategies.get(strategy)
        if not self.strategy:
            raise InvalidVmPlacementPolicy(
                f"unknown vm placement strategy '{strategy}' should be one of {list(strategies.keys())}")
        self.id_ = 0
        """Generates an infinite loop iterator for placement policies

        Args:
            strategy (str): name of the strategy to apply
            placements (str): list of available placements
        """

    def one_per_zone(self):
        """Rotates placement by selecting the new placement every new request"""
        placement = self.placements[self.id_]
        self.id_ += 1
        if self.id_ >= len(self.placements):
            self.id_ = 0
        return placement

    def __iter__(self):
        self.id_ = 0
        return self

    def __next__(self):
        return self.strategy()

    @property
    def zone(self):
        """return the zone of the current placement"""
        return self.placements[self.id_ - 1].zone

    @property
    def name(self):
        """return the name of the current placement"""
        return self.placements[self.id_ - 1].name

    @property
    def count(self):
        """returns the number of placements"""
        return len(self.placements)


@dataclass
class SbpGenericVmInstance:
    name: str
    zone_id: int
    zone_name: str
    ip: str


@dataclass
class SbpGenericVm:
    placement_policy: SbpGenericVmPlacementPolicy
    name: str
    count: int
    ip_addresses: list[str]
    first_digit: int = 0
    nr_: int = 0
    formatting: list[str] = field(default_factory=lambda: ["%s%d%02d", "name", "zone_id", "nr_per_zone"])

    def __iter__(self):
        return self

    def __next__(self):
        if self.nr_ >= self.count:
            raise StopIteration

        ipaddress = self.ip_addresses[self.nr_]
        self.nr_ += 1
        next(self.placement_policy)
        return SbpGenericVmInstance(name=self.name_generator, zone_id=self.zone_id, zone_name=self.zone_name,
                                    ip=ipaddress)

    @property
    def name_generator(self):
        format_string = self.formatting[0]
        format_input = (getattr(self, obj) for obj in self.formatting[1:])
        return format_string % tuple(format_input)

    @property
    def zone_id(self):
        return self.placement_policy.zone

    @property
    def zone_name(self):
        return self.placement_policy.name

    @property
    def nr(self):
        return self.nr_ - 1 + self.first_digit

    @property
    def nr_per_zone(self):
        return (self.nr_ - 1) / self.placement_policy.count + self.first_digit
