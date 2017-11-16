# -*- coding: utf-8 -*-
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content.file import ATFile
from Products.Archetypes import atapi
from Products.Archetypes.utils import DisplayList
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.validation import V_REQUIRED
from plone.app.blob.content import ATBlobSchema
from plone.app.blob.field import BlobField, FileField
from zope.interface import implements

from mpdg.govbr.biblioteca import MessageFactory as _
from mpdg.govbr.biblioteca.config import PROJECTNAME
from mpdg.govbr.biblioteca.content.interfaces import IArquivoBiblioteca
# from liberiun.govtiles.models.accesspage import AccessPage
from mpdg.govbr.biblioteca.browser.utils import sizeof_fmt



ArquivoBibliotecaSchema = ATBlobSchema.copy() + atapi.Schema((

    atapi.ReferenceField(
        name='uid_pratica',
        relationship='uid_pratica',
        description='Caso este arquivo esteja associado a uma BoaPratica, definir nesse campo.',
        required=False,
        widget=ReferenceBrowserWidget(
            label=u'Referencia a BoaPratica'
        ),
        allowed_types=('BoaPratica',),
    ),

    FileField('file',
        required = True,
        primary = True,
        searchable = True,
        accessor = 'getFile',
        mutator = 'setFile',
        index_method = 'getIndexValue',
        languageIndependent = True,
        storage = atapi.AnnotationStorage(migrate=True),
        default_content_type = 'application/octet-stream',
        validators = (('isNonEmptyFile', V_REQUIRED),
                      ('checkFileMaxSize', V_REQUIRED)),
        widget = atapi.FileWidget(label = _(u'label_file', default=u'File'),
        description=_(u''),
        show_content_type = False,)
    ),

    atapi.StringField(
        name='tipo_arquivo',
        default=u'Arquivo',
        widget=atapi.SelectionWidget(label=_(u"Tipo do arquivo"),),
        required=True,
        vocabulary='vocTipoArquivo',
    ),

))


ArquivoBibliotecaSchema['title'].searchable = True
ArquivoBibliotecaSchema['description'].searchable = True
schemata.finalizeATCTSchema(ArquivoBibliotecaSchema)


class ArquivoBiblioteca(ATFile):
    """ Arquivo de biblioteca """

    implements(IArquivoBiblioteca)

    portal_type = "ArquivoBiblioteca"
    schema = ArquivoBibliotecaSchema

    _at_rename_after_creation = True

    dict_file_content_types = {
        'ODT' : ['application/vnd.oasis.opendocument.text', 'application/vnd.oasis.opendocument.text-master', 'application/vnd.oasis.opendocument.text-template'],
        'ODS' : ['application/vnd.oasis.opendocument.spreadsheet', 'application/vnd.oasis.opendocument.spreadsheet-template', 'application/vnd.openxmlformats-officedocument.spreadsheetml.template'],
        'ODP' : ['application/vnd.oasis.opendocument.presentation', 'application/vnd.oasis.opendocument.presentation-template'],
        'DOC' : ['application/msword','application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
        'XLS' : ['application/vnd.ms-excel', 'application/msexcel', 'application/x-msexcel','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'],
        'PPT' : ['application/powerpoint', 'application/mspowerpoint', 'application/x-mspowerpoint','application/vnd.openxmlformats-officedocument.presentationml.presentation'],
        'PPS' : ['application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.slideshow'],
        'PDF' : ['application/pdf', 'application/x-pdf', 'image/pdf'],
        'ZIP' : ['application/zip','multipart/x-zip', 'application/x-zip-compressed', 'application/x-compressed' ],
        'JPG' : ['image/jpeg'],
        'GIF' : ['image/gif' ],
        'PNG' : ['image/png' ],

    }

    def vocTipoArquivo(self):
        return DisplayList(((u'Apresentação', u'Apresentação'),
                            (u'Arquivo', u'Arquivo'),
                            (u'Artigo', u'Artigo'),
                            (u'Cartilha', u'Cartilha'),
                            (u'Documento', u'Documento')))

    def _obj_to_dict(self):
        uid = self.UID()
        # ap  = AccessPage()
        # if ap.store:

        result = {
            'title': self.Title(),
            'tipo_arquivo': self.vocTipoArquivo().getValue(self.getTipo_arquivo()),
            'created': self.created().strftime('%d/%m/%Y'),
            # 'access_count': ap.getAmountAccessByUid(uid),
            'size': sizeof_fmt(self.size()),
            'href': self.absolute_url()+'/view',
            }

        #Define e extensao do arquivo baseado no content_type do OBJ
        file_meta_type = self.getContentType()
        file_type = ''
        for type in self.dict_file_content_types:
            if file_meta_type in self.dict_file_content_types[type]:
                file_type = type
        if not file_type:
            file_type = 'TXT'
        result['format_file'] = file_type

        return result

    def SearchableText(self):
        """
        Override searchable text logic based on the requirements.

        This method constructs a text blob which contains all full-text
        searchable text for this content item.

        This method is called by portal_catalog to populate its SearchableText index.
        """
        entries = []

        # plain text fields we index from ourself,
        # a list of accessor methods of the class
        plain_text_fields = ("Title", "Description", "getId")

        # HTML fields we index from ourself
        # a list of accessor methods of the class
        # html_fields = ("getSummary", "getBiography")


        def read(accessor):
            """
            Call a class accessor method to give a value for certain Archetypes field.
            """
            try:
                value = accessor()
            except:
                value = ""

            if value is None:
                value = ""

            return value


        # Concatenate plain text fields as is
        for f in plain_text_fields:
            accessor = getattr(self, f)
            value = read(accessor)
            entries.append(value)

        # transforms = getToolByName(self, 'portal_transforms')

        # Run HTML valued fields through text/plain conversion
        # for f in html_fields:
        #     accessor = getattr(self, f)
        #     value = read(accessor)

        #     if value != "":
        #         stream = transforms.convertTo('text/plain', value, mimetype='text/html')
        #         value = stream.getData()

        #     entries.append(value)

        # Plone accessor methods assume utf-8
        def convertToUTF8(text):
            if type(text) == unicode:
                return text.encode("utf-8")
            return text

        entries = [ convertToUTF8(entry) for entry in entries ]

        # Concatenate all strings to one text blob
        return " ".join(entries)


atapi.registerType(ArquivoBiblioteca, PROJECTNAME)
