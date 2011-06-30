from django.db import models
from django.contrib.sites.models import Site
from serializer import make_serializers

ENCODER, DECODER = make_serializers()

class Configuration(models.Model):
    key = models.CharField(max_length=50)
    site = models.ForeignKey(Site, blank=True, null=True)
    _data = models.TextField(db_column='data')
    
    def get_data(self):
        if self._data:
            return DECODER.decode(self._data)
        return {}
    
    def set_data(self, data):
        self._data = ENCODER.encode(data)
        
    data = property(get_data, set_data)
    
    @property
    def name(self):
        from configs import CONFIGS
        try:
            return CONFIGS[self.key].name
        except KeyError:
            return self.key

    def __unicode__(self):
        if self.site:
            return '%s (%s)' % (self.name, self.site)
        else:
            return '%s (Default)' % self.name
            
    class Meta:
        unique_together = [('key', 'site')]
