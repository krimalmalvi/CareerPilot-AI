import tempfile
import unittest
from pathlib import Path

import app as career_app


class CareerPilotSmokeTests(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.original_db_path = career_app.DB_PATH
        self.original_upload_dir = career_app.UPLOAD_DIR

        career_app.DB_PATH = Path(self.tempdir.name) / "test.db"
        career_app.UPLOAD_DIR = Path(self.tempdir.name) / "uploads"
        career_app.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

        career_app.init_db()

        career_app.app.config.update(
            TESTING=True,
            SECRET_KEY="test-secret",
            WTF_CSRF_ENABLED=False,
        )

        self.client = career_app.app.test_client()

    def tearDown(self):
        if hasattr(self, "client"):
            self.client = None

        career_app.DB_PATH = self.original_db_path
        career_app.UPLOAD_DIR = self.original_upload_dir

        self.tempdir.cleanup()

    def register(self, email="test@example.com"):
        return self.client.post(
            "/register",
            data={
                "name": "Test User",
                "email": email,
                "password": "strongpassword",
            },
            follow_redirects=True,
        )

    def test_home_page(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"CareerPilot", response.data)

    def test_register_and_dashboard(self):
        response = self.register()

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Good to see you", response.data)

    def test_duplicate_registration_is_handled(self):
        self.register()

        response = self.client.post(
            "/register",
            data={
                "name": "Test User",
                "email": "test@example.com",
                "password": "strongpassword",
            },
            follow_redirects=True,
        )

        self.assertIn(b"already exists", response.data)

    def test_login_logout(self):
        self.register()

        self.client.get("/logout", follow_redirects=True)

        response = self.client.post(
            "/login",
            data={
                "email": "test@example.com",
                "password": "strongpassword",
            },
            follow_redirects=True,
        )

        self.assertIn(b"Good to see you", response.data)

    def test_skill_detection_and_score(self):
        text = (
            "Professional Summary Python developer. "
            "Education: Diploma. Projects developed with "
            "Flask, MySQL, GitHub and Pandas. "
            "Certification completed."
        )

        skills = career_app.find_skills(text)
        score = career_app.calculate_score(text, skills)

        self.assertIn("python", skills)
        self.assertIn("flask", skills)
        self.assertGreater(score, 0)

    def test_protected_dashboard(self):
        response = self.client.get("/dashboard")

        self.assertEqual(response.status_code, 302)


if __name__ == "__main__":
    unittest.main()