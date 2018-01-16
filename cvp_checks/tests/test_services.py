import pytest
import json
import os
from cvp_checks import utils


@pytest.mark.parametrize(
    "group",
    utils.node_groups.keys()
)
def test_check_services(local_salt_client, group):
    output = local_salt_client.cmd("L@"+','.join(utils.node_groups[group]), 'service.get_all', expr_form='compound')

    if len(output.keys()) < 2:
        pytest.skip("Nothing to compare - only 1 node")

    nodes = []
    pkts_data = []
    my_set = set()

    for node in output:
        nodes.append(node)
        my_set.update(output[node])

    for srv in my_set:
        diff = []
        row = []
        for node in nodes:
            if srv in output[node]:
                diff.append(srv)
                row.append("{}: +".format(node))
            else:
                row.append("{}: No service".format(node))
        if diff.count(diff[0]) < len(nodes):
            row.sort()
            row.insert(0, srv)
            pkts_data.append(row)
    assert len(pkts_data) <= 1, \
        "Several problems found for {0} group: {1}".format(
        group, json.dumps(pkts_data, indent=4))
