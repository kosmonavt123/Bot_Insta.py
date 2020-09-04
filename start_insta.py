from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from random import randint
import pandas as pd

# --------------
# In every Selenium script need to include the code below:

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


binary = FirefoxBinary("C:\\Program Files\\Mozilla Firefox\\firefox.exe")

driver = webdriver.Firefox(
    firefox_binary=binary, executable_path=r"C:\\geckodriver.exe"
)

# --------------

browser = driver  # !!!

browser.implicitly_wait(5)  # set up 5 sec delay
# If Selenium cannot find the element, it waits for everything to load
# and tries again.

browser.get("https://www.instagram.com/")
sleep(3)


username = browser.find_element_by_name("username")
username.send_keys("username")  # Change this to your own Instagram username
password = browser.find_element_by_name("password")
password.send_keys("password")  # Change this to your own Instagram password

login_button = browser.find_element_by_xpath("//button[@type='submit']")
login_button.click()
sleep(3)

notnow = browser.find_element_by_css_selector("button.aOOlW.HoLwm")
notnow.click()  # Comment these last 2 lines out, if you don't get a pop up asking about notifications

hashtag_list = [
    "trip",
    "photography",
    "traveling",
    "tech",
    "riga",
    "latvia",
    "yoga",
    "sport",
    "running",
]  # Change this to your own tags

prev_user_list = (
    []
)  # If it's the first time you run it, use this line and comment the two below
# prev_user_list = pd.read_csv('20190604-224633_users_followed_list.csv', delimiter=',').iloc[:,1:2] # useful to build a user log
# prev_user_list = list(prev_user_list['0'])

new_followed = []
tag = -1
followed = 0
likes = 0
comments = 0

for hashtag in hashtag_list:
    tag += 1
    browser.get("https://www.instagram.com/explore/tags/" + hashtag_list[tag] + "/")
    sleep(5)
    first_thumbnail = browser.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/article/div/div/div/div[1]/div[1]/a/div'
    )

    first_thumbnail.click()
    sleep(randint(1, 2))
    try:
        for x in range(1, 200):

            # Every time needed refreshing username
            username = browser.find_element_by_class_name(
                "sqdOP yWX7d     _8A5w5   ZIAjV"
            )
            username.get_attribute("href")

            if username not in prev_user_list:

                # If we already follow, do not unfollow
                if (
                    browser.find_element_by_xpath(
                        "/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[2]/button"
                    ).text
                    == "Follow"
                ):

                    browser.find_element_by_xpath(
                        "/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[2]/button"
                    ).click()
                    new_followed.append(username)
                    followed += 1

                    # Liking the picture
                    button_like = browser.find_element_by_xpath(
                        "/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button"
                    )
                    button_like.click()
                    likes += 1
                    sleep(randint(17, 27))

                    # Comments and tracker
                    comm_prob = randint(1, 13)
                    print("{}_{}: {}".format(hashtag, x, comm_prob))
                    if comm_prob > 7:
                        comments += 1
                        browser.find_element_by_xpath(
                            "/html/body/div[3]/div[2]/div/article/div[2]/section[1]/span[2]/button/span"
                        ).click()
                        comment_box = browser.find_element_by_xpath(
                            "/html/body/div[3]/div[2]/div/article/div[2]/section[3]/div/form/textarea"
                        )

                        if comm_prob < 7:
                            comment_box.send_keys("Awesome!")
                            sleep(1)
                        elif (comm_prob > 6) and (comm_prob < 9):
                            comment_box.send_keys("Good very good;)")
                            sleep(1)
                        elif comm_prob == 9:
                            comment_box.send_keys("prety nice")
                            sleep(1)
                        elif comm_prob == 10:
                            comment_box.send_keys("Whaat:)")
                            sleep(1)
                        # Enter to post comment
                        comment_box.send_keys(Keys.ENTER)
                        sleep(randint(21, 29))

                # Next picture
                browser.find_element_by_link_text("Next").click()
                sleep(randint(24, 30))
            else:
                browser.find_element_by_link_text("Next").click()
                sleep(randint(21, 26))
    # Some hashtag stops refreshing photos (it may happen sometimes), it continues to the next
    except:
        continue

for n in range(0, len(new_followed)):
    prev_user_list.append(new_followed[n])

updated_user_df = pd.DataFrame(prev_user_list)
updated_user_df.to_csv("{}_users_followed_list.csv".format(strftime("%Y%m%d-%H%M%S")))
print("Liked {} photos.".format(likes))
print("Commented {} photos.".format(comments))
print("Followed {} new people.".format(followed))
