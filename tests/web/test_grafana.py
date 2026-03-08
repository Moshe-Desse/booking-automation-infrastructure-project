import allure
import pytest

from data.web.grafana_data import *
from extensions.web_verifications import WebVerify
from workflows.web.grafana_web_flows import  GrafanaWebFlows



class TestGrafana:

    def test01_verify_login_negative(self,grafana_web_flows:GrafanaWebFlows):
        grafana_web_flows.fill_login_fields(WRONG_USER_NAME,WRONG_PASSWORD)
        grafana_web_flows.click_on_login_button()
        WebVerify.text(grafana_web_flows.login.failed_login_message,FAILAD_LOGIN_MESSAGE)

    def test02_verify_login_possitive(self,grafana_web_flows:GrafanaWebFlows):
        grafana_web_flows.fill_login_fields(USER_NAME,PASSWORD)
        grafana_web_flows.click_on_login_button()
        grafana_web_flows.click_on_skip_button()
        WebVerify.text(grafana_web_flows.home.header,EXPECTED_HEADER)

    def test03_create_dashboard(self,grafana_web_flows:GrafanaWebFlows):
        grafana_web_flows.creat_new_dashboard()



        