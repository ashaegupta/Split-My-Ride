import settings
from twilio.rest import TwilioRestClient

class TwilioHelper(object):
    @classmethod
    def send_sms(klass, note, to):
        client = TwilioRestClient(settings.TWILIO_SID, settings.TWILIO_TOKEN)
        try:
            message = client.sms.messages.create(to=to,
                                             from_=settings.TWILIO_NUMBER,
                                             body=note)
            print message.__dict__
            return True
        except Exception, e:
            print e
            return False