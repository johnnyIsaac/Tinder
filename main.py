import os, random, time, undetected_chromedriver, pyautogui, requests

# Selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from fake_useragent import UserAgent


from keras.models import load_model
from keras.utils import load_img, img_to_array
import numpy
#from attractive_net.AttractiveNet.test import get_beauty_score

# Custom
from data.config import *

headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json',
    'Server': 'istio-envoy',
    'Accept-encoding': 'gzip, deflate, br',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.43',
    'Content-Type': 'application/json',
    'Origin': 'https://russiannlp.github.io',
    'Referer': 'https://russiannlp.github.io/',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Accept-Language': 'en-US,en;q=0.9,es-AR;q=0.8,es;q=0.7',
}


class TinderBot:
    def __init__(self):
        browser = self.__open_chrome()
        browser = self.__change_user_agent(browser)
        browser.get("https://tinder.com/ru")
        browser.maximize_window()
        self.__log_in_check(browser)
        xpath = '//*[@id="s-1602360476"]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a'
        print('Starting...')
        try:
            #self.__click(browser, xpath)
            #self.__google_login(browser)
            while True:
                self.__popup_accept(browser)
                action = random.randint(1, 3)
                if(action == 1):
                    browser.get("https://tinder.com/ru")
                    yes_no = random.randint(0, 1)
                    if yes_no == 1:
                        self.__click_image(browser, 'like.png')
                    else:
                        self.__click_image(browser, 'dislike.png')
                if(action == 2):
                    self.__collect_chats(browser)
                if (action == 3):
                    browser.get("https://tinder.com/ru")
                    self.__get_mathces(browser)
            #self.__evaluate_appearance(browser)


        except:
            print('Error')
            self.__finish(browser)

    def __change_user_agent(self, browser):
        ua = UserAgent()
        options = undetected_chromedriver.ChromeOptions()
        userAgent = ua.random
        options.add_argument(f'user-agent={userAgent}')
        return browser

    def __open_chrome(self):
        options = undetected_chromedriver.ChromeOptions()
        profile = f"C:/Users/{os.getlogin()}/AppData/Local/Google/Chrome/User Data/Profile 1"
        options.add_argument(f'user-data-dir={profile}')
        browser = undetected_chromedriver.Chrome(options=options)
        browser.implicitly_wait(60)
        browser.set_window_size(1920, 1080)
        return browser

    def __log_in_check(self, browser):
        time.sleep(0.5)
        site = browser.current_url
        if site == 'https://tinder.com/':
            self.__google_login(browser, EMAIl, PASSWORD)
            print('login')
        else:
            print('Already logged in')

    def __click(self, browser, xpath):
        if(WebDriverWait(browser, DELAY).until(EC.presence_of_element_located((By.XPATH, xpath)))):
            find_button = browser.find_element(By.XPATH, xpath)
            self.__emulate_human_response()
            find_button.click()
            print('Button found and clicked')
        else:
            print('Button not found')
        return browser

    def __click_image(self, browser, image_path):
        image_path = 'assets/images/' + image_path
        self.__emulate_human_response()
        pyautogui.moveTo(pyautogui.click(pyautogui.locateCenterOnScreen(image_path, confidence=0.9)),duration=5)
        return browser

    def __accept_all(self, browser):
        self.__click_image(browser, 'allow_search.jpg')
        self.__click_image(browser, 'accept_conditions.jpg')
        self.__click_image(browser, 'turn_on_messages.jpg')
        self.__click_image(browser, 'block_notif.jpg')
        self.__click_image(browser, 'close_dark_theme.jpg')
        return browser
    def __popup_accept(self, browser):
        self.__click_image(browser, "hurt.jpg")
        self.__click_image(browser, "accept_hurt.jpg")
        self.__click_image(browser, "no_thanks.jpg")
        return browser
    def __emulate_human_response(self):
        time.sleep(random.randint(MIN_DELAY, MAX_DELAY))

    def __load_image(self, img_path, show=False):
        img = load_img(img_path, target_size=(300, 300))
        # (height, width, channels)
        img_tensor = img_to_array(img)
        # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
        img_tensor = numpy.expand_dims(img_tensor, axis=0)
        return img_tensor

    def __get_beauty_score(self, img_path):
        model_path = "attractive_net/AttractiveNet/models/attractiveNet_mnv2.h5"
        print(model_path)
        model = load_model(model_path)
        # load a single image
        new_image = self.__load_image(img_path)
        # check prediction
        pred = model.predict(new_image)
        return str(round(pred[0][0], 1))

    def __get_score(self, browser):
        IMGCOUNTER = 0
        score = self.__get_beauty_score(self.__download_images(browser, IMGCOUNTER))
        return score, browser

    def __download_images(self, browser, IMGCOUNTER):
        print('Finding Images...')
        img_class = "Bdrs(8px) Bgz(cv) Bgp(c) StretchedBox"
        WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, f'//div[@class="{img_class}"]')))
        image = browser.find_element(By.XPATH, f'//div[@class="{img_class}"]')
        img_data = requests.get(image.value_of_css_property("background-image")[5:-2]).content
        person_face_name = 'temp/person_avatars/' + f'person_face{IMGCOUNTER}.jpg'
        with open(person_face_name, 'wb') as handler:
            handler.write(img_data)
        IMGCOUNTER += 1
        print(IMGCOUNTER)
        return person_face_name

    def __google_login(self, browser, email, password):
        print('Starting Google Login...')
        content = '/html/body/div[1]'
        xpath = f'{content}/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a'
        self.__emulate_human_response()
        self.__click(browser, xpath)
        browser = self.__change_user_agent(browser)
        xpath = '//*[@aria-label="Войти через Google"]'
        self.__emulate_human_response()
        self.__click(browser, xpath)
        browser = self.__change_user_agent(browser)
        browser.switch_to.window(browser.window_handles[1])
        xpath = "//input[@type='email']"
        WebDriverWait(browser, DELAY).until(EC.presence_of_element_located((By.XPATH, xpath)))
        self.__emulate_human_response()
        emailfield = browser.find_element(By.XPATH, xpath)
        emailfield.send_keys(email)
        self.__emulate_human_response()
        emailfield.send_keys(Keys.ENTER)
        self.__emulate_human_response()
        xpath = "//input[@type='password']"
        WebDriverWait(browser, DELAY).until(EC.presence_of_element_located((By.XPATH, xpath)))
        browser = self.__change_user_agent(browser)
        self.__emulate_human_response()
        password_field = browser.find_element(By.XPATH, xpath)
        password_field.send_keys(password)
        self.__emulate_human_response()
        password_field.send_keys(Keys.ENTER)
        browser.switch_to.window(browser.window_handles[0])
        self.__accept_all(browser)
        return browser
    def __evaluate_appearance(self, browser):
        print('Starting evaluate appearance of person...')
        score = self.__get_score(browser)
        print(score)
        if float(score) >= 2.8:
            self.__click_image(browser, 'like.png')
        else:
            self.__click_image(browser, 'dislike.png')

    # def __do_likes(self, browser):
    #     self.__emulate_human_response()
    #     xpath = '//button//span/[text()="Лайк"]'
    #     self.__click(browser, xpath)
    #     print('Like button clicked')
    #     return browser

    # def __do_dislike(self, browser):
    #     self.__emulate_human_response()
    #     xpath = '//button//span/[text()="Нет"]'
    #     self.__click(browser, xpath)
    #     print('Dislike button clicked')
    #     return browser

    def __send_message(self, browser, message):
        self.__emulate_human_response()
        input_field = browser.find_element(By.XPATH, "//textarea")
        input_field.send_keys(message)
        browser.find_element(By.XPATH, "//button[@type='submit']").click()
        self.__emulate_human_response()
        return browser
    def __get_mathces(self, browser):
        print('Getting matches...')
        try:
            self.__emulate_human_response()
            match_profiles = browser.find_elements('class name', 'matchListItem')
            links = []
            for profile in match_profiles:
                if profile.get_attribute('href') == 'https://tinder.com/app/recs/likes-you':
                    continue
                else:
                    links.append(profile.get_attribute('href'))
            print('Matches', len(links))
            for link in links:
                browser.get(link)
                self.__emulate_human_response()
                self.__send_message(browser, 'Привет, как дела?')
            self.__emulate_human_response()
        except:
            print('No matches')
        return browser

    def __answer_questions(self, question):
        question = "Девушка:" + question + "\nПарень:"
        response = requests.post("https://api.aicloud.sbercloud.ru/public/v1/public_inference/gpt3/predict",json={"text": question}, headers=headers)
        answer = ""
        if response.status_code == 200:
            try:
                answer = response.json()['predictions'].split('\n')
                new_answer = answer[1]
                new_answer = new_answer.split(':')[1]
                return new_answer
            except:
                print("упс")
        return answer


    def __collect_chats(self, browser):
        try:
            self.__emulate_human_response()
            WebDriverWait(browser, DELAY).until(EC.presence_of_element_located((By.XPATH, '//div[@class="messageList"]/a')))
            self.__emulate_human_response()
            chats = browser.find_elements(By.XPATH, '//div[@class="messageList"]/a')
            links = []
            for chat in chats:
                links.append(chat.get_attribute('href'))
            self.__emulate_human_response()
            self.__join_chat(browser, links)
        except:
            print('Chats empty')
        return browser

    def __join_chat(self, browser, links):
        for link in links:
            browser.get(link)
            self.__emulate_human_response()
            receive_message = browser.find_elements(By.XPATH, '//div[@role="log"]/div/button')
            if receive_message:
                message = receive_message[-1].find_element(By.XPATH, '../div/div/span').text
                try:
                    with open(f"{link.split('/')[-1]}.txt", "r+") as f:
                        text = f.read()
                        if text.split(" ")[-2] != message:
                            f.write(message + " ")
                            print("Didn't receive new messages:")
                            print(message)
                            answer = self.__answer_questions(message)
                            print(answer)
                            self.__send_message(browser, answer)
                        else:
                            print("No new messages")
                except:
                    with open(f"{link.split('/')[-1]}.txt", "w+") as f:
                        f.write(message + " ")
                        print("Receive new messages")
                        print(message)
                        answer = self.__answer_questions(message)
                        print(answer)
                        self.__send_message(browser, answer)
        return browser
    def __finish(self, browser):
        browser.quit()
        browser.close()


def main():
    start = TinderBot()
if __name__ == '__main__':
    main()