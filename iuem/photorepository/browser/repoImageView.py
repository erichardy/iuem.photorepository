
from zope.publisher.browser import BrowserView
from iuem.photorepository.extender import ImageImageRepositoryExtender

class repoImageView(BrowserView):
    """new view for image repository
    """
    
    def unretour(self):
        context = self.context
        # import pdb;pdb.set_trace()
        return "str(context.request) "

    def sourceImage(self):
        context = self.context
        tag = '<img src="' + context.absolute_url() + '/sourceImage" '
        tag += 'ALT="' + str(context.title) + '" '
        tag += 'title="' + str(context.title) + '" '
        tag += 'height="' + str(context.sourceImage.height) + '" '
        tag += 'width="' + str(context.sourceImage.width) + '" '
        tag += '/>'
        # import pdb;pdb.set_trace()
        return tag
    
    def viewImage(self):
        return self.context.tag()
            