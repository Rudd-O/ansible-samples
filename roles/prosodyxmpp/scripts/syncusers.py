#!/usr/bin/env python

import glob, os, urllib, subprocess, sys


def x():
        accts = glob.glob("/var/lib/prosody/*/accounts/*.dat")
        accts = [urllib.unquote(s[len("/var/lib/prosody/"):-4]) for s in accts]
        accts = [(x.split(os.path.sep)[0], x.split(os.path.sep)[-1]) for x in accts]
        user, domain = sys.argv[1].split("@", 1)
        password = sys.argv[2]
        exists = False
        for existing_domain, existing_user in accts:
            if existing_domain == domain and existing_user == user:
                exists = True
        if not exists:
            p = subprocess.Popen(["prosodyctl", "adduser", sys.argv[1]],
                                 stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            stdout, _ = p.communicate("%s\n%s\n" % (password, password))
            print >> sys.stdout, stdout,
            ret = p.wait()
            if ret != 0:
                if "That user already exists" in stdout:
                    pass
                else:
                    assert 0, "prosodyctl ended with abnormal return code %s" % ret
            else:
                print "CHANGED: Created  new account %s@%s" % (user, domain)

x()
