from cdktf import Fn
from constructs import Construct

from imports.vcd.data_vcd_rde_type import DataVcdRdeType
from imports.vcd.rde import Rde


class SbpVcdRde(Rde):
    """SBP version of vcd.nsxt_ip_set"""

    def __init__(
            self,
            scope: Construct,
            ns: str,
            config_file_json: str,
            config_file_yaml: str,
            bearer: str,
            vendor: str = "vmware",
            nss: str = "capvcdCluster",
            resolve: bool = True,
            cap_vcd_cluster_version: str = "1.2.0",
            **kwargs,
    ):
        """Enhances the original vcd.nsxt_ip_set
            Ensures that only one ip set is created, and validates its use across the deployment

        Args:
            scope (Construct): Cdktf App
            id (str): uniq name of the resource

        Original:
            https://registry.terraform.io/providers/vmware/vcd/latest/docs/resources/nsxt_app_port_profile
        """

        rde_type = DataVcdRdeType(
            scope=scope,
            id_=f'{ns}_type',
            vendor=vendor,
            nss=nss,
            version=cap_vcd_cluster_version,
        )

        yaml_template = Fn.templatefile(config_file_yaml, {'bearer': bearer})
        json_template = Fn.templatefile(config_file_json, {'yaml': Fn.jsonencode(yaml_template)})

        super().__init__(
            scope=scope,
            id_=ns,
            resolve=resolve,
            rde_type_id=rde_type.id,
            input_entity=json_template,
            **kwargs,
        )
