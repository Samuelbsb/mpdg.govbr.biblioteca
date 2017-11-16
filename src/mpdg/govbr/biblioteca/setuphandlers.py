import logging
from Products.CMFCore.utils import getToolByName
from plone import api



# The profile id of your package:
PROFILE_ID = 'profile-mpdg.govbr.biblioteca:default'

class Empty:
    pass

def add_catalog_indexes(context, logger=None):
    """Method to add our wanted indexes to the portal_catalog.

    @parameters:

    When called from the import_various method below, 'context' is
    the plone site and 'logger' is the portal_setup logger.  But
    this method can also be used as upgrade step, in which case
    'context' will be portal_setup and 'logger' will be None.
    """
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('mpdg.govbr.biblioteca')

    # Run the catalog.xml step as that may have defined new metadata
    # columns.  We could instead add <depends name="catalog"/> to
    # the registration of our import step in zcml, but doing it in
    # code makes this method usable as upgrade step as well.  Note that
    # this silently does nothing when there is no catalog.xml, so it
    # is quite safe.
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'catalog')

    catalog = getToolByName(context, 'portal_catalog')
    indexes = catalog.indexes()
    # Specify the indexes you want, with ('index_name', 'index_type')
    wanted = (('orgparticipantes', 'FieldIndex'),
        ('tipo_arquivo', 'FieldIndex'),)

    indexables = []
    for name, meta_type in wanted:
        if name not in indexes:
            if meta_type == 'ZCTextIndex':
                item_extras = Empty()
                item_extras.doc_attr = name
                item_extras.index_type = 'Okapi BM25 Rank'
                item_extras.lexicon_id = 'plone_lexicon'
                catalog.addIndex(name, meta_type, item_extras)
            else:
                catalog.addIndex(name, meta_type)
            indexables.append(name)
            logger.info("Added %s for field %s.", meta_type, name)
    if len(indexables) > 0:
        logger.info("Indexing new indexes %s.", ', '.join(indexables))
        catalog.manage_reindexIndex(ids=indexables)

def create_folder_biblioteca(portal):
    portal_workflow = getToolByName(portal, 'portal_workflow')
    folder_documentos = portal.portal_catalog(portal_type="Folder", id="documentos-e-arquivos")
    if not folder_documentos:
        portal.portal_types.get('Folder').global_allow = True
        portal.invokeFactory('Folder',
                            id='documentos-e-arquivos',
                            title='Documentos da Biblioteca',
                            description='Pasta que os arquivos da Biblioteca',
                            excludeFromNav=True
        )

        folder_documentos = portal['documentos-e-arquivos']
        folder_documentos.setConstrainTypesMode(1)
        folder_documentos.setLocallyAllowedTypes(('Folder'))

        portal_workflow.doActionFor(folder_documentos, 'publish')
        # except:portal_workflow.doActionFor(folder_documentos, 'publish_internally')

def create_link_biblioteca(portal):
    portal = api.portal.get()
    try:
        servicos = portal['servicos']
    except KeyError:
        servicos = api.content.create(
            type='Folder',
            id='servicos',
            container=portal
        )
    if 'biblioteca' not in servicos:
        link_biblioteca = api.content.create(
            type='Link',
            remoteUrl='${portal_url}/acesso-a-informacao/biblioteca',
            title='Biblioteca',
            id='biblioteca',
            container= portal['servicos'])

def import_various(context):
    """Import step for configuration that is not handled in xml files.
    """

    logger = context.getLogger('mpdg.govbr.biblioteca')
    site = context.getSite()
    add_catalog_indexes(site, logger)
    create_folder_biblioteca(site)
