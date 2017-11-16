#-*- coding: utf-8 -*-
import unittest
from mpdg.govbr.biblioteca.testing import MPDG_GOVBR_BIBLIOTECA_INTEGRATION_TESTING


class ArquivoBibliotecaViewTest(unittest.TestCase):

    layer = MPDG_GOVBR_BIBLIOTECA_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_view_arquivobiblioteca(self):
        view = self.portal.restrictedTraverse('@@arquivobiblioteca-view')
        self.assertTrue(view)