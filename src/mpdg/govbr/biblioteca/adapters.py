# -*- coding: utf-8 -*-

from zope.interface import implements
from zope.component import adapts

from plone.app.blob.interfaces import IBlobbable
from plone.app.blob.adapters.ofsfile import BlobbableOFSFile

from mpdg.govbr.biblioteca.content.interfaces import IArquivoBiblioteca


class BlobbableArquivoBiblioteca(BlobbableOFSFile):
    """ adapter for ATFile objects to work with blobs """
    implements(IBlobbable)
    adapts(IArquivoBiblioteca)

    def filename(self):
        """ see interface ... """
        return self.context.getFilename()
