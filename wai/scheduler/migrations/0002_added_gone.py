
from south.db import db
from django.db import models
from wai.scheduler.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Presenter.gone'
        db.add_column('scheduler_presenter', 'gone', orm['scheduler.presenter:gone'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Presenter.gone'
        db.delete_column('scheduler_presenter', 'gone')
        
    
    
    models = {
        'scheduler.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'scheduler.meeting': {
            'date': ('django.db.models.fields.DateField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Room']"})
        },
        'scheduler.presentation': {
            'abstract': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meeting': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Meeting']"}),
            'presenter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Presenter']"}),
            'slides': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'scheduler.presenter': {
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'gone': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'scheduler.room': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        }
    }
    
    complete_apps = ['scheduler']
