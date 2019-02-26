from django.test import TestCase

from ischool_classes import olddbservice


class OldDBServiceTestCase(TestCase):

    def setUp(self):
        self.db = olddbservice.iSchoolDBData()

    
    def test_get_waitlist_by_term(self):
        res = self.db.get_waitlist_by_term('1192', 'ndlyga')
        self.assertGreater(len(res), 0)
        self.assertEqual(res[0].termId, '1192')
        self.assertEqual(res[0].profNetId, 'ndlyga')