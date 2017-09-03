import requests
import logging
import urllib3,urllib
import json

class SaltClient(object):
    def __init__(self, salt_host, salt_username, salt_password, **kwargs):
        self.token = None
        self.host = salt_host.rstrip('/')
        self.username = salt_username
        self.password = salt_password
        self.verify_ssl_cert = kwargs.get("verify_ssl_cert", False)


    def postRequest(self,data,prefix='/'):

        url = self.host + prefix
        headers = {'X-Auth-Token': self.get_token()}

        try:
            req = requests.post(url,data=data,headers=headers,verify=self.verify_ssl_cert, timeout=1000)
            if req.status_code != 200:
                raise AuthenticationException("Signing in to salt failed.")
        except Exception as e:
            print(e)

        resp = req.json()

        return resp



    def get_token(self):

        data = {"eauth": "pam", "username": self.username, "password": self.password}
        try:
            req = requests.post(self.host + "/login", data=data, headers={"Accept": "application/json"}, verify=self.verify_ssl_cert, timeout=5.0)
            # if req.status_code != 200:
            #     raise ConnectionException("Signing in to salt (%s) failed with status code %s (body %s)" % (self.host, req.status_code, req.text))
            # logging.debug("Salt login response: %s - %s", req.status_code, req.text)
            if req.status_code != 200:
                raise AuthenticationException("Signing in to salt failed.")
            resp = req.json()
            self.token = resp["return"][0]["token"]
        except  Exception  as e:
            print(e)
        return self.token


    # def postRequest(self,obj,prefix='/'):

    #     url = self.host + prefix

    #     token = self.get_token()
    #     print('---------------')
    #     headers = {'X-Auth-Token': token}
    #     req = urllib.request.Request(url, obj, headers)
    #     opener = urllib.request.urlopen(req)
    #     content = json.loads(opener.read())
    #     return content    



    def remote_server_info(self,server,fun):
        ''' Execute commands without parameters '''
        params = {"client": "local", "tgt": server, "fun": fun}
        ret = self.postRequest(params)
        data = ret['return'][0][server]
        return data



    # def _get_headers(self):
    #     return {"Accept": "application/json", "X-Auth-Token": self.token}

    # def is_minion_reachable(self, minion_id):
    #     req = requests.post(self.host, data={"client": "local", "tgt": minion_id, "fun": "test.ping"}, headers=self._get_headers(), verify=self.verify_ssl_cert)
    #     logging.debug("Salt ping response: %s - %s", req.status_code, req.text)
    #     resp = req.json()
    #     data = resp["return"][0]
    #     if len(data) == 0:  # returns [{}] if request fails
    #         return False
    #     if data.get(vm_id):  # eturns [{"node-name": True}] if ping succeeds
    #         return True
    #     return None

    # def run_async_command(self, target, command, args):
    #     resp = requests.post(self.salt_host, data={"client": "local_async", "tgt": target, "fun": command, "arg": args}, headers=self._get_headers(), verify=self.verify_ssl_cert)
    #     logging.debug("Salt cmd response: %s - %s", resp.status_code, resp.text)
    #     data = resp.json()
    #     return data["return"][0]["jid"]

    # def check_job_status(self, job_id):
    #     resp = requests.post(self.salt_host, data={"client": "runner", "fun": "jobs.lookup_jid", "jid": job_id}, headers=self._get_headers(), verify=self.verify_ssl_cert)
    #     logging.debug("lookup_jid response: %s - %s", resp.status_code, resp.text)
    #     data = resp.json()

    # def run_command(self, target, command, args):
    #     resp = requests.post(self.salt_host, data={"client": "local", "tgt": target, "fun": command, "arg": args}, headers=self._get_headers(), verify=self.verify_ssl_cert)
    #     logging.debug("Salt cmd response: %s - %s", resp.status_code, resp.text)
    #     data = resp.json()

    #     machines = data["return"][0]
    #     for machine, machine_data in machines.items():
    #         for _, command_data in machine_data.items():
    #             if not command_data["result"]:
    #                 return False
    #     return True