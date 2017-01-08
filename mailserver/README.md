# Complete mail server with support for DKIM, SPF, spam classification and Sieve rules

This deploys a full SMTP server and IMAP server with support for:

- DKIM
- SPF
- spam classification and reclassification
- Sieve rules


## Spam handling

### Classification

Spam classification happens upon delivery, where the command `bogofilter-dovecot-deliver`
automatically runs unclassified mail through the `bogofilter` classifier, and then
pipes the result through the Dovecot LDA.

The LDA then runs the Sieve rules that inspect the headers (which contain the result
of the spam classification) and, as the first order of business, uses the sieve
rules deployed in `/var/lib/sieve/before.d` to classify the e-mails into the *SPAM*
folder if they have been detected as spam.

### Reclassification and retraining

If the classifier has made a mistake, you can reclassify e-mails as ham or as spam
by simply using your mail client as follows:

Move them from the folder they are stored in, into the folder *Mark as spam*
(for e-mail that was wrongly classified as proper e-mail) or into the folder
*Mark as ham* (for e-mail wrongly classified as spam).

When you move mails to *Mark as spam*, the server automatically runs them through
the `bogofilter` classifier and tells the classifer to deem this e-mail as spam.
Then, the server files the e-mail into the *SPAM* folder.

When you move mails to *Mark as ham*, the server automatically runs them
through the classifier, deeming them as ham (not spam); immediately after that,
the server moves them to the *INBOX* folder and marks them as unread (so you can
quickly spot them).
