import asyncio
import unittest
import os
import uuid

from tempmailso import TempMailSo
from dotenv import load_dotenv

load_dotenv()

rapid_api_key = os.getenv("RAPID_API_KEY")
token_bearer = os.getenv("TOKEN_BEARER")
test_inbox_id = os.getenv("TEST_INBOX_ID")


class TestTempMailSo(unittest.TestCase):
    def test_get_domains(self):
        temp_mail_so = TempMailSo(rapid_api_key, token_bearer)
        domains = asyncio.run(temp_mail_so.list_domains())
        self.assertIsInstance(domains, list)
        self.assertGreater(len(domains), 0)
        name = uuid.uuid4().hex
        inbox = asyncio.run(temp_mail_so.create_inbox(
            name,
            domains[0]["domain"],
            600,
        ))
        self.assertIsInstance(inbox, dict)
        
        asyncio.run(temp_mail_so.delete_inbox(inbox.get("id")))

        inboxes = asyncio.run(temp_mail_so.list_inboxes())
        self.assertIsInstance(inboxes, list)
        self.assertGreater(len(inboxes), 0)

        emails = asyncio.run(temp_mail_so.list_emails(test_inbox_id))
        self.assertIsInstance(emails, list)
        self.assertGreater(len(emails), 0)

        email = asyncio.run(temp_mail_so.retrieve_email(test_inbox_id, emails[0].get("id")))
        self.assertIsInstance(email, dict)

        asyncio.run(temp_mail_so.delete_email(test_inbox_id, email.get("id")))


if __name__ == "__main__":
    unittest.main()