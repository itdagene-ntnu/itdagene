# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EvaluationHash'
        db.create_table('feedback_evaluationhash', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('preference', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Preference'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['company.Company'])),
            ('hash', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
        ))
        db.send_create_signal('feedback', ['EvaluationHash'])

        # Adding unique constraint on 'EvaluationHash', fields ['preference', 'company']
        db.create_unique('feedback_evaluationhash', ['preference_id', 'company_id'])

        # Adding model 'Evaluation'
        db.create_table('feedback_evaluation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hash', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['feedback.EvaluationHash'])),
            ('internship_marathon_rating', self.gf('django.db.models.fields.IntegerField')()),
            ('internship_marathon_improvement', self.gf('django.db.models.fields.TextField')()),
            ('course_rating', self.gf('django.db.models.fields.IntegerField')()),
            ('course_improvement', self.gf('django.db.models.fields.TextField')()),
            ('visitors_rating', self.gf('django.db.models.fields.IntegerField')()),
            ('has_interview_location', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('interview_location_rating', self.gf('django.db.models.fields.IntegerField')()),
            ('interview_location_improvement', self.gf('django.db.models.fields.TextField')()),
            ('has_banquet', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('banquet_rating', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('banquet_improvement', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('improvement', self.gf('django.db.models.fields.TextField')()),
            ('other', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('want_to_come_back', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('feedback', ['Evaluation'])


    def backwards(self, orm):
        # Removing unique constraint on 'EvaluationHash', fields ['preference', 'company']
        db.delete_unique('feedback_evaluationhash', ['preference_id', 'company_id'])

        # Deleting model 'EvaluationHash'
        db.delete_table('feedback_evaluationhash')

        # Deleting model 'Evaluation'
        db.delete_table('feedback_evaluation')


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
        'company.company': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Company'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'contact_for'", 'null': 'True', 'to': "orm['auth.User']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'company_creator'", 'to': "orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'date_saved': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'has_public_profile': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'mp': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'companies'", 'null': 'True', 'to': "orm['company.Package']"}),
            'partner': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'payment_address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'saved_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'company_saved_by'", 'to': "orm['auth.User']"}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'company'", 'null': 'True', 'to': "orm['auth.User']"}),
            'waiting_for_package': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'waiting_list'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['company.Package']"})
        },
        'company.package': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Package'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'package_creator'", 'to': "orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'date_saved': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'has_stand_first_day': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_stand_last_day': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_waiting_list': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'includes_course': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_full': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'max': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'price': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'saved_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'package_saved_by'", 'to': "orm['auth.User']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.preference': {
            'Meta': {'object_name': 'Preference'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'preference_creator'", 'to': "orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'date_saved': ('django.db.models.fields.DateTimeField', [], {}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nr_of_stands': ('django.db.models.fields.PositiveIntegerField', [], {'default': '30'}),
            'saved_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'preference_saved_by'", 'to': "orm['auth.User']"}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'view_sp': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'feedback.evaluation': {
            'Meta': {'object_name': 'Evaluation'},
            'banquet_improvement': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'banquet_rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'course_improvement': ('django.db.models.fields.TextField', [], {}),
            'course_rating': ('django.db.models.fields.IntegerField', [], {}),
            'has_banquet': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_interview_location': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hash': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feedback.EvaluationHash']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'improvement': ('django.db.models.fields.TextField', [], {}),
            'internship_marathon_improvement': ('django.db.models.fields.TextField', [], {}),
            'internship_marathon_rating': ('django.db.models.fields.IntegerField', [], {}),
            'interview_location_improvement': ('django.db.models.fields.TextField', [], {}),
            'interview_location_rating': ('django.db.models.fields.IntegerField', [], {}),
            'other': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'visitors_rating': ('django.db.models.fields.IntegerField', [], {}),
            'want_to_come_back': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'feedback.evaluationhash': {
            'Meta': {'unique_together': "(('preference', 'company'),)", 'object_name': 'EvaluationHash'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['company.Company']"}),
            'hash': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'preference': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Preference']"})
        },
        'feedback.issue': {
            'Meta': {'object_name': 'Issue'},
            'app': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'assigned_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'assigned_issues'", 'null': 'True', 'to': "orm['auth.User']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'issue_creator'", 'to': "orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'date_saved': ('django.db.models.fields.DateTimeField', [], {}),
            'deadline': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_solved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'saved_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'issue_saved_by'", 'to': "orm['auth.User']"}),
            'solved_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['feedback']