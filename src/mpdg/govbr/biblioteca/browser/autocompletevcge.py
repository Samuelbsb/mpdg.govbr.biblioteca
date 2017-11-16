from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from zope import component, schema


class AutocompleteSearchVcge(BrowserView):
    
    def __call__(self):
        
        field = self.request.get('f', None)
        query = safe_unicode(self.request.get('q', ''))
        query = query.strip()
        if not query or not field:
            return ''
        
        factory = component.getUtility(schema.interfaces.IVocabularyFactory, name='brasil.gov.vcge')
        vocabulary = factory(self.context)
        vocab = {}
        for term in vocabulary:
            vocab[term.token] = term.title
        query = query.lower()
        vocab = vocab.items()
        results = [(value, title) for value, title in vocab if query in value.lower() or query in title.lower()]
        # print 'Search: ' + query
        
        return '\n'.join(["%s|%s" % (value, title) for value, title in results])
    
class AutocompletePopulateVcge(AutocompleteSearchVcge):
    
    def __call__(self):
        results = super(AutocompletePopulateVcge, self).__call__()
        results = results.split('\n')
        query = self.request.get('q', '')
        # print 'Populate: ' + query
        for r in results:
            if r.startswith(u'%s|' % safe_unicode(query)):
                return r