from django.test import TestCase
from itdagene.app.mail.models import MailMapping
from itdagene.core.models import User
from django.contrib.auth.models import Group
from itdagene.app.mail.logic import handle_mail
import email

class MailTestCase(TestCase):
    def setUp(self):
        group = Group(name='test_group')
        user = User(username='test_user', email='testuser@sylliaas.no')
        user1 = User(username='test_user1', email='testuser1@sylliaas.no')
        group.save()
        user.save()
        user.groups.add(group)
        user.save()
        user1.save()
        mapping = MailMapping(address='test')
        mapping.save()
        mapping.users.add(user)
        mapping.users.add(user1)
        mapping.groups.add(group)
        mapping.save()


    def test_handle_mail(self):
        message = """
        From nobody Fri Sep 26 00:53:12 2014
        Received: from smtp.domeneshop.no (smtp.domeneshop.no [194.63.252.55])
        by private.sylliaas.no (Postfix) with ESMTPS id 68B641A33D0
        for <test@test.sylliaas.no>; Fri, 26 Sep 2014 00:53:12 +0200 (CEST)
        Received: from ns166b.studby.ntnu.no ([129.241.125.166]:55694
        helo=[192.168.1.206])
        by smtp.domeneshop.no with esmtpsa (TLS1.0:RSA_AES_128_CBC_SHA1:128)
        (Exim 4.80) (envelope-from <eirik@sylliaas.no>) id 1XXHv0-0001t0-7q
        for test@test.sylliaas.no; Fri, 26 Sep 2014 00:53:46 +0200
        From: Eirik Martiniussen Sylliaas <eirik@sylliaas.no>
        Content-Type: text/plain; charset=us-ascii
        Content-Transfer-Encoding: 7bit
        Subject: last test
        Message-Id: <7E10F820-3F12-4DF1-978B-E7C7F55E5235@sylliaas.no>
        Date: Fri, 26 Sep 2014 00:53:44 +0200
        To: test@test.sylliaas.no
        Mime-Version: 1.0 (Mac OS X Mail 7.3 \(1878.6\))
        X-Mailer: Apple Mail (2.1878.6)

        this is the latest test
        """
        message = email.message_from_string(message)
        self.assertEqual(handle_mail(message, 'eirik@sylliaas.no', 'test@itdagene.no'), {})