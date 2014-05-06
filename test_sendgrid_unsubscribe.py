"""Unit tests for the mass unsubscribe utility for sendgrid.

@author: Sam Pottinger (samnsparky, gleap.org)
@license: GNU GPL v3
"""

import unittest

import mox
import requests

import sendgrid_unsubscribe


class FakeRequestResponse:

    def __init__(self, response):
        self.response = response

    def json(self):
        return self.response


class SendgridUnsubscribeTests(mox.MoxTestBase):

    def test_delete_email_success(self):
        self.mox.StubOutWithMock(requests, 'post')
        
        requests.post(sendgrid_unsubscribe.LIST_DEL_URL, {
            'list': 'test_list',
            'api_user': 'test_api_user',
            'api_key': 'test_api_key',
            'email': 'test_email'
        }).AndReturn(FakeRequestResponse({'removed': 1}))

        self.mox.ReplayAll()

        result = sendgrid_unsubscribe.delete_email(
            'test_list',
            'test_api_user',
            'test_api_key',
            'test_email'
        )

        self.assertTrue(result['successful'])
        self.assertEqual(result['error'], None)

    def test_delete_email_fail(self):
        self.mox.StubOutWithMock(requests, 'post')
        
        requests.post(sendgrid_unsubscribe.LIST_DEL_URL, {
            'list': 'test_list',
            'api_user': 'test_api_user',
            'api_key': 'test_api_key',
            'email': 'test_email'
        }).AndReturn(FakeRequestResponse({'errors': ['err1', 'err2']}))

        self.mox.ReplayAll()

        result = sendgrid_unsubscribe.delete_email(
            'test_list',
            'test_api_user',
            'test_api_key',
            'test_email'
        )

        self.assertFalse(result['successful'])

    def test_delete_email_unexpected(self):
        self.mox.StubOutWithMock(requests, 'post')
        
        requests.post(sendgrid_unsubscribe.LIST_DEL_URL, {
            'list': 'test_list',
            'api_user': 'test_api_user',
            'api_key': 'test_api_key',
            'email': 'test_email'
        }).AndReturn(FakeRequestResponse({}))

        self.mox.ReplayAll()

        result = sendgrid_unsubscribe.delete_email(
            'test_list',
            'test_api_user',
            'test_api_key',
            'test_email'
        )

        self.assertFalse(result['successful'])

    def test_delete_emails(self):
        self.mox.StubOutWithMock(sendgrid_unsubscribe, 'delete_email')

        sendgrid_unsubscribe.delete_email(
            'test_list',
            'test_api_user',
            'test_api_key',
            'test_email_1'
        ).AndReturn({'successful': True, 'email': 'test_email_1'})

        sendgrid_unsubscribe.delete_email(
            'test_list',
            'test_api_user',
            'test_api_key',
            'test_email_2'
        ).AndReturn({'successful': False, 'email': 'test_email_2'})

        self.mox.ReplayAll()

        result = sendgrid_unsubscribe.delete_emails(
            'test_list',
            'test_api_user',
            'test_api_key',
            ['test_email_1', 'test_email_2']
        )

        successful = result['successful']
        failed = result['failed']

        self.assertEqual(len(successful), 1)
        self.assertEqual(successful[0]['email'], 'test_email_1')
        self.assertEqual(len(failed), 1)
        self.assertEqual(failed[0]['email'], 'test_email_2')

    def test_get_malformed_emails(self):
        results = sendgrid_unsubscribe.get_malformed_emails(
            ['test_email_1@example.com', 'test_email_2', 'test_email_3@t.com']
        )

        self.assertEqual(len(results[0]), 2)
        self.assertEqual(len(results[1]), 1)
        self.assertEqual(results[1][0], 'test_email_2')

    def test_stringify_email_errors(self):
        email_error_str = sendgrid_unsubscribe.stringify_email_errors([
            {'email': 'test_email_1', 'error': 'error 1'},
            {'email': 'test_email_2', 'error': 'error 2'}
        ])

        self.assertTrue('test_email_1' in email_error_str)
        self.assertTrue('error 2' in email_error_str)


if __name__ == '__main__':
    unittest.main()
