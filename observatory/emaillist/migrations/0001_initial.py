# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EmailExclusion'
        db.create_table(u'emaillist_emailexclusion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'emaillist', ['EmailExclusion'])


    def backwards(self, orm):
        # Deleting model 'EmailExclusion'
        db.delete_table(u'emaillist_emailexclusion')


    models = {
        u'emaillist.emailexclusion': {
            'Meta': {'object_name': 'EmailExclusion'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['emaillist']