import os

try:
    from pint import UnitRegistry
    from bliss import setup_globals
except ImportError:
    ureg = None
    setup_globals = None
else:
    ureg = UnitRegistry()

from ..exafs.plotter import ExafsPlotter
from ..resources.exafs import RESOURCE_ROOT


class DemoExafsPlotter(ExafsPlotter):
    def __init__(self, **defaults) -> None:
        defaults.setdefault("workflow", os.path.join(RESOURCE_ROOT, "exafs.ows"))
        defaults.setdefault("_scan_type", "any")
        counters = defaults.setdefault("_counters", dict())
        energy_unit = setup_globals.energy.unit or "eV"
        counters.setdefault(
            "any",
            {
                "mu_name": "mu",
                "energy_name": "energy",
                "energy_unit": energy_unit,
            },
        )
        super().__init__(**defaults)

    def _scan_type_from_scan(self, scan) -> str:
        return "any"

    def run(self, expo=0.003):
        e0 = 8800
        e1 = 9600
        step_size = 0.5
        intervals = int((e1 - e0) / step_size) - 1

        from_unit = "eV"
        to_unit = self.counters["energy_unit"]

        if ureg:
            e0 = (e0 * ureg(from_unit)).to(to_unit).magnitude
            e1 = (e1 * ureg(from_unit)).to(to_unit).magnitude
        else:
            assert from_unit == to_unit, "counters energy unit is wrong"

        scan = setup_globals.ascan(
            setup_globals.energy, e0, e1, intervals, expo, setup_globals.mu, run=False
        )
        super().run(scan)


if setup_globals is None:
    exafs_plotter = None
else:
    exafs_plotter = DemoExafsPlotter()
    exafs_plotter.refresh_period = 0.5
