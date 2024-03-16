#!/usr/bin/python3
"""
Simple Passbolt Client
"""
import json
import urllib
import uuid
import requests
import pgpy

class BoltException(Exception):
    """Passbolt library exception"""
    def __init__(self, msg, descr=None):
        self.msg = msg
        self.descr = descr

    def __repr__(self):
        s = f"PASSBOLT LIB EXCEPTION: {self.msg}"
        if self.descr:
            s+=f"\n\n{self.descr}"
        return s

class Bolt:
    """Passbolt API class abstraction"""
    def __init__(self, base_url, privkey_filename, passphrase):
        self.base_url = base_url
        self.privkey, _ = pgpy.PGPKey.from_file(privkey_filename)
        self.passphrase = passphrase
        self.session_cookies = None

    def get_server_pubkey(self):
        "return server public key"
        r = requests.get(f'{self.base_url}/auth/verify.json?api-version=v2')
        if r.status_code != 200:
            raise BoltException(
                "failure fetching server public key",
                f"Return status code: {r.status_code}"
                )
        resp = r.json()
        if resp["header"]["status"] != "success":
            raise BoltException("failure fetching server public key", resp["header"]["message"])
        keydata = resp["body"]["keydata"]
        serverkey = pgpy.PGPKey()
        serverkey.parse(keydata)
        return serverkey

    def _generate_nonce(self):
        nonce=str(uuid.uuid4())
        token=f"gpgauthv1.3.0|36|{nonce}|gpgauthv1.3.0"
        return token

    def send_user_fingerprint(self, enc_token):
        "Send fingerprint to passbolt server"
        payload = {
            "data": {
                "gpg_auth": {
                    "keyid": str(self.privkey.fingerprint),
                    "server_verify_token": enc_token
                    }
                }
            }
        r = requests.post(f'{self.base_url}/auth/verify.json?api-version=v2', json=payload)
        if 'X-GPGAuth-Verify-Response' in r.headers:
            if r.headers['X-GPGAuth-Verify-Response']:
                return r.headers['X-GPGAuth-Verify-Response']
        return None

    def verify(self):
        "verifies server identity"
        plain_token = self._generate_nonce()
        server_pubkey = self.get_server_pubkey()

        msg = pgpy.PGPMessage.new(plain_token)
        enc_token = str(server_pubkey.encrypt(msg))
        token_back = self.send_user_fingerprint(enc_token)
        if token_back != plain_token:
            raise BoltException("token verification error")

    def login(self):
        "logs in to server, setting session cookie"
        payload = { "data": {"gpg_auth": { 'keyid': str(self.privkey.fingerprint) } } }
        r = requests.post(f'{self.base_url}/auth/login.json?api-version=v2', json=payload)
        if r.status_code != 200:
            raise BoltException(
                "failure logging in",
                f"Return status code: {r.status_code} in step 1"
                )
        if 'X-GPGAuth-User-Auth-Token' not in r.headers:
            raise BoltException(
                "failure logging in",
                "Missing X-GPGAuth-User-Auth-Token header"
                )
        tok = urllib.parse.unquote_plus(r.headers['X-GPGAuth-User-Auth-Token']).replace(r"\ ", " ")
        msg = pgpy.PGPMessage.from_blob(tok)
        with self.privkey.unlock(self.passphrase) as lockpick:
            token = lockpick.decrypt(msg).message.decode('ascii')
        payload = {
            "data": {
                "gpg_auth": {
                    "keyid": str(self.privkey.fingerprint),
                    "user_token_result": token
                    }
                }
            }
        r = requests.post(f'{self.base_url}/auth/login.json?api-version=v2', json=payload)
        if r.status_code != 200:
            raise BoltException(
                "failure logging in",
                f"Return status code: {r.status_code} in step 2"
                )
        resp = r.json()
        if resp["header"]["status"] != "success":
            raise BoltException("failure fetching server public key", resp["header"]["message"])
        self.session_cookies = r.cookies

    def get_secret(self, xid):
        "get secret (password + description) from server"
        if self.session_cookies is None:
            raise BoltException("failure fetching server public key", "not logged in")

        r = requests.get(
            f'{self.base_url}/secrets/resource/{xid}.json',
            cookies = self.session_cookies
            )
        if r.status_code != 200:
            raise BoltException("failure fetching secrets", f"Return status code: {r.status_code}")
        resp = r.json()
        if resp["header"]["status"] != "success":
            raise BoltException("failure fetching secrets", resp["header"]["message"])
        msg = pgpy.PGPMessage.from_blob(resp["body"]["data"])
        with self.privkey.unlock(self.passphrase) as lockpick:
            data = lockpick.decrypt(msg).message
        secret = json.loads(data)
        return secret


