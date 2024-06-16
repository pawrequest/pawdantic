import pytest

from tests.models import TestModel, TestModelOptionalJson, TestModelRequiredJson


@pytest.mark.parametrize(
    "model_fixture, model_class",
    [
        ("test_model", TestModel),
        ("test_model_required_json", TestModelRequiredJson),
        ("test_model_optional_json_provided", TestModelOptionalJson),
        ("test_model_optional_json_not_provided", TestModelOptionalJson),
    ]
)
def test_insert_and_retrieve_model(model_fixture, model_class, request, test_session):
    test_model_param = request.getfixturevalue(model_fixture)
    test_session.add(test_model_param)
    test_session.commit()
    result = test_session.query(model_class).first()
    if model_fixture == "test_model_optional_json_not_provided":
        assert result.alerts_list is None
        assert result.alerts_dict is None
        assert result.alerts_tuple is None
        assert result.alert is None

    else:
        assert result.alert == test_model_param.alert
        assert result.alerts_list == test_model_param.alerts_list
        assert result.alerts_dict == test_model_param.alerts_dict
        assert result.alerts_tuple == test_model_param.alerts_tuple
