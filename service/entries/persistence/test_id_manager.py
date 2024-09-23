import re

from hamcrest import assert_that, is_

from service.entries.persistence.id_manager import IdManager

pattern = r'^[{]?([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})[}]?$'


def test_is_uuid():
    assert_that(bool(re.match(pattern, IdManager().assign())), is_(True))
