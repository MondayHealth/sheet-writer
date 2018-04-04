from __future__ import print_function

import base64
import datetime
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import MutableMapping

from apiclient import discovery
# noinspection PyPackageRequirements
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
from pytz import timezone

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = os.path.abspath('./s_private_key.json')

CONTENT_A = """<!DOCTYPE html> <html lang=en xmlns=http://www.w3.org/1999/xhtml xmlns:v=urn:schemas-microsoft-com:vml xmlns:o=urn:schemas-microsoft-com:office:office> <head> <meta charset=utf-8> <meta name=viewport content="width=device-width"> <meta http-equiv=X-UA-Compatible content="IE=edge"> <meta name=x-apple-disable-message-reformatting> <title></title> <!--[if mso]> <style>*{font-family:Nunito,sans-serif!important}</style> <![endif]--> <!--[if !mso]><!--> <link rel=stylesheet type=text/css href="https://fonts.googleapis.com/css?family=Nunito:900,700,400%7CPT+Serif:700i,700,400i,400"> <!--<![endif]--> <style>html,body{margin:0 auto!important;padding:0!important;height:100%!important;width:100%!important}*{-ms-text-size-adjust:100%;-webkit-text-size-adjust:100%}div[style*="margin: 16px 0"]{margin:0!important}table,td{mso-table-lspace:0!important;mso-table-rspace:0!important}table{border-spacing:0!important;border-collapse:collapse!important;table-layout:fixed!important;margin:0 auto!important}table table table{table-layout:auto}img{-ms-interpolation-mode:bicubic}*[x-apple-data-detectors],.x-gmail-data-detectors,.x-gmail-data-detectors *,.aBn{border-bottom:0!important;cursor:default!important;color:inherit!important;text-decoration:none!important;font-size:inherit!important;font-family:inherit!important;font-weight:inherit!important;line-height:inherit!important}.a6S{display:none!important;opacity:.01!important}img.g-img+div{display:none!important}.button-link{text-decoration:none!important}@media only screen and (min-device-width:320px) and (max-device-width:374px){.email-container{min-width:320px!important}}@media only screen and (min-device-width:375px) and (max-device-width:413px){.email-container{min-width:375px!important}}@media only screen and (min-device-width:414px){.email-container{min-width:414px!important}}</style> <style>.button-td,.button-a{transition:all 100ms ease-in}.button-td:hover,.button-a:hover{background:#555555!important;border-color:#555555!important}a{font-weight:700!important}@media screen and (max-width:600px){.email-container p{font-size:17px!important}}</style> <!--[if gte mso 9]> <xml> <o:OfficeDocumentSettings> <o:AllowPNG/> <o:PixelsPerInch>96</o:PixelsPerInch> </o:OfficeDocumentSettings> </xml> <![endif]--> </head> <body width=100% bgcolor=#222222 style=margin:0;mso-line-height-rule:exactly> <div style=width:100%;background:#fff3f4;text-align:left> <div style=display:none;font-size:1px;line-height:1px;max-height:0;max-width:0;opacity:0;overflow:hidden;mso-hide:all;font-family:sans-serif> </div> <div style=max-width:600px;margin:auto class=email-container> <!--[if mso]> <table role=presentation cellspacing=0 cellpadding=0 border=0 width=600 align=center> <tr> <td> <![endif]--> <table role=presentation cellspacing=0 cellpadding=0 border=0 align=center width=100% style=max-width:600px> <tr> <td style="padding:20px 0;text-align:center"> <img src="https://static1.squarespace.com/static/5a660035bff200b621e41423/t/5a660a8ac83025db5a384c71/1518299107742/?format=1500w" width=160 height=40 alt="Monday Health" border=0 style=height:auto;background:0;font-family:sans-serif;font-size:15px;line-height:140%;color:#555> </td> </tr> </table> <table role=presentation cellspacing=0 cellpadding=0 border=0 align=center width=100% style=max-width:600px> <tr> <td bgcolor=#ffffff> <table role=presentation cellspacing=0 cellpadding=0 border=0 width=100%> <td style=padding:40px;font-family:sans-serif;font-size:15px;line-height:140%;color:#555> <div><div><div><div style=color:rgb(0,0,0);font-family:arial,sans-serif;font-size:medium><font color=#555555 face=sans-serif><span style=font-size:15px>Hey """

CONTENT_B = """,</span></font></div><div style=color:rgb(0,0,0);font-family:arial,sans-serif;font-size:medium><font color=#555555 face=sans-serif><span style=font-size:15px>&nbsp;</span></font></div><div><div><span style=font-size:15px;background-color:rgb(255,255,255)><font color=#555555 face=sans-serif>Thanks for getting in touch! We'll get back to you within the next 48-72 hours with therapist recommendations that meet your needs.<br><br>Please don't hesitate to reach out if you have any questions about Monday or therapy in general. We're here for you.<br><br>Be well,<br>Monday</span></div></div></div></div> </td> </tr> </table> </td> </tr> </table> <table role=presentation cellspacing=0 cellpadding=0 border=0 align=center width=100% style=max-width:680px;font-family:sans-serif;color:#888;font-size:12px;line-height:140%> <tr> <td style="padding:40px 10px;width:100%;font-family:sans-serif;font-size:12px;line-height:140%;text-align:center;color:#888" class=x-gmail-data-detectors> © 2018 Monday Health Inc.<br>201 E 25th Street, New York, NY 10010<br><a href=mailto:hello@mondayhealth.com>hello@mondayhealth.com</a><br><br><a href=https://www.monday.health/terms/>Terms of Use</a> | <a href=https://www.monday.health/privacypolicy/>Privacy Policy</a> <br><br> </td> </tr> </table> <!--[if mso]> </td> </tr> </table> <![endif]--> </div> </div> </body> </html>"""

FROM = "Monday Health <recommendations@mondayhealth.com>"

BCC_RECIPIENTS = ["chris@mondayhealth.com", "enrique@mondayhealth.com"]

TIMEZONE = "US/Eastern"

required_fields = [
    "first", "last", "email", "age", "zip"
]

optional_fields = [
    "provider-gender", "phone", "lang", "max-spend", "other", "patient-gender",
    "experience", "tell-us", "insurance"
]

field_order = [
    "date", "time", "problem", "first", "last", "email", "phone", "age", "zip",
    "insurance", "provider-gender", "lang", "max-spend", "other",
    "patient-gender", "experience", "tell-us"
]


def send_mail(body):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        SERVICE_ACCOUNT_FILE, scopes=[
            "https://www.googleapis.com/auth/gmail.send"
        ])

    # YOU NEED TO PUT THE CLIENT ID IN THE FIELD. NOT THE ADDRESS
    # https://admin.google.com/AdminHome?fral=1&chromeless=0#OGX:ManageOauthClients
    address = "enrique@mondayhealth.com"
    credentials = credentials.create_delegated(address)
    gmail = discovery.build('gmail', 'v1', credentials=credentials)

    try:
        message = (gmail.users().messages().send(userId=address, body=body)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except Exception as error:
        print('An error occurred: %s' % error)


def create_message(to, name):
    simple = MIMEText("Hey " + name + """, 
    Thanks for getting in touch! We'll get back to you within the next 48-72 hours with therapist recommendations that meet your needs.
    
    Please don't hesitate to reach out if you have any questions about Monday or therapy in general. We're here for you.
    
    Be well,
    Monday""", 'plain')
    html = MIMEText(CONTENT_A + name + CONTENT_B, 'html')
    message = MIMEMultipart('alternative')
    message['to'] = to
    message['from'] = FROM
    message['subject'] = "Welcome to Monday!"
    message['bcc'] = ", ".join(BCC_RECIPIENTS)
    message.attach(simple)
    message.attach(html)
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


def service():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return discovery.build('sheets', 'v4', credentials=credentials)


def add_values(values):
    spreadsheet_id = '1zGH6qgBABvchyu3C1rCexqHSL3rIzSmJbyM30DRxnDk'

    # The A1 notation of a range to search for a logical table of data.
    # Values will be appended after the last row of the table.
    range_ = 'A1:' + chr(ord('a') + len(values)).upper() + '1'

    value_range_body = {
        "majorDimension": "ROWS",
        "range": range_,
        "values": [values]
    }

    request = service().spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range_,
        valueInputOption='RAW',
        body=value_range_body)

    return request.execute()


def _error(reason: str):
    return {"success": False, "reason": reason}


def lambda_entry(params: dict, context):
    if 'problem' not in params:
        return _error("no problem array")

    try:
        iter(params['problem'])
    except TypeError:
        return _error("problem is not an iterable")

    tz = timezone(TIMEZONE)
    now: datetime.datetime = datetime.datetime.now(tz)
    found: MutableMapping[str, str] = {
        "date": "{0:%m/%d/%Y}".format(now),
        "time": "{0:%H:%M:%S}".format(now),
        "problem": ", ".join(params['problem'])
    }

    for required in required_fields:
        val = params.get(required, "")
        if not val:
            return _error("missing required field: " + required + " " + val)
        if len(val) > 256:
            return _error("param " + required + " too long")
        found[required] = val

    for optional in optional_fields:
        val = params.get(optional, "")
        if len(val) > 512:
            return _error("param " + optional + " too long")
        found[optional] = val

    # Do it
    add_values(list(map(lambda x: found[x], field_order)))

    # Send an email
    send_mail(create_message(params.get("email"), params.get("first")))

    return {'success': True}


def command_line():
    # send_mail(create_message("ixplode@gmail.com", "christopher"))
    tz = timezone(TIMEZONE)
    now: datetime.datetime = datetime.datetime.now(tz)
    found: MutableMapping[str, str] = {
        "date": "{0:%m/%d/%Y}".format(now),
        "time": "{0:%H:%M:%S}".format(now)
    }
    print(now)
    print(found)


if __name__ == '__main__':
    command_line()
