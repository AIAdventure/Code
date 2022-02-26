import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from kora.selenium import wd
from selenium.webdriver.common.by import By

class Scraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--binary=/path/to/other/chrome/binary")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--window-size=1920x1080")
        exec_path = "chromedriver"
        self.driver = webdriver.Chrome(
            options=chrome_options, executable_path=exec_path
        )
        self.max_depth = 10
        self.end_actions = {
            "End Game and Leave Comments",
            "Click here to End the Game and Leave Comments",
            "See How Well You Did (you can still back-page afterwards if you like)",
            "You have died.",
            "You have died",
            "Epilogue",
            "Save Game",
            "Your quest might have been more successful...",
            "5 - not the best, certainly not the worst",
            "The End! (leave comments on game)",
            "6 - it's worth every cent",
            "You do not survive the journey to California",
            "Quit the game.",
            "7 - even better than Reeses' Cups®",
            "8 - it will bring you enlightenment",
            "End of game! Leave a comment!",
            "Better luck next time",
            "click here to continue",
            "Rating And Leaving Comments",
            "You do not survive your journey to California",
            "Your Outlaw Career has come to an end",
            "Thank you for taking the time to read my story",
            "You have no further part in the story, End Game and Leave Comments",
            "",
            "You play no further part in this story. End Game and Leave Comments",
            "drivers",
            "Alas, poor Yorick, they slew you well",
            "My heart bleeds for you",
            "To End the Game and Leave Comments click here",
            "Call it a day",
            "Check the voicemail.",
            "reset",
            "There's nothing you can do anymore...it's over.",
            "To Be Continued...",
            "Thanks again for taking the time to read this",
            "If you just want to escape this endless story you can do that by clicking here",
            "Boo Hoo Hoo",
            "End.",
            "Pick up some money real quick",
            "",
            "Well you did live a decent amount of time in the Army",
            "End Game",
            "You have survived the Donner Party's journey to California!",

        }
        self.texts = set()
        
    def GoToURL(self, url):
        self.texts = set()
        self.driver.get(url)
        time.sleep(0.5)

    def GetText(self):
        div_elements = ele= self.driver.find_elements(By.XPATH, "//div[@class='description']")
        text = div_elements[0].text
        return text

    def GetLinks(self):
        ele= self.driver.find_elements(By.XPATH, "//div[@class='room-choices mt-4']/ul/li/a")
        return ele
    def GoBack(self):
        self.driver.back()
        time.sleep(0.2)

    def ClickAction(self, links, action_num):
        links[action_num].click()
        time.sleep(0.2)

    def GetActions(self):
        return [link.text for link in self.GetLinks()[:]]

    def NumActions(self):
        return len(self.GetLinks())

    def BuildTreeHelper(self, parent_story, action_num, depth, old_actions):
        depth += 1
        action_result = {}

        action = old_actions[action_num]
        print("Action is ", repr(action))
        action_result["action"] = action

        links = self.GetLinks()
        if action_num >= len(links):
            return None

        self.ClickAction(links, action_num)
        result = self.GetText()
        if result == parent_story or result in self.texts:
            self.GoBack()
            return None

        self.texts.add(result)
        print(len(self.texts))

        action_result["result"] = result

        actions = self.GetActions()
        action_result["action_results"] = []

        for i, action in enumerate(actions):
            if actions[i] not in self.end_actions:
                sub_action_result = self.BuildTreeHelper(result, i, depth, actions)
                if action_result is not None:
                    action_result["action_results"].append(sub_action_result)

        self.GoBack()
        return action_result

    def BuildStoryTree(self, url):
        scraper.GoToURL(url)
        text = scraper.GetText()
        actions = self.GetActions()
        story_dict = {}
        story_dict["tree_id"] = url
        story_dict["context"] = ""
        story_dict["first_story_block"] = text
        story_dict["action_results"] = []

        for i, action in enumerate(actions):
            if action not in self.end_actions:
                action_result = self.BuildTreeHelper(text, i, 0, actions)
                if action_result is not None:
                    story_dict["action_results"].append(action_result)
            else:
                print("done")

        return story_dict


    def save_tree(tree, filename):
        with open(filename, "w") as fp:
            json.dump(tree, fp)
            
urls =  [
        "https://infinite-story.com/story/room.php?id=58387",
        "https://infinite-story.com/story/room.php?id=87587",
        "https://infinite-story.com/story/room.php?id=33470",
        "https://infinite-story.com/story/room.php?id=96691",
        "https://infinite-story.com/story/room.php?id=98844",
        "https://infinite-story.com/story/room.php?id=47871",
        "https://infinite-story.com/story/room.php?id=29088",
        "https://infinite-story.com/story/room.php?id=56017",
        "https://infinite-story.com/story/room.php?id=200154",
        "https://infinite-story.com/story/room.php?id=36382",
         
        
        ]      
            
scraper = Scraper()
for i in range(len(urls)):
    print("****** Extracting Adventure ", urls[i], " ***********")
    tree = scraper.BuildStoryTree(urls[i])
    save_tree(tree, "F:/AIDungeon-master/AIDungeon-master/data/story" + str(41 + i) + ".json")

print("done")

