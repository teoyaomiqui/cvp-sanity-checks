def test_uncommited_changes(local_salt_client):
    git_status = local_salt_client.cmd(
        'salt:master',
        'cmd.run',
        ['cd /srv/salt/reclass/classes/cluster/; git status'],
        expr_form='pillar')
    assert 'nothing to commit' in git_status.values()[0], 'Git status showed' \
           ' some unmerged changes {}'''.format(git_status.values()[0])
