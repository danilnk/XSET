from locust import task, SequentialTaskSet,FastHttpUser, HttpUser, constant_pacing, constant_throughput, events
from config.config import cfg, logger
from utils.assertion import check_http_response
from utils.non_test_methods import open_csv_file
import sys, re, random


class PurchaseFlightTicket(SequentialTaskSet): # класс с задачами (содержит основной сценарий)

    test_users_csv_filepath = './test_data/customers.csv'

    def on_start(self):

        @task
        def uc00_getHomePage(self) -> None:

            self.test_users_data = open_csv_file(self.test_users_csv_filepath)
            logger.info(f"Test data fot users is: {self.test_users_data}")

            r00_0_headers = {
                'sec-fetch-mode': 'navigate'
            }


            self.client.get(
                '/WebTours/',
                name="reg_00_0_/WebTours/",
                allow_redirects=False,
                #debug_stream=sys.stderr
            )

            self.client.get(
                '/WebTours/header.html',
                name="reg_00_1_/WebTours/header.html",
                allow_redirects=False,
                #debug_stream=sys.stderr
            )

            r_02_url_param_signOff = 'true'

            self.client.get(
                f'/cgi-bin/welcome.pl?signOff=true={r_02_url_param_signOff}',
                name="reg_00_2_/cgi-bin/nav.pl?in=home",
                allow_redirects=False,
                #debug_stream=sys.stderr
            )

            with self.client.get(
                    f'/cgi-bin/nav.pl?in=home',
                    name="reg_00_3_Home_page_/cgi-bin/nav.pl?in=home",
                    allow_redirects=False,
                    catch_response=True
                    #debug_stream=sys.stderr
            ) as req00_3_response: \
                    check_http_response(req00_3_response, 'name="userSession"')

            self.user_session = re.search(r"name=\"userSession\" value=\"(.*)\"\/>", req00_3_response.text).group(1)

            logger.info(f"USER_SESSION PARAMETER: {self.user_session}")

            self.client.get(
                '/WebTours/home.html',
                name="reg_00_4_/WebTours/home.html",
                allow_redirects=False,
                #debug_stream=sys.stderr
            )

        @task
        def uc01_LoginAction(self) -> None:
            r01_00_headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            self.user_data_row = random.choice(self.test_users_data)

            self.username = self.user_data_row["username"]
            self.password = self.user_data_row["password"]

            logger.info(f"chosen username: {self.username} / password: {self.password}")

            r01_00_body = f"userSession={self.user_session}&username={self.username}&password={self.password}&login.x=0&login.y=0&JSFormSubmit=off"

            with self.client.post(
                    '/cgi-bin/login.pl',
                    name='reg_01_0_LoginAction/cgi-bin/login.pl',
                    headers=r01_00_headers,
                    data=r01_00_body,
                    # debug_stream=sys.stderr,
                    catch_response=True
            ) as req01_0_response: \
                    check_http_response(req01_0_response,"User password was correct")

            self.client.get(
                '/cgi-bin/login.pl?intro=true',
                name="reg_01_1_LoginAction/cgi-bin/login.pl?intro=true",
                # debug_stream=sys.stderr,
                allow_redirects=False
            )

            self.client.get(
                '/cgi-bin/nav.pl?page=menu&in=home',
                name="reg_01_1_LoginAction/cgi-bin/nav.pl?page=menu&in=home",
                # debug_stream=sys.stderr,
                allow_redirects=False
            )

        uc00_getHomePage(self)
        uc01_LoginAction(self)

    @task
    def my_dummy_task(self):
        print('привет')




class WebToursBaseUserClass(FastHttpUser): # юзер-класс, принимающий в себя основные параметры теста
    wait_time = constant_pacing(cfg.pacing)

    host = cfg.url

    logger.info(f'WebToursBaseUserClass started. Host: {host}')

    tasks = [PurchaseFlightTicket]