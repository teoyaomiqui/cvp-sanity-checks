import json
import pytest
import os
from cvp_checks import utils


@pytest.mark.parametrize(
    "group",
    utils.node_groups.keys()
)
def test_check_default_gateways(local_salt_client, group):
    netstat_info = local_salt_client.cmd(
        "L@"+','.join(utils.node_groups[group]), 'cmd.run', ['ip r | sed -n 1p'], expr_form='compound')

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
