#complete your tasks in this file
import sys
import math
from typing import *
from dataclasses import dataclass

sys.setrecursionlimit(10**6)

@dataclass(frozen=True)
class GlobeRect:
    lo_lat: float
    hi_lat: float
    west_long: float
    east_long: float


@dataclass(frozen=True)
class Region:
    rect: GlobeRect
    name: str
    terrain: str


@dataclass(frozen=True)
class RegionCondition:
    region: Region
    year: int
    pop: int
    ghg_rate: float

tokyo_rect = GlobeRect(35.0, 36.0, 139.0, 140.0)
tokyo = Region(tokyo_rect, "Tokyo", "other")

paris_rect = GlobeRect(48.5, 49.0, 2.0, 3.0)
paris = Region(paris_rect, "Paris", "other")

pacific_rect = GlobeRect(10.0, 20.0, -150.0, -140.0)
pacific = Region(pacific_rect, "Pacific Slice", "ocean")

slo_rect = GlobeRect(35.1, 35.4, -120.8, -120.4)
slo = Region(slo_rect, "San Luis Obispo Region", "forest")

region_conditions: List[RegionCondition] = [
    RegionCondition(tokyo, 2020, 37000000, 100000000.0),
    RegionCondition(paris, 2020, 11000000, 25000000.0),
    RegionCondition(pacific, 2020, 0, 0.0),
    RegionCondition(slo, 2020, 300000, 1000000.0)
]

def emissions_per_capita(rc: RegionCondition) -> float:
    if rc.pop == 0:
        return 0.0
    return rc.ghg_rate / rc.pop

def area(gr: GlobeRect) -> float:

    R = 6378.1

    phi1 = math.radians(gr.lo_lat)
    phi2 = math.radians(gr.hi_lat)

    lam1 = math.radians(gr.west_long)
    lam2 = math.radians(gr.east_long)

    diff = lam2 - lam1

    if diff < 0:
        diff += 2 * math.pi

    return (R ** 2) * abs(diff) * abs(math.sin(phi2) - math.sin(phi1))

def emissions_per_square_km(rc: RegionCondition) -> float:

    a = area(rc.region.rect)

    if a == 0:
        return 0.0

    return rc.ghg_rate / a

def density(rc: RegionCondition) -> float:

    a = area(rc.region.rect)

    if a == 0:
        return 0.0

    return rc.pop / a

def densest_helper(rc_list: List[RegionCondition]) -> RegionCondition:
    if len(rc_list) == 1:
        return rc_list[0]

    best_rest = densest_helper(rc_list[1:])

    if density(rc_list[0]) > density(best_rest):
        return rc_list[0]
    else:
        return best_rest


def densest(rc_list: List[RegionCondition]) -> str:
    return densest_helper(rc_list).region.name

def growth_rate(terrain: str) -> float:

    if terrain == "ocean":
        return 0.0001

    if terrain == "mountains":
        return 0.0005

    if terrain == "forest":
        return -0.00001

    return 0.0003

def grow_population(pop: float, rate: float, years: int) -> float:

    if years <= 0:
        return pop

    return grow_population(pop * (1 + rate), rate, years - 1)


def project_condition(rc: RegionCondition, years: int) -> RegionCondition:

    rate = growth_rate(rc.region.terrain)

    new_pop = int(grow_population(rc.pop, rate, years))

    if rc.pop == 0:
        new_ghg = 0.0
    else:
        new_ghg = rc.ghg_rate * (new_pop / rc.pop)

    return RegionCondition(
        rc.region,
        rc.year + years,
        new_pop,
        new_ghg
    )