# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Video.uploaded'
        db.alter_column('distributed_video', 'uploaded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True))


    def backwards(self, orm):
        
        # Changing field 'Video.uploaded'
        db.alter_column('distributed_video', 'uploaded', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True))


    models = {
        'distributed.files': {
            'Meta': {'object_name': 'Files'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uploaded': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'distributed.video': {
            'Meta': {'object_name': 'Video'},
            'converted': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uploaded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'video': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['distributed']
