'''
code by emanchez on github (sanchez.emmanuelm@gmail.com)
this code is adapted from a class project which originally produced a category ID along with the comments. This function was removed for this project to avoid using YouTube's API.
'''

import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time


#FUNCTIONS
def write_to_file(comments, filename="youtube_file.txt", cat_id=""):
    # write comments as tab-seperated-values in format "{category_id}\t{comment}"
    # must write function to find category id (using YouTube API), otherwise it will be blank
    if (len(comments) == 0): #DEBUG: print warning if no comments were loaded
        for i in range(0,10): # galaxy brain: error is easier to notice if you print error 10 times
            print("WARNING: NO COMMENTS FOUND")
    with open(filename, 'a') as youtube_comments_file:
        failed = 0 #DEBUG
        for i in comments:
            try:
                temp = i.replace("\n", " ") #remove newline characters to maintain integrity of output file
                temp = temp.replace("\t", " ") #remove tabs from ripped comments to maintain integrity of tab-seperated-values
                youtube_comments_file.write(cat_id + "\t" + temp + "\n")
            except:
                failed += 1 # the error here is that a comment may have a character that is not utf-8 which will crash the program
        if failed > 0: #DEBUG
            print("failed to write: " + str(failed) + "comments")


def get_driver(profile_filepath=""):
    # Get driver using firefox profile filepath, if no parameter passed, selenium will use a default firefox instance (no addons or previous settings will load)
    
    if profile_filepath != "":
        print("Loading profile...")
        profile = webdriver.FirefoxProfile(profile_filepath) # open the firefox profile for adblock
        driver = webdriver.Firefox(profile) # open firefox with the profile retrieved
    else:
        print("Loading browser...")
        driver = webdriver.Firefox() # open firefox without a profile
    return driver
    

def get_comments(url, driver, action, delay=5):
    print("grabbing url...")
    driver.get(url) # go to url
    
    print("scrolling...")
    time.sleep(delay) # load page

    # scroll down on page
    action.key_down(Keys.PAGE_DOWN) #buffer key-press [PGDN]
    action.perform() #do key-press
    action.key_up(Keys.PAGE_DOWN) #buffer key-release [PGDN]
    action.perform() #do key-release
    
    print("grabbing comments...")
    time.sleep(delay) # load comments
    
    # get comment elements
    comment_elements = m_driver.find_elements_by_xpath("//yt-formatted-string[@id='content-text'][@class='style-scope ytd-comment-renderer']") #current (Jan2019) xml path to html element that holds comments
    # get comments as text
    comments = [i.text for i in comment_elements]
    return comments


############# SAMPLE PROGRAM #############

#MAIN
if __name__ == "__main__":
    print("Creating driver...")
    m_driver = get_driver() # start firefox browser

    print("Creating action chains...")
    m_action = ActionChains(m_driver) # virtual events (key press/release)

    
    print("start program")

    link = "https://www.youtube.com/watch?v=VKh9inKBlks" # example youtube link
    filename = "youtube_comments.txt"

    comments = get_comments(link, m_driver, m_action, 10)
    write_to_file(comments, filename)
'''
    except:
        for i in range(0,10):
            print("Whoops! couldn't grab those comments")
'''
