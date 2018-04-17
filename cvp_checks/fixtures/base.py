import pytest
import cvp_checks.utils as utils


@pytest.fixture(scope='session')
def local_salt_client():
    return utils.init_salt_client()


nodes = utils.calculate_groups()


@pytest.fixture(scope='session', params=nodes.values(), ids=nodes.keys())
def nodes_in_group(request):
    return request.param
