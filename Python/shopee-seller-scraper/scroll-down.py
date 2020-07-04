## Current directory and URL
url = 'https://shopee.co.id/search?keyword='
query = 'jas wisuda'
query_encode = requote_uri(query.strip('').lower())
url_query = url + query_encode
dir_path = os.getcwd()

## Wrangling HTML with BeautifulSoup
driver.get(url_query)
driver.implicitly_wait(20)

## Region filter
region_dropdown_button = driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[3]/div[1]/div[3]/div[2]/div[5]/div[1]/div')
driver.implicitly_wait(5)
region_dropdown_button.click()

## 
region_list = driver.find_element_by_class_name('col-xs-2-4 shopee-search-item-result__item')
soup = BeautifulSoup(driver.page_source,'html.parser')
a = soup.find_all('div',attrs={'class':'col-xs-2-4 shopee-search-item-result__item'})
c = []
for elem in a:
    try:
        b = elem.find('div',class_='_1NoI8_ _16BAGk')
        c.append(b.text)
    except:
        pass
len(c)
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
time.sleep(3)
driver.execute_script('window.scrollTo(0, 100*document.body.scrollHeight);')
driver.get(url_query)
driver.implicitly_wait(20)
driver.execute_script('return document.documentElement.scrollHeight;')

y = 1000
for timer in range(0,50):
    driver.execute_script("window.scrollTo(0, "+str(y)+")")
    y += 1000  
    time.sleep(1)
    
def scroll_to_bottom(driver):

    old_position = 0
    new_position = None

    while new_position != old_position:
        # Get old scroll position
        old_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))
        # Sleep and Scroll
        time.sleep(1)
        driver.execute_script((
                "var scrollingElement = (document.scrollingElement ||"
                " document.body);scrollingElement.scrollTop ="
                " scrollingElement.scrollHeight;"))
        # Get new position
        new_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))

pre_scroll_height = driver.execute_script('return document.documentElement.scrollHeight;')
run_time = 10
for iter in range(0,pre_scroll_height,300):
    driver.execute_script("window.scrollTo(0, {});".format(iter))
    time.sleep(1.5)
    
pre_scroll_height = driver.execute_script('return document.body.scrollHeight;')
run_time, max_run_time = 0, 10
while True:
    iteration_start = time.time()
    # Scroll webpage, the 100 allows for a more 'aggressive' scroll
    driver.execute_script('window.scrollTo(0, 5*document.body.scrollHeight);')

    post_scroll_height = driver.execute_script('return document.body.scrollHeight;')

    scrolled = post_scroll_height != pre_scroll_height
    timed_out = run_time >= max_run_time

    if scrolled:
        run_time = 0
        pre_scroll_height = post_scroll_height
    elif not scrolled and not timed_out:
        run_time += time.time() - iteration_start
    elif not scrolled and timed_out:
        break

scrolls = 4
while True:
    scrolls -= 1
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(3)
    if scrolls < 0:
        break

def __scroll_down_page(self, speed=8):
    current_scroll_position, new_height= 0, 1
    while current_scroll_position <= new_height:
        current_scroll_position += speed
        self.__driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
        new_height = self.__driver.execute_script("return document.body.scrollHeight")
