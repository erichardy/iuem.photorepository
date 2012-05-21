
from zope.publisher.browser import BrowserView
from iuem.photorepository.extender import ImageImageRepositoryExtender

class repoImageView(BrowserView):
    """new view for image repository
    """
    
    def unretour(self):
        context = self.context
        import pdb;pdb.set_trace()
        return "str(context.request) "

    def sourceImage(self):
        context = self.context
        return self.context.sourceImage.tag()
            