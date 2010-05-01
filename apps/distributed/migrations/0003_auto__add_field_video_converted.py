# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Video.converted'
        db.add_column('distributed_video', 'converted', self.gf('django.db.models.fields.files.FileField')(default=1, max_length=100), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Video.converted'
        db.delete_column('distributed_video', 'converted')


    models = {
        'distributed.files': {
            'Meta': {'object_name': 'Files'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uploaded': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'distributed.video': {
            'Meta': {'object_name': 'Video'},
            'converted': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uploaded': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'video': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['distributed']
