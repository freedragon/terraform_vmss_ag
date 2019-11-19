#!/usr/bin/python3

# simple HTTP server which run a simple page for health probe

from bottle import route, run, redirect, response

hostname = '0.0.0.0'
hostport = 9000

def writebody():
    body = '<html><head><title>VM Health Check</title></head>'
    body += '<body><h2> ' + hostname + ' is Healthy </h2><ul><h3></body></html>'
    return body


@route('/')
def root():
    return writebody()


@route('/health')
def isHealthy():
        return writebody()

run(host=hostname, port=hostport)
