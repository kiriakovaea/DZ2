class Auth:
    API = 'login'

    @staticmethod
    def auth_params(login, password):
        auth_data = {
            'login': login,
            'password': password
        }
        return auth_data


class CloseSession:
    API = 'logout'


class UserList:
    API = 'admin/users'


class CreateUser:
    def __init__(self, id):
        self.id = id

    API = 'admin/user'

    @staticmethod
    def auth_params(new_login, new_password):
        auth_data = {
            'new_login': new_login,
            'new_password': new_password
        }
        return auth_data

    @classmethod
    def from_json(cls, json):
        if json is None:
            return None
        return cls(id=json['id'])


class RecreateDb:
    API = 'admin/recreatedb'


class RequirementsList:
    def __init__(self, id=None, name=None, risk=None):
        self.risk = risk
        self.name = name
        self.id = id

    API = 'reqs'

    @classmethod
    def from_json(cls, json):
        if json is None:
            return None
        res_list = []
        for elem in json:
            obj = cls(id=elem['id'],
                      name=elem['name'],
                      risk=elem['risk'])
            res_list.append(obj)
        return res_list

    @classmethod
    def from_json_name(cls, json):
        if json is None:
            return None
        res_list = []
        for elem in json:
            obj = cls(id=None,
                      name=elem,
                      risk=None)
            res_list.append(obj)
        return res_list


class AddRequirement:
    def __init__(self, id):
        self.id = id

    API = 'req'

    @classmethod
    def from_json(cls, json):
        if json is None:
            return None
        return cls(id=json['id'])

    @staticmethod
    def auth_params(name: str, risk: int):
        auth_data = {
            'name': name,
            'risk': risk
        }
        return auth_data


class AddTestCase:
    def __init__(self, id):
        self.id = id

    API = 'testcase'

    @staticmethod
    def auth_params(name: str, requirements: list):
        auth_data = {
            'name': name,
            'requirements': requirements
        }
        return auth_data

    @classmethod
    def from_json(cls, json):
        if json is None:
            return None
        return cls(id=json['id'])


class TestCases:
    def __init__(self, id=None, name=None, requirement=None):
        self.name = name
        self.id = id
        self.requirement = requirement

    API = 'testcases'

    @classmethod
    def from_json(cls, json):
        if json is None:
            return None
        res_list = []
        for elem in json:
            obj = cls(id=elem['id'],
                      name=elem['name'],
                      requirement=RequirementsList.from_json_name(elem['requirements']))
            res_list.append(obj)
        return res_list


class AddTestRun:
    def __init__(self, id):
        self.id = id

    API = 'testrun'

    @classmethod
    def from_json(cls, json):
        if json is None:
            return None
        return cls(id=json['id'])

    @staticmethod
    def auth_params(start_date, end_date, description, name):
        auth_data = {
            'start_date': start_date,
            'end_date': end_date,
            'description': description,
            'test_cases': name
        }
        return auth_data


class TestRuns:
    def __init__(self, id, start_date, end_date, description, test_cases):
        self.id = id
        self.test_cases = test_cases
        self.description = description
        self.end_date = end_date
        self.start_date = start_date

    API = 'testruns'

    @classmethod
    def from_json(cls, json):
        if json is None:
            return None
        res_list = []
        for elem in json:
            obj = cls(start_date=elem['start_date'],
                      end_date=elem['end_date'],
                      description=elem['description'],
                      # test_cases=TestCases.from_json(elem['test_cases']))
                      test_cases=elem['test_cases'],
                      id=elem['id'])
            res_list.append(obj)
        return res_list


class Result:
    API = 'result'

    @staticmethod
    def auth_params(name: str, is_passed: bool, date_time: str):
        auth_data = {
            'name': name,
            'is_passed': is_passed,
            'date_time': date_time
        }
        return auth_data


class Report:
    API = 'pdf'
