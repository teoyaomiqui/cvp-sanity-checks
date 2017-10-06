from cvp_checks import utils


def test_ntp_sync(local_salt_client):
    config = utils.get_configuration(__file__)
    fail = {}
    saltmaster_time = int(local_salt_client.cmd(
        'salt:master',
        'cmd.run',
        ['date +%s'],
        expr_form='pillar').values()[0])

    nodes_time = local_salt_client.cmd(
        '*', 'cmd.run', ['date +%s'])

    for node, time in nodes_time.iteritems():
        if (int(time) - saltmaster_time) > config["time_deviation"] or \
                (int(time) - saltmaster_time) < -config["time_deviation"]:
            fail[node] = time

    assert not fail, 'SaltMaster time: {}\n' \
                     'Nodes with time mismatch:\n {}'.format(saltmaster_time,
                                                             fail)
