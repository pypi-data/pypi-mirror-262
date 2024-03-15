import requests

from gupshup.exceptions import UnauthorizedError, WrongFormatInputError


class Client(object):
    BASE_URL_MESSAGE = "http://api.gupshup.io/sm/api/v1/template/msg"
    BASE_URL_TEMPLATES = "https://api.gupshup.io/sm/api/v1/template/list/"
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "*/*"}

    def __init__(self, apikey=None, app_name=None):
        self.APIKEY = apikey
        self.APP_NAME = app_name

        self.headers["apikey"] = self.APIKEY

    def get_templates_app(self, **kwargs):
        return self.parse(requests.request(
            "GET", self.BASE_URL_TEMPLATES + self.APP_NAME, headers=self.headers, **kwargs
        ))

    def get_variables_for_template(self):
        templates = self.get_templates_app()
        list_templates_with_variables = []
        try:
            for template in templates['templates']:
                data_vars = []
                header_vars = []
                footer_vars = []
                for key, value in template.items():
                    if key == "data" or key == "header" or key == "footer":
                        for i in range(1, 10):
                            var = "{{" + str(i) + "}}"
                            if var in value:
                                if key == "data":
                                    data_vars.append(i)
                                elif key == "header":
                                    header_vars.append(i)
                                elif key == "footer":
                                    footer_vars.append(i)

                variables = {
                    "data_vars": data_vars,
                    "header_vars": header_vars,
                    "footer_vars": footer_vars,
                    "template_id": template['id']
                }
                list_templates_with_variables.append(variables)
            return list_templates_with_variables
        except:
            return []

    def send_templates_msg(self, data):
        return self.parse(requests.request(
            "POST", self.BASE_URL_MESSAGE, headers=self.headers, data=data
        ))

    def parse(self, response):
        status_code = response.status_code
        if "Content-Type" in response.headers and "application/json" in response.headers["Content-Type"]:
            try:
                r = response.json()
            except ValueError:
                r = response.text
        else:
            r = response.text
        if status_code == 200:
            return r
        if status_code == 204:
            return None
        if status_code == 400:
            raise WrongFormatInputError(r)
        if status_code == 401:
            raise UnauthorizedError(r)
        if status_code == 500:
            raise Exception
        return r
