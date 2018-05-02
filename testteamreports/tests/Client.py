import os
import subprocess
import requests

from testteamreports.tests.API import Auth, CreateUser, CloseSession, UserList, RecreateDb, RequirementsList, \
    AddRequirement, TestCases, AddTestCase, AddTestRun, TestRuns, Result, Report
from testteamreports.tests.Global import Server_host, utility_path
from testteamreports.tests.Shared import get_obj_from_json


class Client:
    def __init__(self):
        self.__session = requests.Session()
        self.__session.verify = False
        self.host = Server_host

    def is_connected(self):
        if self.__session.cookies.get('authorization') is not None:
            return True

    def login(self, login, password):
        request = self.__session.post(Server_host + Auth.API, json=Auth.auth_params(login, password))
        return request.status_code

    def create_user(self, login, password):
        if self.is_connected():
            self.logout()
        self.login('admin', 'admin')
        request = self.__session.post(url=Server_host + CreateUser.API, json=CreateUser.auth_params(login, password))
        self.logout()
        response = get_obj_from_json(request, CreateUser)
        return response

    def logout(self):
        request = self.__session.post(url=Server_host + CloseSession.API, json=None)
        return request.status_code

    def users_list(self):
        if self.is_connected():
            self.logout()
        self.login('admin', 'admin')
        request = self.__session.get(url=Server_host + UserList.API)
        return request.status_code

    def recreate_db(self):
        if self.is_connected():
            self.logout()
        self.login('admin', 'admin')
        request = self.__session.post(url=Server_host + RecreateDb.API)
        return request.status_code

    def requirements_list(self):
        request = self.__session.get(url=Server_host + RequirementsList.API)
        response = get_obj_from_json(request, RequirementsList)
        return response

    def add_requirement(self, name: str, risk: int):
        request = self.__session.post(url=Server_host + AddRequirement.API, json=AddRequirement.auth_params(name, risk))
        response = get_obj_from_json(request, AddRequirement)
        return response

    def test_cases(self):
        request = self.__session.get(url=Server_host + TestCases.API)
        response = get_obj_from_json(request, TestCases)
        return response

    def add_test_case(self, name, requirements):
        request = self.__session.post(url=Server_host + AddTestCase.API, json=AddTestCase.auth_params(name, requirements))
        response = get_obj_from_json(request, AddTestCase)
        return response

    def add_test_run(self, start_date, end_date, description, test_cases_names):
        # format_start_date = build_timestamp(start_date)
        # format_end_date = build_timestamp(end_date)
        request = self.__session.post(url=Server_host + AddTestRun.API,
                                      json=AddTestRun.auth_params(start_date, end_date, description,
                                                                   test_cases_names))
        response = get_obj_from_json(request, AddTestRun)
        return response

    def test_runs(self):
        request = self.__session.get(url=Server_host + TestRuns.API)
        response = get_obj_from_json(request, TestRuns)
        return response

    def add_result(self, test_run_id, name, is_passed, date_time):
        # format_datetime = build_timestamp(date_time)
        request = self.__session.post(url=Server_host + AddTestRun.API + "/" + str(test_run_id) + '/' + Result.API,
                                      json=Result.auth_params(name, is_passed, date_time))
        response = request.status_code
        return response

    def get_report(self, test_run_id):
        request = self.__session.get(url=Server_host + AddTestRun.API + "/" + str(test_run_id) + '/' + Report.API)
        with open('Report\\report_fact.pdf', 'wb') as fh:
            fh.write(request.content)
        return request.status_code

    @staticmethod
    def compare_reports():
        path = os.path.abspath('Report')
        expected_report_pdf = path + '\\report_expected.pdf'
        expected_report_png = path + '\\report_expected.png'
        fact_report_pdf = path + '\\report_fact.pdf'
        fact_report_png = path + '\\report_fact.png'
        diff = path + '\\diff.png'

        subprocess.run(f'{utility_path} -density 300 {fact_report_pdf} {fact_report_png}')
        subprocess.run(f'{utility_path} -density 300 {expected_report_pdf} {expected_report_png}')
        subprocess.run(f'{utility_path} compare -metric ae {expected_report_png} {fact_report_png} {diff}')