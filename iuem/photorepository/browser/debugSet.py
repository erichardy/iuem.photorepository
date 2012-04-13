from Products.Five import BrowserView


class create(BrowserView):
    """a view"""
    def go(self):
        imAlbumid="MyTestAlbum"
        imPhotoid=("MyTestPhoto1","MyTestPhoto2","MyTestPhoto3","MyTestPhoto4")
        
        debug="Creating imAlbum "+imAlbumid+"/n"
        try:
            self.context.invokeFactory(id=imAlbumid, type_name='imAlbum')
        except:
            debug=debug+" OOPS !! "+"/n"
        
        
        container = getattr(self.context, "MyTestAlbum", None)
        
        for photo in imPhotoid:
            debug=debug+"Creating imPhoto "+photo+"/n"
            try:
                container.invokeFactory(id=photo, type_name='imPhoto')
            except:
                debug=debug+" OOPS !! "+"/n"
            imPhotoSmallId=photo+"_small"
            debug=debug+"Creating imPhotoSmall "+imPhotoSmallId+"/n"
            try:
                container.invokeFactory(id=imPhotoSmallId, type_name='imPhotoSmall')
            except:
                debug=debug+" OOPS !! "+"/n"
        return debug
