#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
ddns use coredns etcd api
'''
import hashlib

from flask import Flask, render_template, request
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api, Resource, abort, reqparse

from etcdc import etcdc

auth = HTTPBasicAuth()


class Ddns(Resource):
    def __init__(self, *args, **kwargs):
        self.ec = etcdc.etcdc('http://127.0.0.1:2379')

    def get(self):
        ip = request.remote_addr
        return ip

    @auth.login_required
    def put(self, name, ip=None):
        ip = ip or request.remote_addr
        self.ec.dns(ip, name)
        return name+':'+ip, 201

def md5(src):
    m2 = hashlib.md5()
    m2.update(src.encode('utf-8'))
    return m2.hexdigest()

def create_app(config, name=__name__):
    app = Flask(name)
    app.config.from_pyfile(config, silent=False)
    user = app.config['USER']
    passwd = app.config['PASSWORD']

    @app.errorhandler(Exception)
    def internal_server_error(e):
        return '', 500

    @auth.verify_password
    def verify_password(username, password):
        if user == md5(username) and passwd == md5(password):
            return True
        return False

    api = Api(app)
    api.add_resource(Ddns, '/api/ddns', '/api/ddns/<name>',
                     '/api/ddns/<name>/<ip>')
    app.run(
        host=app.config['SERVER_HOST'],
        port=app.config['SERVER_PORT'],
        ssl_context=(app.config['SERVER_CERT'], app.config['SERVER_KEY'])
    )


if __name__ == '__main__':
    create_app('application.cfg')
