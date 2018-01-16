import pytest
from cvp_checks import utils


@pytest.mark.parametrize(
    "group",
    utils.node_groups.keys()
)
def test_list_of_repo_on_nodes(local_salt_client, group):
    info_salt = local_salt_client.cmd('L@' + ','.join(
                                      utils.node_groups[group]),
                                      'pillar.data', ['linux:system:repo'],
                                      expr_form='compound')
    raw_actual_info = local_salt_client.cmd(
        group,
        'cmd.run',
        ['cat /etc/apt/sources.list.d/*;'
         'cat /etc/apt/sources.list|grep deb|grep -v "#"'],
        expr_form='pcre')
    actual_repo_list = [item.replace('/ ', ' ').replace('[arch=amd64] ', '')
                        for item in raw_actual_info.values()[0].split('\n')]
    expected_salt_data = [repo['source'].replace('/ ', ' ')
                                        .replace('[arch=amd64] ', '')
                          for repo in info_salt.values()[0]
                          ['linux:system:repo'].values()
                          if 'source' in repo.keys()]

    diff = {}
    my_set = set()
    fail_counter = 0
    my_set.update(actual_repo_list)
    my_set.update(expected_salt_data)
    import json
    for repo in my_set:
        rows = []
        if repo not in actual_repo_list:
            rows.append("{}: {}".format("pillars", "+"))
            rows.append("{}: No repo".format('config'))
            diff[repo] = rows
            fail_counter += 1
        elif repo not in expected_salt_data:
            rows.append("{}: {}".format("config", "+"))
            rows.append("{}: No repo".format('pillars'))
            diff[repo] = rows
    assert fail_counter == 0, \
        "Several problems found for {0} group: {1}".format(
            group, json.dumps(diff, indent=4))
    if fail_counter == 0 and len(diff) > 0:
        print "\nWarning: nodes contain more repos than reclass"
