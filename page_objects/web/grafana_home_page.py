from playwright.sync_api import Page

class GrafanaHomePage:

    def __init__(self,page:Page):
        self.page = page
        self.header = page.locator("[class='css-uantyg']") #Grafana < כותרת של האתר
        self.deshboards_button = page.locator("(//*[contains(@class,'css-1vx4yny')]/button)[3]") # כפתור הדשבורד
        self.deshboards_options = page.locator("[class='css-1fkiuh3']") 
        self.dashboard_viewer = page.locator("//*[@class='css-1vhkca4']/a")
        self.plus_button = page.locator("//*[@id='floating-boundary']/header/div[1]/div[2]/button[1]")
        self.new_dashboard_button = page.locator("//*[@id='grafana-portal-container']//div//div/div/a[1]")
        self.add_visualization_button = page.locator("[data-testid^='data-testid Cr']")
        self.source_test_data = page.locator("//*[@id='grafana-portal-container']/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[1]//h2/button")
        self.save_dashboard_button = page.locator("[data-testid^='data-testid Sa']")
        self.title_field = page.locator("[data-testid^='data-testid Panel editor o']")
        self.home_button = page.locator("[data-testid^='data-testid H']")
        self.data_source_field = page.locator("//*[@id='grafana-portal-container']/div[2]/div[2]/div[2]/div[1]/div[1]/div/input")



