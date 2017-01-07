require "fileinto";

if anyof (
	header :contains ["X-Spam-Flag"] ["yes"],
	header :contains ["X-Bogosity"] ["Spam,"]
) {
  fileinto "SPAM";
}
