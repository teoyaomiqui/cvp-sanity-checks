import json
import requests


def test_elasticsearch_cluster(local_salt_client):
    salt_output = local_salt_client.cmd(
        'elasticsearch:client',
        'pillar.get',
        ['_param:haproxy_elasticsearch_bind_host'],
        expr_form='pillar')
    IP = salt_output[salt_output.keys()[0]]
    assert requests.get('http://{}:9200/'.format(IP)).status_code == 200, \
        'Cannot check elasticsearch url on {}.'.format(IP)


def test_stacklight_services_replicas(local_salt_client):
    salt_output = local_salt_client.cmd(
        'docker:client:stack:monitoring',
        'cmd.run',
        ['docker service ls'],
        expr_form='pillar')
    wrong_items = []
    for line in salt_output[salt_output.keys()[0]].split('\n'):
        if line[line.find('/') - 1] != line[line.find('/') + 1] \
           and 'replicated' in line:
            wrong_items.append(line)
    assert len(wrong_items) == 0, \
        '''Some monitoring services doesn't have expected number of replicas:
              {}'''.format(json.dumps(wrong_items, indent=4))


def test_stacklight_containers_status(local_salt_client):
    salt_output = local_salt_client.cmd(
        'docker:swarm:role:master',
        'cmd.run',
        ['docker service ps $(docker stack services -q monitoring)'],
        expr_form='pillar')
    result = {}
    for line in salt_output[salt_output.keys()[0]].split('\n')[1:]:
        shift = 0
        print line
        if line.split()[1] == '\\_':
            shift = 1
        if line.split()[1 + shift] not in result.keys():
            result[line.split()[1]] = 'NOT OK'
        if line.split()[4 + shift] == 'Running' \
           or line.split()[4 + shift] == 'Ready':
            result[line.split()[1 + shift]] = 'OK'
    assert 'NOT OK' not in result.values(), \
        '''Some containers are in incorrect state:
              {}'''.format(json.dumps(result, indent=4))
