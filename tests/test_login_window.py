import unittest
from unittest.mock import patch

import login


class EntryStub:
    def __init__(self, value):
        self.value = value

    def get(self):
        return self.value


class LoginHarness:
    login_action = login.Login.login_action
    return_to_login = login.Login.return_to_login

    def __init__(self, events):
        self.events = events
        self.username_entry = EntryStub("workshop-user")
        self.password_entry = EntryStub("workshop-password")
        self.application = None

    def withdraw(self):
        self.events.append("hide-login")

    def deiconify(self):
        self.events.append("show-login")


class LoginWindowTests(unittest.TestCase):
    def test_login_waits_for_dashboard_window_before_hiding_login(self):
        events = []

        class FakeApplication:
            def __init__(self, master, user, on_logout):
                self.master = master
                self.user = user
                self.on_logout = on_logout
                events.append("create-dashboard")

            def wait_visibility(self):
                events.append("dashboard-visible")

            def iconbitmap(self, _path):
                events.append("set-icon")

            def destroy(self):
                events.append("destroy-dashboard")

        user = {"username": "workshop-user", "role": "Mechanic", "bootstrap_admin": False}
        harness = LoginHarness(events)
        with (
            patch("login.auth.authenticate", return_value=user),
            patch("login.KitboyApp", FakeApplication),
            patch("login.pywinstyles.apply_style", side_effect=lambda *_: events.append("style")),
        ):
            harness.login_action()

        self.assertEqual(
            events,
            ["create-dashboard", "style", "set-icon", "dashboard-visible", "hide-login"],
        )

    def test_invalid_credentials_show_error_owned_by_login_window(self):
        harness = LoginHarness([])
        with (
            patch("login.auth.authenticate", return_value=None),
            patch("login.messagebox.showerror") as show_error,
        ):
            harness.login_action()

        self.assertEqual(show_error.call_args.kwargs["parent"], harness)
        self.assertIsNone(harness.application)


if __name__ == "__main__":
    unittest.main()
