# Complete mail server with support for DKIM, SPF, spam classification and Sieve rules

This Ansible recipe deploys a full SMTP server and IMAP server compliant
with all the best practices for spam-free and good-delivery e-mail processing,
including (but not limited to) the following features:

- DKIM
- SPF
- spam classification and reclassification
- Sieve rules
- greylisting

## Greylisting

Your new mail server will reject any and all new e-mails from senders it hasn't
seen for 60 seconds.  This is *normal*.  The sending servers will retry after a
few minutes, after which the greylisting process will determine that the e-mail
is legitimate.

If you want to whitelist specific servers or domains for sending you e-mail
without greylisting, you can do so by adding rules to the files
`/etc/postfix/postgrey_whitelist_clients.local`.  See the documentation for
*Postgrey whitelist* online to understand what to put in that file.

## Spam handling

### Automatic classification

Spam classification happens upon delivery, where the command
`bogofilter-dovecot-deliver` automatically runs unclassified mail through the
`bogofilter` classifier, and then pipes the result through the Dovecot LDA.

The LDA then runs the Sieve rules that inspect the headers (which contain the
result of the spam classification) and, as the first order of business, uses
the sieve rules deployed in `/var/lib/sieve/before.d` to classify the e-mails
into the *SPAM* folder if they have been deemed to be spam.

Because the rule that classifies mail as spam executes before your own Sieve
rules, all of your e-mail will go through the classifier.  This may mean that,
during the first few days, `bogofilter` will have to catch up with what *you*
understand as spam and not spam, and a few e-mails will be misclassified.
Worry not, as the process is very easy (see the next section) and `bogofilter`
learns very quickly what counts as spam and what doesn't.

**SPF and DKIM interaction with spam handling**: `bogofilter` takes into
account mail headers when deciding what is spam and what isn't, so the headers
added by the SPF and DKIM validators will inform `bogofilter` quite reliably as
to the legitimacy of the e-mail it's receiving for classification.

### Reclassification and retraining

If the classifier has made a mistake, you can reclassify e-mails as ham or as
spam by simply using your mail client as follows:

Move them from the folder they are stored in, into the folder *Mark as spam*
(for e-mail that was wrongly classified as proper e-mail) or into the folder
*Mark as ham* (for e-mail wrongly classified as spam).

When you move mails to *Mark as spam*, the server automatically runs them
through the `bogofilter` classifier again, telling the classifer to deem those
messages as spam.  Then, the server files the e-mail into the *SPAM* folder.

When you move mails to *Mark as ham*, the server automatically runs them
through the classifier, deeming them as ham (not spam); immediately after that,
the server moves them to the *INBOX* folder and marks them as unread (so you
can quickly spot them).  From the *INBOX* folder, you can then sort your
newly-unspammed e-mails into the right folders.

You'll discover quite quickly that `bogofilter` learns really well what
qualifies as spam and what does not, according to your own criteria.  It's
almost magic.  After a few days, pretty much every e-mail will be correctly
classified, with a false positive and false negative rate of less than 0.1%.
