import copy

from hypothesis import given
from hypothesis import strategies as st
from mock import Mock, call, patch
import pytest

from hammurabi import Law
from tests.helpers import FAILING_RULE, PASSING_RULE, TestRule


@given(name=st.text(), description=st.text())
def test_documentation(name, description):
    law = Law(name="Empty", description="empty law", rules=())
    law.name = name
    law.description = description
    expected_documentation = f"{name}\n{description}"

    assert law.documentation == expected_documentation


def test_executes_no_task():
    law = Law(name="Empty", description="empty law", rules=())
    law.commit = Mock()

    law.enforce()

    assert len(law.rules) == 0
    assert law.commit.called is False


def test_executes_task():
    rule = copy.deepcopy(PASSING_RULE)
    rule.execute = Mock()

    law = Law(name="Passing", description="passing law", rules=(rule,))
    law.commit = Mock()

    law.enforce()

    rule.execute.assert_called_once_with()
    law.commit.assert_called_once_with()


@patch("hammurabi.law.logging")
@patch("hammurabi.law.config")
def test_rule_execution_failed_no_abort(mocked_config, mocked_logging):
    mocked_config.rule_can_abort = False
    mocked_logging.error = Mock()
    mocked_logging.warning = Mock()
    expected_exception = "failed"

    rule = copy.deepcopy(FAILING_RULE)
    rule.param = expected_exception
    rule.get_rule_chain = Mock(return_value=[copy.deepcopy(PASSING_RULE)])

    law = Law(name="Passing", description="passing law", rules=(rule,))
    law.commit = Mock()

    law.enforce()

    assert mocked_logging.error.called
    rule.get_rule_chain.assert_called_once_with(rule)
    assert mocked_logging.warning.called
    law.commit.assert_called_once_with()


@patch("hammurabi.law.logging")
@patch("hammurabi.law.config")
def test_rule_execution_aborted(mocked_config, mocked_logging):
    mocked_config.rule_can_abort = True
    mocked_logging.error = Mock()
    mocked_logging.warning = Mock()
    expected_exception = "failed"

    rule = copy.deepcopy(FAILING_RULE)
    rule.param = expected_exception
    rule.get_rule_chain = Mock(return_value=[copy.deepcopy(PASSING_RULE)])

    law = Law(name="Passing", description="passing law", rules=(rule,))
    law.commit = Mock()

    with pytest.raises(Exception) as exc:
        law.enforce()

    assert mocked_logging.error.called
    assert str(exc.value) == expected_exception
    rule.get_rule_chain.assert_called_once_with(rule)
    assert mocked_logging.warning.called
    assert law.commit.called is False


def test_execution_order():
    rule_1 = TestRule(name="rule_1", param="rule_1")
    rule_2 = TestRule(name="rule_2", param="rule_2")
    rule_3 = TestRule(name="rule_3", param="rule_3")

    rule_1.get_execution_order = Mock(return_value=[])
    rule_2.get_execution_order = Mock(return_value=[])
    rule_3.get_execution_order = Mock(return_value=[])

    law = Law(name="Passing", description="passing law", rules=(rule_1, rule_2, rule_3))
    law.get_execution_order()

    rule_1.get_execution_order.assert_called_once_with()
    rule_2.get_execution_order.assert_called_once_with()
    rule_3.get_execution_order.assert_called_once_with()


def test_commit_changes():
    rule = copy.deepcopy(PASSING_RULE)
    rule.execute = Mock()
    rule.made_changes = True

    law = Law(name="Passing", description="passing law", rules=(rule,))
    law.git_commit = Mock()
    law.get_execution_order = Mock(return_value=[rule])

    expected_commit_message = f"{law.documentation}\n\n* {rule.name}"

    law.enforce()

    rule.execute.assert_called_once_with()
    law.get_execution_order.assert_called_once_with()
    law.git_commit.assert_called_once_with(expected_commit_message)


def test_commit_no_changes():
    rule = copy.deepcopy(PASSING_RULE)
    rule.execute = Mock()
    rule.made_changes = False

    law = Law(name="Passing", description="passing law", rules=(rule,))
    law.git_commit = Mock()
    law.get_execution_order = Mock(return_value=[rule])

    law.enforce()

    rule.execute.assert_called_once_with()
    law.get_execution_order.assert_called_once_with()
    assert law.git_commit.called is False
