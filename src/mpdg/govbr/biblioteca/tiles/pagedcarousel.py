# -*- coding: utf-8 -*-
import logging
from AccessControl import Unauthorized
from collective.cover import _
from collective.cover.tiles.base import IPersistentCoverTile, PersistentCoverTile
from plone.app.uuid.utils import uuidToCatalogBrain
from plone.tiles.interfaces import ITileDataManager
from plone.uuid.interfaces import IUUID
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from mpdg.govbr.biblioteca.content.arquivo_biblioteca import ArquivoBiblioteca

# TODO: efetuar esse import apenas se o produto mpdg.govbr.observatorio estiver instalado.
# Ex.: https://github.com/plone/plone.app.blocks/blob/master/plone/app/blocks/testing.py#L14
from mpdg.govbr.observatorio.browser.utils import ContadorManager

from mpdg.govbr.biblioteca.config import PROJECTNAME


logger = logging.getLogger(PROJECTNAME)


FILE_CONTENT_TYPES = ArquivoBiblioteca.dict_file_content_types


types_display = SimpleVocabulary(
    [SimpleTerm(value=u'recent', title=_(u'Recentes')),
     SimpleTerm(value=u'featured', title=_(u'Destaques'))]
    )

content_types = SimpleVocabulary(
    [SimpleTerm(value=u'ArquivoBiblioteca', title=_(u'Arquivos Biblioteca')),
    ]
    )

class IPagedCarouselTile(IPersistentCoverTile):
    """
    """

    type_display = schema.Choice(
        title=_(u'Critério de exibição'),
        vocabulary=types_display,
        required=True,
    )

    content_type = schema.Choice(
        title=_(u'Tipo de conteúdo'),
        vocabulary=content_types,
        required=True,
    )

#     form.widget(uuids=TextLinesSortableFieldWidget)
    uuids = schema.List(
        title=_(u'Elements'),
        value_type=schema.TextLine(),
        required=False,
        readonly=False,
    )

class PagedCarouselTile(PersistentCoverTile):
    is_configurable = True

    @property
    def portal_catalog(self):
        return self.context.portal_catalog

    def accepted_ct(self):
        """ Returna uma lista com os conteudos aceitos no tile
        """
        return ['Folder' , 'ArquivoBiblioteca']

    def populate_with_object(self, obj):
        super(PagedCarouselTile, self).populate_with_object(obj)  # check permission

        type_display = self.data.get('type_display', None)
        content_type = self.data.get('content_type', None)

        if (type_display in ['more_access', 'recent'] and obj.portal_type != 'Folder') \
           or (type_display == 'featured' and obj.portal_type != content_type):
            raise Unauthorized(
                _('You are not allowed to add content to this tile'))

        uuid = IUUID(obj, None)
        data_mgr = ITileDataManager(self)

        old_data = data_mgr.get()
        if data_mgr.get()['uuids']:
            uuids = data_mgr.get()['uuids']
            if type(uuids) != list:
                uuids = [uuid]
            elif uuid not in uuids:
                uuids.append(uuid)
            old_data['uuids'] = uuids
        else:
            old_data['uuids'] = [uuid]
        data_mgr.set(old_data)

    def get_related_brains(self):
        """ Obtem o brain do objeto cujo attr uuid faz referencia.
        """
        uuids = self.data.get('uuids', None)
        brains = []

        if uuids:
            for uuid in uuids:
                if uuidToCatalogBrain(uuid):
                    brains.append(uuidToCatalogBrain(uuid))
        return brains

    def get_childrens_brain_by_type(self, brain, content_type):
        """ Obtem os filhos de um objeto folder apartir de seu brain
        """
        brains = self.portal_catalog(path={'query': brain.getPath(), 'depth': 1}, portal_type=content_type)
        return (brain for brain in brains)

    def get_dados(self):
        """ Obtem os dados que serão usados no template
        """

        type_display = self.data.get('type_display', None)
        content_type = self.data.get('content_type', None)

        if type_display == 'featured':
            brains = self.get_related_brains()
        else:
            brains = []
            folders = self.get_related_brains()
            for folder in folders:
                brains += self.get_childrens_brain_by_type(folder, content_type)

        if brains:
            if type_display == 'more_access':
                brains.sort(key=lambda l: ContadorManager(l.UID).getAcesso(), reverse=True)
            else:
                brains.sort(key=lambda l: l.created, reverse=True)

        return {
            'type_display': type_display,
            'content_type': content_type,
            'list': [self._brain_for_dict(brain) for brain in brains if brain]
        }

    def _brain_for_dict(self, brain):
        '''
            Converte uma pagina em dicionario
        '''
        contador = ContadorManager(brain.UID)
        title = brain.Title
        data_object =  {
            'title': title,
            'url': brain.getURL()+'/view',
            'download': brain.getURL()+'/download',
            'created': brain.created.strftime('%d/%m/%Y'),
            'portal_type': brain.portal_type,
            'access': contador.getAcesso()
        }

        if brain.portal_type == 'ArquivoBiblioteca':
            data_object['file_size'] = brain.getObjSize

            obj = brain.getObject()
            if not title:
                data_object['title'] = obj.title_or_id()
            #Define e extensao do arquivo baseado no content_type do OBJ
            file_meta_type = obj.getContentType()

            file_type = ''
            for type in FILE_CONTENT_TYPES:
                if file_meta_type in FILE_CONTENT_TYPES[type]:
                    file_type = type
            if not file_type:
                file_type = 'OUTRO'

            data_object['content_type'] = file_type
            data_object['generic_type'] = obj.getTipo_arquivo()        

        return data_object
