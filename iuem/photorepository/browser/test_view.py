from Products.Five import BrowserView

class testView(BrowserView):
    """a view for test...
    """
    
    def howToAccessFormData(self):
        # import pdb;pdb.set_trace()
        return "It's a mystery... ;-("
    
    def vehicle(self):
        return self.request.form['form.widgets.vehicle'][0]
    
    def destination(self):
        return self.request.form['form.widgets.destination'][0]
        