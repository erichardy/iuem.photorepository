from zope.publisher.browser import BrowserView

class repoFolderAlbumView(BrowserView):
    """customization of atct_album_view
    """
    
    def general(self):
        return  eval(str(self.context.general))
    
    def science(self):
        return  eval(str(self.context.science))
    
    def where(self):
        return eval(str(self.context.where))
    
    def laboratory(self):
        return eval(str(self.context.laboratory))
    
    def reseachproject(self):
        return eval(str(self.context.reseachproject))
    
    def licencetype(self):
        return eval(str(self.context.licencetype))
    
    def recording_date_time(self):
        return str(self.context.recording_date_time)
    
    def photographer(self):
        return str(self.context.photographer)