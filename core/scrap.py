from playwright.async_api import async_playwright

class ProfileInfo:
    def __init__(self, username, password, date):
        self.username = username
        self.password = password

        self.date = date
        self.day = self.date.split('-')[0].lstrip('0')  # Eliminăm 0-ul de început
        self.month = self.date.split('-')[1]
        self.year = self.date.split('-')[2]

        self.tokens = {}
        self.times = {}

    async def get_information(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()

            # Login
            await page.goto("https://www.myfreecams.com/model_admin")
            await page.fill('#username', self.username)
            await page.fill('#password', self.password)
            await page.click('input[value="Continue"]')

            # Navighează la pagina cu iframe
            await page.goto("https://profiles.myfreecams.com/_/ext/token_sessions")
            iframe_element = await page.wait_for_selector('iframe#content_iframe')
            frame = await iframe_element.content_frame()

            # Selectează ziua curentă în select[name="period"]
            await frame.select_option('select[name="period"]', value=self.day)

            # Preia conținutul vechi al tabelului pentru comparație
            old_table = await frame.query_selector('form table:nth-of-type(2)')
            old_html = await old_table.inner_html()

            # Dă click pe butonul submit
            await frame.click('form tbody tr:nth-of-type(5) td:nth-of-type(2) input[type="submit"]')

            # Așteaptă să se schimbe conținutul tabelului (să fie diferit de cel vechi)
            await frame.wait_for_function(
                """(oldHTML) => {
                    const newTable = document.querySelector('form table:nth-of-type(2)');
                    return newTable && newTable.innerHTML !== oldHTML;
                }""",
                arg=old_html,
                timeout=15000
            )

            # Acum extrage noile informații
            second_table = await frame.query_selector('form table:nth-of-type(2)')
            rows = await second_table.query_selector_all('tr')

            count = 0
            for row in rows:
                cols = await row.query_selector_all('td')
                if len(cols) == 2:
                    key = (await cols[0].inner_text()).strip().rstrip(':')
                    value = (await cols[1].inner_text()).strip()

                    if count < 9:
                        self.tokens[key] = value
                    else:
                        self.times[key] = value
                    count += 1
