from src.DZ2_AppForTest.sample_data.test_2_testdata import requirements_data, test_cases_data, test_run_data, \
    test_result_data
from testteamreports.tests.Client import Client


class Tests(Client):
    @staticmethod
    def test_1():
        client = Client()
        client.create_user('so', 'so')
        assert client.login('so', 'so') == 200
        client.users_list()

    @staticmethod
    def test_2():
        Tests.requirements()
        Tests.testcases()
        Tests.testruns()
        Tests.testresult()
        Tests.report()

    @staticmethod
    def requirements():
        client = Client()
        client.create_user('kate', 'kate')
        client.login('kate', 'kate')
        assert client.login('kate', 'kate') == 200
        for i in requirements_data:
            client.add_requirement(i['name'], i['risk'])

        client.requirements_list()

    @staticmethod
    def testcases():
        client = Client()
        client.login('kate', 'kate')
        assert client.login('kate', 'kate') == 200
        for i in test_cases_data:
            client.add_test_case(i['name'], i['requirements'])
        client.test_cases()

    @staticmethod
    def testruns():
        client = Client()
        client.login('kate', 'kate')
        assert client.login('kate', 'kate') == 200
        client.add_test_run(test_run_data['start_date'], test_run_data['end_date'],
                            test_run_data['description'], test_run_data['test_cases'])
        client.test_runs()

    @staticmethod
    def testresult():
        client = Client()
        client.login('kate', 'kate')
        assert client.login('kate', 'kate') == 200
        test_runs_list = client.test_runs()
        for i in test_runs_list:
            for j in test_result_data:
                client.add_result(test_run_id=i.id, name=j['name'], is_passed=j['is_passed'], date_time=j['date_time'])

    @staticmethod
    def report():
        client = Client()
        client.login('kate', 'kate')
        assert client.login('kate', 'kate') == 200
        client.get_report(test_run_id=1)
        client.compare_reports()

Tests.test_2()