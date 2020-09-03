from unittest import TestCase
from requests import Session
from ordway.session import TimeoutAdapter, timeout_retry_adapter, session_factory

class SessionFactoryTestCase(TestCase):
    def test_attaches_retry_adapter_for_existing_session(self):
        existing_session = Session()
        session_factory(existing_session)

        self.assertEqual(existing_session.adapters["http://"], timeout_retry_adapter)
        self.assertEqual(existing_session.adapters["https://"], timeout_retry_adapter)

    def test_attaches_retry_adapter_for_new_session(self):
        new_session = session_factory()
        self.assertEqual(new_session.adapters["http://"], timeout_retry_adapter)
        self.assertEqual(new_session.adapters["https://"], timeout_retry_adapter)

class TimeoutAdapterTestCase(TestCase):
    def test_sets_timeout(self):
        adapter = TimeoutAdapter()
        self.assertEqual(adapter.timeout, adapter.DEFAULT_TIMEOUT)

        adapter = TimeoutAdapter(timeout=5)
        self.assertEqual(adapter.timeout, 5)

    def test_get_state_includes_timeout(self):
        state = TimeoutAdapter(timeout=15).__getstate__()

        self.assertIn("timeout", state)
        self.assertEqual(state["timeout"], 15)