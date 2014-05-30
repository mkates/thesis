from django.test import TestCase
from analyze.helper import *

class PlayMatchTestCase(TestCase):
    def setUp(self):
       self.i = 1

    def test_matches_effective(self):
        mostLikelyPlay()
