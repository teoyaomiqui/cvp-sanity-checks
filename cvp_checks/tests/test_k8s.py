import pytest
import json

def test_k8s_get_cs_status(local_salt_client):
    result = local_salt_client.cmd(
        'etcd:server', 'cmd.run',
        ['kubectl get cs'],
        expr_form='pillar'
    )
    errors = []
    if not result:
        pytest.skip("k8s is not found on this environment")
    for node in result:
        for line in result[node].split('\n'):
            line = line.strip()
            if 'MESSAGE' in line:
                continue
            else:
                if 'Healthy' not in line:
                    errors.append (line)
        break
    assert not errors, 'k8s is not healthy: {}'.format(json.dumps(
                                                             errors,
                                                             indent=4))


def test_k8s_get_nodes_status(local_salt_client):
    result = local_salt_client.cmd(
        'etcd:server', 'cmd.run',
        ['kubectl get nodes'],
        expr_form='pillar'
    )
    errors = []
    if not result:
        pytest.skip("k8s is not found on this environment")
    for node in result:
        for line in result[node].split('\n'):
            line = line.strip()
            if 'STATUS' in line:
                continue
            else:
                if 'Ready' not in line:
                    errors.append (line)
        break
    assert not errors, 'k8s is not healthy: {}'.format(json.dumps(
                                                             errors,
                                                             indent=4))
