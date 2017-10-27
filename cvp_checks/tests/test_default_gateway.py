import json
import pytest
import os
from cvp_checks import utils


@pytest.mark.parametrize(
    "group",
    utils.get_groups(os.path.basename(__file__))
)
def test_check_default_gateways(local_salt_client, group):
    if "skipped" in group:
        pytest.skip("skipped in config")
    netstat_info = local_salt_client.cmd(
        group, 'cmd.run', ['ip r | sed -n 1p'], expr_form='pcre')

    gateways = {}
    nodes = netstat_info.keys()

    for node in nodes:
        if netstat_info[node] not in gateways:
            gateways[netstat_info[node]] = [node]
        else:
            gateways[netstat_info[node]].append(node)

    assert len(gateways.keys()) == 1, \
        "There were found few gateways within group {group}: {gw}".format(
        group=group,
        gw=json.dumps(gateways, indent=4)
    )
