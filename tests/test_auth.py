import unittest

from auth import ROLE_PAGES, ROLES, hash_password, normalize_role, verify_password


class PasswordTests(unittest.TestCase):
    def test_hash_verifies_without_matching_the_plaintext(self):
        stored = hash_password("workshop-pass")

        self.assertNotEqual(stored, "workshop-pass")
        self.assertEqual(verify_password("workshop-pass", stored), (True, False))
        self.assertEqual(verify_password("incorrect", stored), (False, False))

    def test_legacy_password_is_marked_for_upgrade_after_verification(self):
        self.assertEqual(verify_password("legacy", "legacy"), (True, True))
        self.assertEqual(verify_password("incorrect", "legacy"), (False, True))

    def test_workshop_roles_have_separate_page_access(self):
        self.assertEqual(set(ROLES), set(ROLE_PAGES))
        self.assertIn("users", ROLE_PAGES["Admin"])
        self.assertNotIn("payments", ROLE_PAGES["Mechanic"])
        self.assertIn("diagnostics", ROLE_PAGES["Mechanic"])

    def test_existing_role_values_are_normalized(self):
        self.assertEqual(normalize_role("admin"), "Admin")
        self.assertEqual(normalize_role("service advisor"), "Service Advisor")
        self.assertIsNone(normalize_role("unknown"))


if __name__ == "__main__":
    unittest.main()
