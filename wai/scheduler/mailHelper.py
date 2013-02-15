from django.core.mail import EmailMultiAlternatives
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def mailWai(subject, message, sender, to, cc = "", replyTo = ""):
    msg = EmailMultiAlternatives(subject, strip_tags(message), sender, to, [], headers = {'Reply-To': replyTo, 'Cc': cc})
    msg.attach_alternative(message, "text/html")
    msg.send()
