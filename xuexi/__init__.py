#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@project: AutoXue
@file: __init__.py
@author: kessil
@contact: https://github.com/kessil/AutoXue/
@time: 2019-10-26(星期六) 09:03
@Copyright © 2019. All rights reserved.
'''
import re
import random
import time
import requests
import string
from urllib.parse import quote
from collections import defaultdict
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from .unit import Timer, logger, caps, rules, prefers, cfg
from .model import BankQuery

class CONST:
    # 阅读文章时长要求(单位：秒)
    ARTICLE_TIME_REQUIRED = 720
    VIDEO_TIME_REQUIRED = 1080
    # 挑战答题题数上下限
    CHALLENGE_COUNT_MIN = cfg.getint('nums', 'challenge_count_min')
    CHALLENGE_COUNT_MAX = cfg.getint('nums', 'challenge_count_max')
    # 挑战答题题数
    CHALLENGE_COUNT = cfg.getint('nums', 'challenge_count') or 0
    # 挑战答题提交延时上下限
    CHALLENGE_DELAY_MIN = cfg.getint('nums', 'challenge_delay_min')
    CHALLENGE_DELAY_MAX = cfg.getint('nums', 'challenge_delay_max')
    # 每日答题组数
    DAILY_GROUP_COUNT = cfg.getint('nums', 'daily_group_count') or 0
    # 每日答题组间延时上下限
    DAILY_GROUP_DELAY_MIN = cfg.getint('nums', 'daily_group_delay_min')
    DAILY_GROUP_DELAY_MAX = cfg.getint('nums', 'daily_group_delay_max')
    # 试听学习观看视频数量上下限
    VIDEO_COUNT_MIN = cfg.getint('nums', 'video_count_min')
    VIDEO_COUNT_MAX = cfg.getint('nums', 'video_count_max')
    VIDEO_COUNT = cfg.getint('nums', 'video_count') or 0
    # 试听学习每则视频观看时间上下限
    VIDEO_DELAY_MIN = cfg.getint('nums', 'video_delay_min')
    VIDEO_DELAY_MAX = cfg.getint('nums', 'video_delay_max')

    # 新闻学习数量上下限
    ARTICLE_COUNT_MIN = cfg.getint('nums', 'article_count_min')
    ARTICLE_COUNT_MAX = cfg.getint('nums', 'article_count_max')
    ARTICLE_COUNT = cfg.getint('nums', 'article_count') or 0

    # 新闻学习阅读时间上下限
    ARTICLE_DELAY_MIN = cfg.getint('nums', 'article_delay_min')
    ARTICLE_DELAY_MAX = cfg.getint('nums', 'article_delay_max')
    ARTICLE_STAR_COUNT = cfg.getint('nums', 'article_star_count')


class Automation():
    # 初始化 Appium 基本参数
    def __init__(self):
        self.desired_caps = {
            "platformName": caps["platformname"],
            "platformVersion": caps["platformversion"],
            "automationName": caps["automationname"],
            "unicodeKeyboard": caps["unicodekeyboard"],
            "resetKeyboard": caps["resetkeyboard"],
            "noReset": caps["noreset"],
            'newCommandTimeout': 800,
            "deviceName": caps["devicename"],
            "uuid": caps["uuid"],
            "appPackage": caps["apppackage"],
            "appActivity": caps["appactivity"]
        }
        logger.info('打开 appium 服务,正在配置...')
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        self.wait = WebDriverWait(self.driver, 10)
        self.size = self.driver.get_window_size()

    # 屏幕方法
    def swipe_up(self):
        # 向上滑动屏幕
        self.driver.swipe(self.size['width'] * random.uniform(0.55, 0.65),
                          self.size['height'] * random.uniform(0.65, 0.75),
                          self.size['width'] * random.uniform(0.55, 0.65),
                          self.size['height'] * random.uniform(0.25, 0.35), random.uniform(800, 1200))
        logger.debug('向上滑动屏幕')

    def swipe_down(self):
        # 向下滑动屏幕
        self.driver.swipe(self.size['width'] * random.uniform(0.55, 0.65),
                          self.size['height'] * random.uniform(0.25, 0.35),
                          self.size['width'] * random.uniform(0.55, 0.65),
                          self.size['height'] * random.uniform(0.65, 0.75), random.uniform(800, 1200))
        logger.debug('向下滑动屏幕')

    def swipe_right(self):
        # 向右滑动屏幕
        self.driver.swipe(self.size['width'] * random.uniform(0.01, 0.11),
                          self.size['height'] * random.uniform(0.75, 0.89),
                          self.size['width'] * random.uniform(0.89, 0.98),
                          self.size['height'] * random.uniform(0.75, 0.89), random.uniform(800, 1200))
        logger.debug('向右滑动屏幕')
    def swipe_left(self):
        # 向右滑动屏幕
        self.driver.swipe(self.size['width'] * random.uniform(0.89, 0.98),
                          self.size['height'] * random.uniform(0.75, 0.89),
                          self.size['width'] * random.uniform(0.01, 0.11),
                          self.size['height'] * random.uniform(0.75, 0.89), random.uniform(800, 1200))
        logger.debug('向左滑动屏幕')

    # 返回事件
    def safe_back(self, msg='default msg'):
        logger.debug(msg)
        self.driver.keyevent(4)
        time.sleep(1)

    def safe_click(self, ele:str):
        self.wait.until(EC.presence_of_element_located((By.XPATH, ele))).click()
        time.sleep(1)

    def __del__(self):
        self.driver.close_app()
        self.driver.quit()


class App(Automation):
    def __init__(self):
        self.bq = BankQuery()
        self.bank = None
        self._score = defaultdict(tuple)
        super().__init__()
        self.driver.wait_activity('com.alibaba.android.rimet.biz.home.activity.HomeActivity', 20, 3)
        # logger.error(self.driver.current_activity)

    def view_score(self):
        self.safe_click(rules['score_entry'])
        titles = ["登录", "阅读文章", "视听学习", "文章学习时长", 
                "视听学习时长", "每日答题", "每周答题", "专项答题", 
                "挑战答题", "订阅", "收藏", "分享", "发表观点"]
        score_list = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, rules['score_list'])))
        for t, score in zip(titles, score_list):
            s = score.get_attribute("name")
            self._score[t] = tuple([int(x) for x in re.findall(r'\d+', s)])

        # print(self._score)
        for i in self._score:
            logger.debug(f'{i}, {self._score[i]}')
        self.safe_back('score -> home')

        # 增加《动态计算积分方案》的功能
        g, _ = self._score["挑战答题"]
        if 0 == g:
            self.count_challenge = random.randint(max(10, CONST.CHALLENGE_COUNT_MIN), 
                                                  min(20, CONST.CHALLENGE_COUNT_MAX))
        elif 3 == g:
            self.count_challenge = random.randint(max(5, CONST.CHALLENGE_COUNT_MIN), 
                                                  min(10, CONST.CHALLENGE_COUNT_MAX))
        else:
            self.count_challenge = 0
        self.count_challenge = CONST.CHALLENGE_COUNT

        g, _ = self._score["阅读文章"]







    def _search(self, content, options, exclude=''):
        logger.debug(f'search {content} in baidu <exclude {exclude}>')
        content = re.sub(r'[\(（]出题单位.*', "", content)
        # logger.info(content)
        if options[-1].startswith("以上") and chr(len(options)+64) not in exclude:
            logger.info(options)
            logger.info(f'根据经验: {chr(len(options)+64)} 很可能是正确答案')
            return len(options)-1
        url = quote('https://www.sougou.com/s?wd=' + content, safe=string.printable)
        headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        }
        response = requests.get(url, headers=headers).text
        counts = []
        for i, option in zip(['A', 'B', 'C', 'D', 'E', 'F'], options):
            count = response.count(option)
            counts.append((count, i))
            logger.info(f'{i}. {option}: {count}')
        counts = sorted(counts, key=lambda x:x[0], reverse=True)
        counts = [x for x in counts if x[1] not in exclude]
        c, i = counts[0]
        logger.info(f'根据搜索结果: {i} 很可能是正确答案')
        return ord(i)-65

    def _verify_answer(self, content, options):
        # logger.info("\n".join(options))
        self.bank = self.bq.get({
            "category": "挑战题",
            "content": content,
            "options": options
        })
        # logger.warning(self.bank)
        if self.bank:
            if '' != self.bank["answer"]:
                logger.info(options)
                logger.info(f'提交正确答案 {self.bank["answer"]}')
                return ord(self.bank["answer"])-65
            else:
                logger.info(f'已知的排除项有: {self.bank["excludes"]}')
                return self._search(content, options, self.bank["excludes"])
        return self._search(content, options)

    def _challenge_cycle(self, num):
        self.safe_click(rules['challenge_entry'])
        while True:
            self.bank = None
            content = self.wait.until(EC.presence_of_element_located((By.XPATH, rules['challenge_content']))).get_attribute("name")
            option_elements = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, rules['challenge_options'])))
            options = [x.get_attribute("name") for x in option_elements]
            length_of_options = len(options)
            # print(content, options)
            logger.info(f'<{num}> {content}')
            choose_index = self._verify_answer(content, options) # <int>0~length_of_options
            challenge_delay = random.randint(CONST.CHALLENGE_DELAY_MIN, CONST.CHALLENGE_DELAY_MAX)
            logger.info(f'随机延时 {challenge_delay} 秒...')
            time.sleep(challenge_delay)            
            if 0 >= num:
                logger.debug(f'已达成指定题量，选项偏移一位,自动回答错误')
                choose_index = (choose_index + 1) % length_of_options
            option_elements[choose_index].click()

            try:
                time.sleep(2)
                wrong = self.driver.find_element_by_xpath(rules['challenge_revival'])
                # 找到了，说明答错，先把排除项推送了
                logger.debug("很遗憾这题回答错误...")
                if not self.bank or "" == self.bank["answer"]:
                    self.bq.put({
                        "category": "挑战题",
                        "content": content,
                        "options": options,
                        "answer": "",
                        "excludes": chr(65+choose_index),
                        "notes": ""
                    })
                else:
                    logger.debug('故意答错的题目不要put')
                # if "分享就能复活" == wrong.get_attribute("name"):
                #     logger.debug("分享再来一局吧...")
                #     wrong.click()
                #     time.sleep(2)
                # elif "再来一局" == wrong.get_attribute("name"):
                #     logger.debug("很遗憾呢，请返回再接再厉……")
                #     break
                # else:
                #     logger.debug("肯定出问题了！居然会来到我的位置？")
                self.safe_back('challenge -> quiz')
                break
            except:
                # 没找到，回答正确，继续吧
                num -= 1
                logger.debug("回答正确，请继续你的表演……")
                if not self.bank:
                    logger.debug(f'扩充题库...')
                    self.bq.post({
                        "category": "挑战题",
                        "content": content,
                        "options": options,
                        "answer": chr(65+choose_index),
                        "excludes": "",
                        "notes": ""
                    })
                elif self.bank and '' == self.bank['answer']:
                    logger.debug(f'更新题库...')
                    self.bq.put({
                        "category": "挑战题",
                        "content": content,
                        "options": options,
                        "answer": chr(65+choose_index),
                        "excludes": "",
                        "notes": ""
                    })


        return num

    def challenge(self, challenge_count=None):
        if not prefers['challenge_enable']:
            logger.info(f'根据配置，跳过挑战答题')
            return
        if self.back_or_not('挑战答题'):
            return 
        if not challenge_count:
            challenge_count = random.randint(CONST.CHALLENGE_COUNT_MIN, CONST.CHALLENGE_COUNT_MAX)
        logger.info(f'本局挑战答题目标 {challenge_count} 题')
        while True:
            if 0 >= self._challenge_cycle(challenge_count):
                logger.info(f'已成功挑战 {challenge_count} 题，返回首页！')
                break
            else:
                logger.info(f'未完成{challenge_count}题，再来一局……')
                time.sleep(5)

    def some_music(self):
        if self.back_or_not('视听学习时长'):
            return 
        logger.debug('正在打开《音乐之声》...')
        self.safe_click('//*[@resource-id="cn.xuexi.android:id/home_bottom_tab_button_mine"]')
        self.safe_click('//*[@text="听新闻广播"]')
        self.safe_click('//*[@text="音乐之声"]')
        self.safe_click(rules['home_entry'])

    def watch(self, video_count=None):
        if not video_count:
            logger.info('视听学习已完成，无须重复学习')
            return
        logger.info("开始学习百灵视频...")
        self.safe_click(rules['bailing_enter'])
        self.safe_click(rules['video_first'])
        if not video_count:
            video_count = random.randint(CONST.VIDEO_COUNT_MIN, CONST.VIDEO_COUNT_MAX)
        logger.info(f'预计观看视频 {video_count} 则')
        while video_count:
            video_count -= 1
            video_delay = random.randint(CONST.VIDEO_DELAY_MIN, CONST.VIDEO_DELAY_MAX)
            logger.info(f'正在观看视频 <{video_count}#> {video_delay} 秒进入下一则...')
            time.sleep(video_delay)
            self.swipe_up()
        else:
            logger.info(f'视听学习完毕，正在返回...')
            self.safe_back('video -> bailing')
            logger.info(f'正在返回首页...')
            self.safe_click(rules['home_entry'])

    def _daily_cycle(self):
        for i in range(5):
            self.bank = None
            time.sleep(random.randint(3, 5))
            category = self.wait.until(EC.presence_of_element_located((By.XPATH, rules["daily_category"]))).get_attribute("name")
            if "填空题" == category:
                self._blank()
            elif "单选题" == category:
                self._radio()
            elif "多选题" == category:
                self._check()
            else:
                logger.error(f"未知的题目类型 {category}")

    def daily(self, daily_count=None):
        if not prefers['daily_enable']:
            logger.info(f'根据配置，跳过每日答题')
            return

        if self.back_or_not('每日答题'):
            return 
        
        gain, total = self._score['每日答题']
        self.safe_click(rules["daily_entry"])

        if not daily_count:
            while True:
                self._daily_cycle()
                score = self.wait.until(EC.presence_of_element_located((By.XPATH, rules["daily_score"]))).get_attribute("name")
                try:
                    score = int(score)
                except:
                    raise TypeError('integer required')
                logger.debug(f'本轮得分 {score} 【{gain}/{total}】')
                gain += score
                if gain >= total:
                    logger.info(f'每日答题已完成')
                    # 返回我要答题页面
                    self.safe_back("daily -> quiz")
                    break
                else:
                    delay = random.randint(CONST.DAILY_GROUP_DELAY_MIN, CONST.DAILY_GROUP_DELAY_MAX)
                    logger.info(f'每日答题未完成，{delay} 秒后再来一组')
                    time.sleep(delay)
                    self.safe_click(rules['daily_again'])
                    continue
        else:
            while daily_count:
                self._daily_cycle()
                daily_count -= 1
                logger.info(f'每日答题完成第{daily_count}#组，再来一组')
                self.safe_click(rules['daily_again'])

    def _submit(self):
        self.safe_click(rules["daily_submit"])
        time.sleep(random.randint(2,3))

    def _blank(self):
        contents = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, rules["daily_blank_content"])))
        content = " ".join([x.get_attribute("name") for x in contents])
        blank_edits = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, rules["daily_blank_edits"])))
        # print(type(blank_edits), isinstance(blank_edits, list), len(blank_edits))
        logger.info(f'填空题 {content}')
        self.bank = self.bq.get({
            "category": "填空题",
            "content": content
        })
        if self.bank:
            words = self.bank["answer"].split(" ")
            logger.info(f'提交正确答案 {words}')
        else:
            words = ["不忘初心牢记使命"]*len(blank_edits)
            logger.info(f'提交默认答案 {words}')
        for k,v in zip(blank_edits, words):
            time.sleep(3)
            k.send_keys(v)

        self._submit()
        try:            
            wrong_or_not = self.driver.find_element_by_xpath(rules["daily_wrong_or_not"])
            logger.debug("填空题回答错误")
            right_answer = self.driver.find_element_by_xpath(rules["daily_answer"]).get_attribute("name")
            answer = re.sub(r'正确答案： ', '', right_answer)
            logger.debug(f"正确答案 {answer}")
            notes = self.driver.find_element_by_xpath(rules["daily_notes"]).get_attribute("name")
            logger.debug(f"解析 {notes}")
            self._submit()
            if 1 == len(blank_edits):
                self.bq.post({
                    "category": "填空题",
                    "content": content,
                    "options": [],
                    "answer": answer,
                    "excludes": "",
                    "notes": notes
                })
            else:
                logger.error("多位置的填空题待完善...")
        except:
            logger.debug("填空题回答正确")

    def _radio(self):
        content = self.wait.until(EC.presence_of_element_located((By.XPATH, rules["daily_content"]))).get_attribute("name")
        option_elements = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, rules["daily_options"])))
        options = [x.get_attribute("name") for x in option_elements]
        length_of_options = len(options)
        logger.info(f"单选题 {content}\n{options}")
        self.bank = self.bq.get({
            "category": "单选题",
            "content": content,
            "options": options
        })
        if self.bank:
            answer = self.bank["answer"]
            logger.info(f"提交正确答案 {answer}")
            choose_index = ord(answer)-65
            option_elements[choose_index].click()
        else:
            choose_index = self._search(content, options)
            logger.info(f"提交正确答案 {chr(choose_index+65)}")
            option_elements[choose_index].click()

        # 提交答案
        self._submit()
        try:            
            wrong_or_not = self.driver.find_element_by_xpath(rules["daily_wrong_or_not"])
            logger.debug("单选题回答错误")
            right_answer = self.driver.find_element_by_xpath(rules["daily_answer"]).get_attribute("name")
            answer = re.sub(r'正确答案： ', '', right_answer)
            logger.debug(f"正确答案 {answer}")
            notes = self.driver.find_element_by_xpath(rules["daily_notes"]).get_attribute("name")
            logger.debug(f"解析 {notes}")
            self._submit()
            self.bq.post({
                "category": "单选题",
                "content": content,
                "options": options,
                "answer": answer,
                "excludes": "",
                "notes": notes
            })
        except:
            logger.debug("单选题回答正确")
            if not self.bank:
                self.bq.post({
                    "category": "单选题",
                    "content": content,
                    "options": options,
                    "answer": chr(choose_index+65),
                    "excludes": "",
                    "notes": ""
                })

    def _check(self):
        content = self.wait.until(EC.presence_of_element_located((By.XPATH, rules["daily_content"]))).get_attribute("name")
        option_elements = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, rules["daily_options"])))
        options = [x.get_attribute("name") for x in option_elements]
        length_of_options = len(options)
        logger.info(f"多选题 {content}\n{options}")
        self.bank = self.bq.get({
            "category": "多选题",
            "content": content,
            "options": options
        })
        if self.bank:
            answer = self.bank["answer"]
            logger.debug(f"提交答案 {answer}")
            for k, option in zip(['A', 'B', 'C', 'D', 'E', 'F', 'G'], option_elements):
                if k in answer:
                    option.click()
                    time.sleep(1)
                else:
                    continue
        else:
            logger.debug('默认全选...')
            for option in option_elements:
                option.click()
                time.sleep(1)
        # 提交答案
        self._submit()
        try:
            wrong_or_not = self.driver.find_element_by_xpath(rules["daily_wrong_or_not"])
            logger.debug("多选题回答错误")
            right_answer = self.driver.find_element_by_xpath(rules["daily_answer"]).get_attribute("name")
            answer = re.sub(r'正确答案： ', '', right_answer)
            logger.debug(f"正确答案 {answer}")
            notes = self.driver.find_element_by_xpath(rules["daily_notes"]).get_attribute("name")
            logger.debug(f"解析 {notes}")
            self._submit()
            self.bq.post({
                "category": "多选题",
                "content": content,
                "options": options,
                "answer": answer,
                "excludes": "",
                "notes": notes
            })
        except:
            logger.debug("多选题回答正确")
            if not self.bank:
                self.bq.post({
                    "category": "多选题",
                    "content": content,
                    "options": options,
                    "answer": "ABCDEFG"[:length_of_options],
                    "excludes": "",
                    "notes": ""
                })
        
    def quiz(self):
        self.safe_click(rules['mine_entry'])
        self.safe_click(rules['quiz_entry'])
        if random.random() > 0.5:
            logger.debug(f'挑战答题优先')
            self.challenge()
            self.daily()
        else:
            logger.debug(f'每日答题优先')
            self.daily()
            self.challenge()

        self.safe_back('quiz -> mine')
        self.safe_back('mine -> home')

    def start(self):
        self.view_score()
        if random.random() > 0.5:
            logger.debug(f'视听学习优先')
            self.watch()
            self.some_music()            
            if random.random() > 0.5:
                self.read()
                self.quiz()
            else:
                self.quiz()
                self.read()
        else:
            logger.debug(f'视听学习置后')
            self.some_music()
            if random.random() > 0.5:
                self.read()
                self.quiz()
            else:
                self.quiz()
                self.read()
            self.watch()

    def read(self, article_count=None, star_count=None):
        if not prefers['read_enable']:
            logger.info(f'根据配置，跳过阅读文章')
            return
        if self.back_or_not('阅读文章'):
            return 
        logger.debug(f'正在进行新闻学习...')
        vol_not_found = True
        while vol_not_found:
            volumns = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, rules['article_volumn'])))
            first_vol = volumns[0]
            for vol in volumns:
                title = vol.get_attribute("name")
                logger.debug(title)
                if "订阅" == title:
                    vol.click()
                    vol_not_found = False
                    break
                else:
                    continue
            else:
                logger.debug('未找到，左滑一屏')
                self.driver.scroll(vol, first_vol, duration=500)
        if not article_count:
            article_count = random.randint(CONST.ARTICLE_COUNT_MIN, CONST.ARTICLE_COUNT_MAX)
        if not star_count:
            star_count = CONST.ARTICLE_STAR_COUNT
        logger.info(f'阅读时刻，开始！ {article_count} 篇目')
        self._article_cycle(article_count, star_count)
    
    def _star(self):
        if not prefers['stars_enable']:
            logger.info(f'根据配置，跳过收藏文章')
            return
        logger.debug(f'这篇文章真是妙笔生花呀！收藏啦！')
        self.safe_click(rules['article_stars'])
        # self.safe_click(rules['article_stars']) # 取消收藏

    def _share(self):
        if not prefers['share_enable']:
            logger.info(f'根据配置，跳过分享文章')
            return
        logger.debug(f'好东西必须和好基友分享，走起，转起！')
        self.safe_click(rules['article_share'])
        self.safe_click(rules['article_share_xuexi'])
        time.sleep(3)
        self.safe_back('share -> article')

    def _comments(self):
        if not prefers['comments_enable']:
            logger.info(f'根据配置，跳过评论文章')
            return
        logger.debug(f'哇塞，这么精彩的文章必须留个言再走！')
        self.safe_click(rules['article_comments'])
        edit_area = self.wait.until(EC.presence_of_element_located((By.XPATH, rules['article_comments_edit'])))
        edit_area.send_keys("不断学习，不断进步，充实每一天")
        self.safe_click(rules['article_comments_publish'])
        time.sleep(2)
        self.safe_click(rules['article_comments_list'])
        self.safe_click(rules['article_comments_delete'])
        self.safe_click(rules['article_comments_delete_confirm'])

    def star_share_comments(self):
        if random.random() < 0.33:
            self._comments()
            if random.random() < 0.5:
                self._star()
                self._share()
            else:
                self._share()
                self._star()
        else:
            if random.random() < 0.5:
                self._star()
                self._share()
            else:
                self._share()
                self._star()
            self._comments()
   

    def _article_cycle(self, num, star_count):
        titles = []
        while num or star_count:
            articles = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, rules['article_list'])))
            for article in articles:
                title = article.get_attribute("name")
                if title in titles:
                    continue
                article.click()
                logger.info(f'<{num}> 当前篇目 {title}')
                article_delay = random.randint(CONST.ARTICLE_DELAY_MIN, CONST.ARTICLE_DELAY_MAX)
                logger.info(f'阅读时间估计 {article_delay} 秒...')
                while article_delay > 0:
                    delay = random.randint(min(10, article_delay), min(20, article_delay))
                    logger.debug(f'延时 {delay} 秒...')
                    time.sleep(delay)
                    article_delay -= delay
                    self.swipe_up()
                else:
                    logger.debug(f'{article_delay}秒 学习完毕')

                if star_count > 0:
                    try:
                        comment_area = self.driver.find_element_by_xpath(rules['article_comments'])
                        self.star_share_comments()
                        star_count -= 1
                    except:
                        logger.debug('这是一篇关闭评论的文章')

                titles.append(title)
                num -= 1
                self.safe_back('article -> list')
            else:
                self.swipe_up()


    def back_or_not(self, title):
        gain, total = self._score[title]
        if gain == total:
            logger.info(f'{title} 已完成')
            return True
        return False


    def test(self):
        self.view_score()
        self.quiz()  


class Challenge(App):
    def __init__(self):
        super().__init__()

    def _challenge_cycle(self, num):
        pass

    def start(self):
        pass

class Daily(App):
    def __init__(self):
        super().__init__()

    def _cycle(self):
        pass

    def start(self):
        pass

class Read(App):
    def __init__(self):
        super().__init__()

    def _cycle(self, num):
        pass

    def start(self):
        pass

class View(App):
    def __init__(self):
        super().__init__()

    def _cycle(self, num):
        pass

    def start(self):
        pass
