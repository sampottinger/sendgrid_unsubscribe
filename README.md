Sendgrid Mass Unsubscribe Utility
=================================
Keep it simple: given a text file where each line contains an email address,
this utility can remove each email address from a SendGrid mailing list in bulk.

<br>
Installation
------------
 * Get Python and Pip ([Windows](http://docs.python-guide.org/en/latest/starting/install/win/), [Mac](http://docs.python-guide.org/en/latest/starting/install/osx/) , [Linux](http://docs.python-guide.org/en/latest/starting/install/linux/))
 * Get [Git](http://git-scm.com/book/en/Getting-Started-Installing-Git)
 * ```git clone https://github.com/Samnsparky/sendgrid_unsubscribe.git```
 * ```pip install -r requirements.txt```

<br>
Usage
-----
```python unsubscribe.py path_to_users_list list_name api_user api_key```

Arguments:

 - **path_to_users_list**: The path to the text file with email addresses to remove from the mailing list. Should be a text file where each line contains an email address to remove. Blank lines ignored.
 - **list_name**: The name of the SendGrid list to remove the email addresses from.
 - **api_user**: Your Sendgrid username (api user) / the sendgrid username (api user) to act on behalf of.
 - **api_key**: The API key to use to log into Sendgrid with.

<br>
Authors, License, and Development
---------------------------------
Released under the GNU GPL v3. Copyright Sam Pottinger, 2014. Unit tests in test_sendgrid_unsubscribe.py. Epydoc docstrings used.
