from urllib import request
from http import cookiejar

WAYTOSMS_USERNAME = "<Registered Mobile Number>"
WAYTOSMS_PASSWORD = "<Password>"
WAYTOSMS_LOGIN_DATA_FORMAT = 'username={}&password={}&Submit=Sign+in'.format(WAYTOSMS_USERNAME, WAYTOSMS_PASSWORD)
WAYTOSMS_LOGIN_URL = "http://site24.way2sms.com/Login1.action?"
WAYTOSMS_SEND_SMS_URL = 'http://site24.way2sms.com/smstoss.action?'
WAYTOSMS_SEND_SMS_FORMAT = 'ssaction=ss&Token={}&mobile={}&message={}&msgLen=136'
WAYTOSMS_USERAGENT_HEADER = ('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120')
WAYTOSMS_REFERER_HEADER_FORMAT = 'http://site25.way2sms.com/sendSMS?Token={}'
FORGOT_PASSWORD_OTP_FORMAT = "OTP for forgot password is {}. Please don't share OTP with others.\n Happy tailoring !!!"


class WayToSMSHelper:

    def __init__(self):
        # logging into the sms site
        login_data = WAYTOSMS_LOGIN_DATA_FORMAT.format(WAYTOSMS_USERNAME, WAYTOSMS_PASSWORD).encode('utf-8')

        # For cookies
        cj = cookiejar.CookieJar()
        self.opener = request.build_opener(request.HTTPCookieProcessor(cj))

        # Adding header details
        self.opener.addheaders = [WAYTOSMS_USERAGENT_HEADER]
        try:
            self.opener.open(WAYTOSMS_LOGIN_URL, login_data)
        except IOError:
            print("IOError while login to waytsms")
            return
        self.session_id = str(cj).split('~')[1].split(' ')[0]
        self.opener.addheaders = [('Referer', WAYTOSMS_REFERER_HEADER_FORMAT.format(self.session_id))]

        print("success! logged into waytosms")

    def send_sms(self, number, message):
        message = "+".join(message.split(' '))
        send_sms_data = WAYTOSMS_SEND_SMS_FORMAT.format(self.session_id, number, message).encode('utf-8')
        try:
            self.opener.open(WAYTOSMS_SEND_SMS_URL, send_sms_data)
        except IOError:
            print("IOError while sending sms using waytsms")


if __name__ == '__main__':
    wts_helper = WayToSMSHelper()
    wts_helper.send_sms("<Mobile Number>", "<Message>")

