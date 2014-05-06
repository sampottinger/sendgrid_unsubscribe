"""Utility to unsubscribe users from Sendgrid list given a file of email addrs.

Script that unsubscribes all users in a provided text file from a Sendgrid list
via the Sendgrid API. Note that it requires the requests library (pip install
requests). Will remove all email addresses it can and report back which were
successfully removed and which were not.

USAGE: python unsubscribe.py path_to_users_list list_name api_user api_key

@author: Sam Pottiner (samnsparky, gleap.org)
@license: GNU GPL v3
"""

import itertools
import sys

import requests

LIST_DEL_URL = 'https://api.sendgrid.com/api/newsletter/lists/email/delete.json'
USAGE_STR = 'USAGE: python unsubscribe.py path_to_users_list list_name '\
    'api_user api_key'


def partition(pred, iterable):
    """Use predicate to partition entries into false entries and true entries.

    Thanks https://docs.python.org/dev/library/itertools.html.
    """
    t_1, t_2 = itertools.tee(iterable)
    return itertools.ifilterfalse(pred, t_1), filter(pred, t_2)


def delete_email(target_list, api_user, api_key, email_to_remove):
    """Removes the specified email address from the specified list.

    @param target_list: The name of the list to remove emails from.
    @type target_list: str
    @param api_user: The name of the API user to make the request on behalf of.
    @type api_user: str
    @param api_key: The API key associated with the provided api_user.
    @type api_key: str
    @param email_to_remove: The email address to remove.
    @type email_to_remove: str
    @return: Dictionary of form:
        'email': email address removed,
        'successful': boolean if removed or not,
        'error': None if no error. Otherwise description of error.
    @rtype: dict
    """
    params = {
        'list': target_list,
        'api_user': api_user,
        'api_key': api_key,
        'email': email_to_remove
    }
    request = requests.post(LIST_DEL_URL, params)
    result = request.json()

    if 'removed' in result and result['removed'] == 1:
        return {
            'successful': True,
            'error': None,
            'email': email_to_remove
        }
    elif 'errors' in result:
        return {
            'successful': False,
            'error': '\n'.join(result['errors']),
            'email': email_to_remove
        }
    else:
        return {
            'successful': False,
            'error': 'unknown',
            'email': email_to_remove
        }


def delete_emails(target_list, api_user, api_key, emails_to_remove):
    """Removes the specified email addresses from the specified list.

    @param target_list: The name of the list to remove emails from.
    @type target_list: str
    @param api_user: The name of the API user to make the request on behalf of.
    @type api_user: str
    @param api_key: The API key associated with the provided api_user.
    @type api_key: str
    @param emails_to_remove: The email addresses to remove.
    @type emails_to_remove: list of str
    @return: Dictionary of form:
        'email': email address removed,
        'successful': boolean if removed or not,
        'error': None if no error. Otherwise description of error.
    @rtype: dict
    """
    aut_delete_email = lambda x: delete_email(target_list, api_user, api_key, x)
    results = map(aut_delete_email, emails_to_remove)
    (failed, successful) = partition(lambda x: x['successful'], results)
    return {'successful': list(successful), 'failed': list(failed)}


def get_malformed_emails(target_list):
    """Look through a list of emails for those without an "@" sign.

    @param target_list: The list of emails to look through.
    @type target_list: list of str
    @return: Tuple of (list of str valid email addresses, list of str malformed
        email addresses).
    @rtype: tuple
    """
    email_has_at = lambda x: x.find('@') != -1
    (malformed_emails, valid_emails) = partition(email_has_at, target_list)
    return (list(valid_emails), list(malformed_emails))


def stringify_email_errors(results):
    """Format email deletion errors to display to user.

    @param results: The results from deleting email addresses from the Sendgrid
        list.
    @type results: list of dict
    @return: String describing the errors encountered.
    @rtype: str
    """
    stringify_email_err = lambda x: '%s (%s)' % (x['email'], x['error'])
    email_error_strs = map(stringify_email_err, results)
    email_errors = '\n\t-'.join(email_error_strs)
    return '[ ERROR ] Failed to remove emails:\n\t-%s' % email_errors


def main():
    """Routine to have unsubscribe run as a command line utility."""
    if len(sys.argv < 5):
        print USAGE_STR
        return

    # Read user command line arguments
    path_to_users_list = sys.argv[1]
    list_name = sys.argv[2]
    api_user = sys.argv[3]
    api_key = sys.argv[4]

    # Load list of email addresses to remove
    with open(path_to_users_list) as users_list_file:
        raw_list = users_list_file.read().split('\n')
        emails_to_rem = [x for x in raw_list if x != '']
        (valid_emails, malformed_emails) = get_malformed_emails(emails_to_rem)

    if len(malformed_emails) > 0:
        malformed_listing = '\n\t-'.join(malformed_emails)
        print '[ WARN ] Ignoring malformed emails:\n\t-%s' % malformed_listing
        print '[ INFO ] Removing %d email addresses.' % len(valid_emails)

    # Delete emails and report results
    results = delete_emails(list_name, api_user, api_key, valid_emails)

    report_attr = (len(results['successful']), len(results['failed']))
    print '[ INFO ] %d successfully removed. Failed to remove %d.' % report_attr

    if len(results['failed']) > 0:
        print stringify_email_errors(results['failed'])


if __name__ == '__main__':
    main()
