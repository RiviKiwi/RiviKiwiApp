from django.views.generic import TemplateView
import logging
logger = logging.getLogger('main_app')

class AboutView(TemplateView):

    template_name = "main/about.html"
    
    def get_context_data(self, **kwargs):
        logger.debug('render page about.html')
        return super().get_context_data(**kwargs)
