import pytest
import json


def test_etc_hosts(local_salt_client):
    nodes_info = local_salt_client.cmd(
        '*', 'cmd.run',
        ['cat /etc/hosts']
    )
    result = {}
    for node in nodes_info.keys():
        for nd in nodes_info.keys():
           if node not in nodes_info[nd]:
              if node in result:
                  result[node]+=','+nd
              else:
                  result[node]=nd
    assert len(result) <= 1, \
        "Some hosts are not presented in /etc/hosts: {0}".format(
         json.dumps(result, indent=4))     
