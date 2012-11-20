#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup
lookup = TemplateLookup(directories=['template/email', 'template'])

import string
import smtplib
from email.mime.text import MIMEText

import DatabaseParser
db = DatabaseParser

import Splitpot
import logging
log = logging.getLogger('appLog')


def sendMail(
    host,
    sender,
    to,
    subject,
    body,
    ):
    """
  Wrapper for the smtplib
  """

    msg = MIMEText(body)
    msg['From'] = sender
    msg['To'] = to
    msg['Subject'] = subject
    server = smtplib.SMTP(host)
    server.sendmail(sender, [to], msg.as_string())
    server.quit()


RUNNING_URL = 'http://0xabc.de/splitpot/'


def SettingsWrapper(to, subject, body):
    """
  Sends mail using sendMail-method. Adds the required parameters like host & sender from the config file
  """

  # TODO read from config file and provide login data

    log.info('sending mail to "' + to + '" with subject: "' + subject + '"')
    sendMail('localhost', 'splitpot@0xabc.de', to, subject, body)


def signupConfirm(email, key):
    """
  Sends the mail, that contains the activation url
  """

    log.info('sending signup confirmation to ' + email + ': ' + key)
    tmpl = lookup.get_template('signup_confirmation.email')
    SettingsWrapper(email, 'Signup Confirmation',
                    tmpl.render(url=RUNNING_URL + '/user/confirm?key='
                    + key))


def forgotConfirmation(email, key):
    """
  Sends the email with the url to confirm a password reset
  """

    log.info('sending a forgot-pwd-conf-key to ' + email + ': ' + key)
    tmpl = lookup.get_template('forgot_confirmation.email')
    SettingsWrapper(email, 'Password Reset',
                    tmpl.render(url=RUNNING_URL
                    + '/user/forgot_form?key=' + key))


def forgotNewPwd(email, pwd):
    """
  Sends the mail, that contains the freshly generated password for a user
  """

    log.info('sending a new pwd to ' + email + ': ' + pwd)  # TODO remove password from logging
    tmpl = lookup.get_template('forgot_success.email')
    SettingsWrapper(email, 'Info: Password reset successfully',
                    tmpl.render(pwd=pwd))


def payday(email, payments):
    """
  Sends a mail with all paiments of specific user. No changes on database/payments. This is only the helper for the template-retrieval
  """

    tmpl = lookup.get_template('payday.email')
    SettingsWrapper(email, 'Payday!', tmpl.render(payments))  # TODO enough data or more?


def mergeRequest(newEmail, oldEmail, key):
    """
    Send a confirmation mail to the mail address that is going to be merged.
    """

    log.info('sending an account merge confirmation link to "'
             + oldEmail.lower() + '"')

    tmpl = lookup.get_template('merge_request.email')
    SettingsWrapper(oldEmail, 'Account Merge Request',
                    tmpl.render(newEmail=newEmail, oldEmail=oldEmail, url=RUNNING_URL
                    + 'user/merge?key=' + key))


