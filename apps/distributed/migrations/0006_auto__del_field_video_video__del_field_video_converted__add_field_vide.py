# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Video.video'
        db.delete_column('distributed_video', 'video')

        # Deleting field 'Video.converted'
        db.delete_column('distributed_video', 'converted')

        # Adding field 'Video.file'
        db.add_column('distributed_video', 'file', self.gf('django.db.models.fields.files.FileField')(default=2, max_length=100), keep_default=False)

        # Adding field 'Video.file_converted'
        db.add_column('distributed_video', 'file_converted', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'Video.video'
        db.add_column('distributed_video', 'video', self.gf('django.db.models.fields.files.FileField')(default=2, max_length=100), keep_default=False)

        # Adding field 'Video.converted'
        db.add_column('distributed_video', 'converted', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True), keep_default=False)

        # Deleting field 'Video.file'
        db.delete_column('distributed_video', 'file')

        # Deleting field 'Video.file_converted'
        db.delete_column('distributed_video', 'file_converted')


    models = {
        'distributed.files': {
            'Meta': {'object_name': 'Files'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uploaded': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'distributed.video': {
            'Meta': {'object_name': 'Video'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'file_converted': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uploaded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['distributed']
