# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'WorkSchedule.has_met'
        db.add_column('workschedule_workschedule', 'has_met',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'WorkSchedule.description'
        db.add_column('workschedule_workschedule', 'description',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding M2M table for field worker on 'WorkSchedule'
        db.create_table('workschedule_workschedule_worker', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('workschedule', models.ForeignKey(orm['workschedule.workschedule'], null=False)),
            ('worker', models.ForeignKey(orm['workschedule.worker'], null=False))
        ))
        db.create_unique('workschedule_workschedule_worker', ['workschedule_id', 'worker_id'])


    def backwards(self, orm):
        # Deleting field 'WorkSchedule.has_met'
        db.delete_column('workschedule_workschedule', 'has_met')

        # Deleting field 'WorkSchedule.description'
        db.delete_column('workschedule_workschedule', 'description')

        # Removing M2M table for field worker on 'WorkSchedule'
        db.delete_table('workschedule_workschedule_worker')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'workschedule.worker': {
            'Meta': {'object_name': 'Worker'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'worker_creator'", 'to': "orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'date_saved': ('django.db.models.fields.DateTimeField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.IntegerField', [], {}),
            'saved_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'worker_saved_by'", 'to': "orm['auth.User']"}),
            't_shirt_size': ('django.db.models.fields.IntegerField', [], {}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'workschedule.workerinschedule': {
            'Meta': {'object_name': 'WorkerInSchedule'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'workerinschedule_creator'", 'to': "orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'date_saved': ('django.db.models.fields.DateTimeField', [], {}),
            'has_met': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'saved_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'workerinschedule_saved_by'", 'to': "orm['auth.User']"}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'workers_in_schedule'", 'to': "orm['workschedule.WorkSchedule']"}),
            'worker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'in_schedules'", 'to': "orm['workschedule.Worker']"})
        },
        'workschedule.workschedule': {
            'Meta': {'object_name': 'WorkSchedule'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'workschedule_creator'", 'to': "orm['auth.User']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'date_saved': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            'has_met': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'saved_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'workschedule_saved_by'", 'to': "orm['auth.User']"}),
            'start_time': ('django.db.models.fields.TimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'worker': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'schedules'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['workschedule.Worker']"})
        }
    }

    complete_apps = ['workschedule']