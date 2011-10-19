import settings
from twilio.rest import TwilioRestClient

class TwilioHelper(object):
    @classmethod
    def send_sms(klass, note, to_phone):
        client = TwilioRestClient(settings.TWILIO_SID, settings.TWILIO_TOKEN)
        try:
            message = client.sms.messages.create(to=to_phone,
                                             from_=settings.TWILIO_NUMBER,
                                             body=note)
            return True
        except Exception, e:
            print e
            return False