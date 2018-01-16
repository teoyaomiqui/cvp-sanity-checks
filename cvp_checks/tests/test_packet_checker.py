import pytest
import json
import os
from cvp_checks import utils


@pytest.mark.parametrize(
    "group",
    utils.node_groups.keys()
)
def test_check_package_versions(local_salt_client, group):
    output = local_salt_client.cmd("L@"+','.join(utils.node_groups[group]), 'lowpkg.list_pkgs', expr_form='compound')

    if len(output.keys()) < 2:
        pytest.skip("Nothing to compare - only 1 node")

    nodes = []
    pkts_data = []
    my_set = set()

    for node in output:
        nodes.append(node)
        my_set.update(output[node].keys())

    for deb in my_set:
        diff = []
        row = []
        for node in nodes:
            if deb in output[node].keys():
                diff.append(output[node][deb])
                row.append("{}: {}".format(node, output[node][deb]))
            else:
                row.append("{}: No package".format(node))
        if diff.count(diff[0]) < len(nodes):
            row.sort()
            row.insert(0, deb)
            pkts_data.append(row)
    assert len(pkts_data) <= 1, \
        "Several problems found for {0} group: {1}".format(
        group, json.dumps(pkts_data, indent=4))


@pytest.mark.parametrize(
    "group",
    utils.node_groups.keys()
)
def test_check_module_versions(local_salt_client, group):
    pre_check = local_salt_client.cmd(
        "L@"+','.join(utils.node_groups[group]), 'cmd.run', ['dpkg -l | grep "python-pip "'], expr_form='compound')
    if pre_check.values().count('') > 0:
        pytest.skip("pip is not installed on one or more nodes")
    if len(pre_check.keys()) < 2:
        pytest.skip("Nothing to compare - only 1 node")
    output = local_salt_client.cmd("L@"+','.join(utils.node_groups[group]), 'pip.freeze', expr_form='compound')

    nodes = []
    pkts_data = []
    my_set = set()

    for node in output:
        nodes.append(node)
        my_set.update([x.split("=")[0] for x in output[node]])
        output[node] = dict([x.split("==") for x in output[node]])

    for deb in my_set:
        diff = []
        row = []
        for node in nodes:
            if deb in output[node].keys():
                diff.append(output[node][deb])
                row.append("{}: {}".format(node, output[node][deb]))
            else:
                row.append("{}: No module".format(node))
        if diff.count(diff[0]) < len(nodes):
            row.sort()
            row.insert(0, deb)
            pkts_data.append(row)
    assert len(pkts_data) <= 1, \
        "Several problems found for {0} group: {1}".format(
        group, json.dumps(pkts_data, indent=4))
