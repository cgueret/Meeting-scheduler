
from south.db import db
from django.db import models
from wai.scheduler.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Presentation'
        db.create_table('scheduler_presentation', (
            ('id', orm['scheduler.Presentation:id']),
            ('meeting', orm['scheduler.Presentation:meeting']),
            ('presenter', orm['scheduler.Presentation:presenter']),
            ('slides', orm['scheduler.Presentation:slides']),
            ('title', orm['scheduler.Presentation:title']),
            ('abstract', orm['scheduler.Presentation:abstract']),
        ))
        db.send_create_signal('scheduler', ['Presentation'])
        
        # Adding model 'Meeting'
        db.create_table('scheduler_meeting', (
            ('date', orm['scheduler.Meeting:date']),
            ('location', orm['scheduler.Meeting:location']),
        ))
        db.send_create_signal('scheduler', ['Meeting'])
        
        # Adding model 'Room'
        db.create_table('scheduler_room', (
            ('id', orm['scheduler.Room:id']),
            ('name', orm['scheduler.Room:name']),
            ('note', orm['scheduler.Room:note']),
        ))
        db.send_create_signal('scheduler', ['Room'])
        
        # Adding model 'Presenter'
        db.create_table('scheduler_presenter', (
            ('id', orm['scheduler.Presenter:id']),
            ('name', orm['scheduler.Presenter:name']),
            ('group', orm['scheduler.Presenter:group']),
            ('email', orm['scheduler.Presenter:email']),
            ('note', orm['scheduler.Presenter:note']),
        ))
        db.send_create_signal('scheduler', ['Presenter'])
        
        # Adding model 'Group'
        db.create_table('scheduler_group', (
            ('id', orm['scheduler.Group:id']),
            ('name', orm['scheduler.Group:name']),
        ))
        db.send_create_signal('scheduler', ['Group'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Presentation'
        db.delete_table('scheduler_presentation')
        
        # Deleting model 'Meeting'
        db.delete_table('scheduler_meeting')
        
        # Deleting model 'Room'
        db.delete_table('scheduler_room')
        
        # Deleting model 'Presenter'
        db.delete_table('scheduler_presenter')
        
        # Deleting model 'Group'
        db.delete_table('scheduler_group')
        
    
    
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
