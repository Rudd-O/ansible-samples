require ["vnd.dovecot.pipe", "copy", "imapsieve", "environment", "variables", "imap4flags"];

if environment :matches "imap.mailbox" "*" {
  set "mailbox" "${1}";
}

if string "${mailbox}" "Trash" {
  stop;
}

pipe :copy "learn-ham";
