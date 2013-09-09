from zope.publisher.browser import BrowserView

class imDebug(BrowserView):
    def __call__(self):
        context = self.context
        import pdb;pdb.set_trace()