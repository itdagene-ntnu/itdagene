# -*- coding: utf-8 -*-
from optparse import make_option
from django.core.management.base import BaseCommand
import MySQLdb
from datetime import datetime
from itdagene.app.career.models import Town, Joblisting
from itdagene.app.company.models import Company, Comment, CompanyContact
from itdagene.core.models import User

def safe_unicode(obj):
    string = str(obj)
    return string.decode('latin1').encode('utf8')

class Command (BaseCommand):

    option_list = BaseCommand.option_list
    
    requires_model_validation = False
    help='Run the migration'
    def handle(self, *args, **options):
        """
        Will fetch data from the old site
        """
        with open('/django-sites/db-pw/old', 'rb') as f:
            db_password = f.readline()
        db_password = db_password.replace("\n","").strip()

        im_users = False
        im_companies = False
        im_comments = False
        im_company_contacts = False
        im_towns = True
        im_joblisting = True
        anonymous = User.objects.get(pk=1)

        conn = MySQLdb.connect (host = "127.0.0.1",
                                user = "itdagen_admin",
                                passwd = db_password,
                                db = "itdagen_itdagen")
        cursor = conn.cursor()

        if im_users:
            print "Importing users"
            count = 0
            cursor.execute('SELECT * FROM bruker')
            for u_row in cursor.fetchall():
                if int(u_row[1]) == 0:
                    user = User()
                    user.pk = int(u_row[0])
                    user.username = safe_unicode(u_row[3])
                    user.first_name = safe_unicode(u_row[5])
                    user.last_name = safe_unicode(u_row[6])
                    user.is_active = False
                    user.save()
                    if u_row[2]:
                        user.profile.year = int(u_row[2])
                    count += 1
                if (count % 10) == 0: print str(count) + ' users'
            print "============================"
            print "Imported " + str(count) + " users."
            print "============================"
            print
        if im_companies:
            print "Importing companies"
            count = 0
            cursor.execute('SELECT * FROM bedrift')
            for company_row in cursor.fetchall():
                company = Company(creator_id=1,saved_by_id=1, date_created=datetime.now(),date_saved=datetime.now())
                company.pk = int(company_row[0])
                company.name = safe_unicode(company_row[1])
                company.address = safe_unicode(company_row[2])
                company.payment_address = safe_unicode(company_row[3])
                company.fax = safe_unicode(company_row[4])
                company.phone = safe_unicode(company_row[5])
                company.url = safe_unicode(company_row[6])
                try:
                    company.description = safe_unicode(company_row[10])
                except UnicodeDecodeError:
                    pass
                company.save()
                count += 1
                if (count % 50) == 0: print str(count) + ' companies'
            print "============================"
            print "Imported " + str(count) + " companies."
            print "============================"
            print


        if im_comments:
            print "Importing company comments"
            count = 0
            cursor.execute('SELECT * FROM kommentar')
            for c_row in cursor.fetchall():
                try:
                    company = Company.objects.get(pk=int( c_row[1]))
                except:
                    company = None
                    print "Company not in database"
                try:
                    user = User.objects.get(pk=int(c_row[2]))
                except (TypeError, User.DoesNotExist):
                    user = User.objects.get(pk=1)
                if company:
                    comment = Comment()
                    comment.pk = int(c_row[0])
                    comment.company = company
                    comment.user = user
                    comment.timestamp = safe_unicode(c_row[3])
                    comment.content = safe_unicode(c_row[4])
                    comment.save()
                    count += 1
                    if (count % 200) == 0: print str(count) + ' comments'
            print "============================"
            print "Imported " + str(count) + " comments."
            print "============================"
            print

        if im_company_contacts:
            print "Importing company contacts"
            count = 0
            cursor.execute('SELECT * FROM kontaktperson')
            for c_row in cursor.fetchall():
                name = safe_unicode(c_row[2])
                if name != '':
                    try:
                        company = Company.objects.get(pk=int( c_row[1]))
                    except (TypeError, Company.DoesNotExist):
                        company = None
                        print "Company not in database"
                    if company:
                        contact = CompanyContact()
                        contact.company = company

                        name = name.split(' ')
                        first_name = ""
                        for i in xrange(len(name) - 1):
                            first_name += name[i] + ' '
                        contact.first_name = first_name.strip()
                        contact.last_name = name[len(name)-1]

                        contact.phone = safe_unicode(c_row[3])
                        contact.mobile_phone = safe_unicode(c_row[4])
                        contact.email = safe_unicode(c_row[5])
                        contact.position = safe_unicode(c_row[6])
                        contact.save()
                        count += 1
                        if (count % 50) == 0: print str(count) + ' contacts'
            print "============================"
            print "Imported " + str(count) + " contacts."
            print "============================"
            print

        if im_towns:
            print "Importing towns"
            count = 0
            cursor.execute('SELECT * FROM byer')
            for c_row in cursor.fetchall():
                town = Town(creator=anonymous, saved_by=anonymous, date_created=datetime.now(),date_saved=datetime.now())
                town.pk = int(c_row[0])
                town.name = safe_unicode(c_row[1])
                town.save()
                count += 1
            print "============================"
            print "Imported " + str(count) + " towns."
            print "============================"
            print

        if im_joblisting:
            print "Importing joblistings"
            count = 0
            cursor.execute('SELECT * FROM jobb')
            for c_row in cursor.fetchall():
                try:
                    company = Company.objects.get(pk=int( c_row[1]))
                except:
                    company = None
                    print "Company not in database"
                try:
                    town = Town.objects.get(pk=int(c_row[8]))
                except:
                    town = None
                    print "Town not in database"
                if company and town:
                    t = safe_unicode(c_row[5])
                    if t == 'Sommerjobb':
                        type = 'si'
                    elif t == 'Fast stilling':
                        type = 'pp'
                    else:
                        type = 'bi' #Bad import


                    jobl = Joblisting(creator=anonymous, saved_by=anonymous, date_created=datetime.now(),date_saved=datetime.now())
                    jobl.company = company
                    jobl.title = safe_unicode(c_row[2])
                    jobl.description = safe_unicode(c_row[3])
                    if c_row[4]:
                        jobl.deadline = safe_unicode(c_row[4])
                    jobl.type = type
                    jobl.from_year = safe_unicode(c_row[6])
                    jobl.to_year = safe_unicode(c_row[7])
                    jobl.save()
                    jobl.towns.add(town)
                    jobl.save()
                    count += 1
                    if (count % 200) == 0: print str(count) + ' joblistings'
            print "============================"
            print "Imported " + str(count) + " joblistings."
            print "============================"
            print

        cursor.close ()
        conn.close()
