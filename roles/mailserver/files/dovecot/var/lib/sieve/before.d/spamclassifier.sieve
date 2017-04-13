require ["fileinto", "vnd.dovecot.filter"];

filter "spamclassifier";

if anyof (
	header :contains ["X-Spam-Flag"] ["yes"],
	header :contains ["X-Bogosity"] ["Spam,"]
) {
  fileinto "SPAM";
}
