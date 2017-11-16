from plone.i18n.normalizer import idnormalizer

def generateIdForContext(context, id, count=0):

    if getattr(context, id, False):
        if count > 0:
            id = id[:(len(str(count))+1)*-1]
        count += 1
        id = '%s-%s' % (id, count)
        return generateIdForContext(context, id, count)
    else:
        return id

def renameArqBiblioteca(context, event):

    file = context.getFile()
    filename = file.getFilename()
    id = (idnormalizer.normalize(filename))
    folder_context = context.aq_parent
    IdNovo = generateIdForContext(folder_context, id)
    context.setId(IdNovo)
    context.reindexObject()
    return 

