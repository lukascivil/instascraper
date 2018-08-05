from selenium import webdriver
import time

# login
def login(username, password):
	input_username = chrome.find_element_by_xpath('//input[@name="username"]')
	input_password = chrome.find_element_by_xpath('//input[@name="password"]')
	input_username.clear()
	input_password.clear()
	input_username.send_keys(username)
	input_password.send_keys(password)
	button_login = chrome.find_element_by_xpath('//button["Log in"]')
	button_login.click()
	time.sleep(2)


def getAllMyimagelinks(username):

	imglinks = []

	# 1 - GO TO PERFIL PAGE
	chrome.get('https://www.instagram.com/' + username)

	# 2 - SCROLL DOWN

	# Time to load infinite scroll
	SCROLL_PAUSE_TIME = 2

	# Get scroll height
	last_height = chrome.execute_script("return document.body.scrollHeight")

	while True:

		#  GET ALL IMAGE LINKS
		obg_imglinks = chrome.find_elements_by_xpath("//a[@href]")
		for obg_imglink in obg_imglinks:
			print(obg_imglink.get_attribute("href"))
			if "https://www.instagram.com/p/" in obg_imglink.get_attribute("href"):
				if obg_imglink.get_attribute("href") not in imglinks:
					imglinks.append(obg_imglink.get_attribute("href"))

	    # Scroll down to bottom
		chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		# Wait to load page
		time.sleep(SCROLL_PAUSE_TIME)

		# Calculate new scroll height and compare with last scroll height
		new_height = chrome.execute_script("return document.body.scrollHeight")
		if new_height == last_height:
			break
		last_height = new_height

	return imglinks


def getAllMylikes(imglinks):
	imgqueeuquero = ""
	vector_likes = []

	print(len(imglinks))
	for imglink in imglinks:
			
			newword = imglink.replace("https://www.instagram.com/p/", "")
			newword = newword.split('/')[0]

			chrome.get(imglink)
			time.sleep(0.5)
			try:
				imgqueeuquero = chrome.find_element_by_xpath("//img[@srcset]")

				isimg = True
				obg_likes = chrome.find_element_by_xpath("//a[@href='" + "/p/" + newword + "/liked_by/" +"']")
				
				print(obg_likes.text)
				
			except Exception as e:
				isimg = False

			if isimg:
				likevalue = obg_likes.text.split(' ')[0]
				vector_likes.append(int(likevalue))

	return vector_likes
	

def getAllMyfollowers(username):

	# 1 - GO TO PERFIL PAGE
	chrome.get('https://www.instagram.com/' + username)

	button_followers = chrome.find_element_by_xpath("//a[@href='" + "/" + username + "/followers/" +"']")
	button_followers.click()
	time.sleep(1)


username = ''
password = ''

# 1
options = webdriver.ChromeOptions()
options.add_argument('headless')
# chrome = webdriver.Chrome('chromedriver.exe')
chrome = webdriver.Chrome('chromedriver.exe', chrome_options=options)
chrome.get('https://www.instagram.com/accounts/login/')
time.sleep(2)

# 2
login(username, password)

# 3
imglinks = getAllMyimagelinks(username)

# 4
likes = getAllMylikes(imglinks)
print(sum(likes))

# 5
chrome.quit()