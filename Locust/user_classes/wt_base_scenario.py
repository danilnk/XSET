from locust import task, SequentialTaskSet,FastHttpUser, HttpUser, constant_pacing, events
from config.config import cfg, logger
from utils.assertion import check_http_response
import sys


class PurchaseFlightTicket(SequentialTaskSet): # класс с задачами (содержит основной сценарий)
    @task
    def uc00_getHomePage(self) -> None:

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
        ) as req00_3_response:\
            check_http_response(req00_3_response, 'name="userSession"')

        self.client.get(
            '/WebTours/home.html',
            name="reg_00_4_/WebTours/home.html",
            allow_redirects=False,
            #debug_stream=sys.stderr
        )




class WebToursBaseUserClass(FastHttpUser): # юзер-класс, принимающий в себя основные параметры теста
    wait_time = constant_pacing(cfg.pacing)

    host = cfg.url

    logger.info(f'WebToursBaseUserClass started. Host: {host}')

    tasks = [PurchaseFlightTicket]