from constructs import Construct

from imports.vcd.data_vcd_vm_placement_policy import DataVcdVmPlacementPolicy
from .decorators import run_once


@run_once(parameter_match=["name", "urn"])
class SbpDataVcdVmPlacementPolicy(DataVcdVmPlacementPolicy):
    """Extends the original vcd.data_vcd_vm_placement_policy class
       to ensure that it only gets called once"""

    def __init__(self, scope: Construct, id_: str, name: str, urn: str):
        """Enhances the original vcd.data_vcd_vm_placement_policy
           to ensure that it only gets called once

        Args:
            scope (Construct): Cdktf App
            id_ (str): uniq name of the resource
            name (str): name of the placement policy
            urn (str): the urn of the provider vcd id

        Original:
            https://registry.terraform.io/providers/vmware/vcd/3.10.0/docs/data-sources/catalog_vapp_template
        """
        super().__init__(
            scope=scope,
            id_=f'sbp_vcd_catalog_vapp_template_{name}',
            name=name,
            provider_vdc_id=urn
        )
