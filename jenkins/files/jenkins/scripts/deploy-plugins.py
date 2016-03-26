#!/usr/bin/env python

import os
import sys
import time
import yaml
import zipfile

from httplib import HTTPConnection, HTTPSConnection
from urlparse import urlparse
from xml.dom.minidom import parseString

try:
    jenkins = yaml.load(sys.argv[1])
except Exception, e:
    assert 0, (e, sys.argv[1])

jenkins_url = jenkins.get("url", "http://localhost:8080")
netloc = urlparse(jenkins_url).netloc
jenkins_class = HTTPSConnection if jenkins_url.startswith("https") else HTTPConnection
jenkins_path = jenkins.get("path", "/var/lib/jenkins")
jenkins_plugin_path = os.path.join(jenkins_path, "plugins")

def existing_plugins_and_versions():
    conn = jenkins_class(netloc)
    try:
        url = jenkins_url + "/pluginManager/api/xml?depth=1&xpath=/*/*/shortName|/*/*/version&wrapper=plugins"
        conn.request('GET', url)
        response = conn.getresponse().read()
    except Exception, e:
        raise Exception("Failed to connect to Jenkins with error %s.  URL: %s" % ( e, url ))
    parsed = parseString(response)
    shortnames = parsed.getElementsByTagName("shortName")
    versions = parsed.getElementsByTagName("version")
    plugin_names_and_versions = dict()
    for n, v in zip(shortnames, versions):
        n = "".join(c.nodeValue for c in n.childNodes)
        v = "".join(c.nodeValue for c in v.childNodes)
        plugin_names_and_versions[n.encode("utf-8")] = v.encode("utf-8")
    return plugin_names_and_versions

def request_install_of_plugins(plugins_to_install):
    "Returns changed and could_not_install."
    to_install = set(plugins_to_install) - set(existing_plugins_and_versions())
    if not to_install:
        return False, []
    if to_install:
        shell = '<jenkins>%s</jenkins>'
        plugreq = '<install plugin="%s@latest" />'

        p = "".join([plugreq % t for t in to_install])
        text = shell % p
        conn = jenkins_class(netloc)
        conn.request(
            'POST',
            jenkins_url + '/pluginManager/installNecessaryPlugins',
            text,
            {"Content-Type": "text/xml"},
        )
        response = conn.getresponse().read()
    for _ in range(30):
        remaining_to_install = set(plugins_to_install) - set(existing_plugins_and_versions())
        if remaining_to_install:
            time.sleep(1)
            continue
        return True, list(to_install)
    return True, list(remaining_to_install)

def run():
    changed, could_not_install = request_install_of_plugins(jenkins['plugins'])
    assert not could_not_install, could_not_install
    if changed:
        print "CHANGED"

run()
