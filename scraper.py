# import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
import smtplib
import os

YOUTUBE_TRENDING_URL = 'https://www.youtube.com/feed/trending?gl=VN'
VIDEO_DIV_TAG = 'ytd-video-renderer'
SENDER_EMAIL = 'testsenderemail2020@gmail.com'
RECEIVER_EMAIL = 'testsenderemail2020@gmail.com'
SENDER_PASSWORD = os.environ['GMAIL_PASSWORD']

def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument('--headless')
  driver = webdriver.Chrome(options=chrome_options)
  driver.implicitly_wait(30)
  return driver

def get_videos(driver):
  driver.get(YOUTUBE_TRENDING_URL)
  videos = driver.find_elements(By.TAG_NAME, VIDEO_DIV_TAG)
  return videos

def parse_video(video):
  title_tag = video.find_element(By.ID, 'video-title')
  title = title_tag.text
  url = title_tag.get_attribute('href')

  thumbnail_tag = video.find_element(By.TAG_NAME, 'img')
  thumbnail_url = thumbnail_tag.get_attribute('src')

  channel_div = video.find_element(By.TAG_NAME, 'ytd-channel-name')
  channel_name = channel_div.text
  description = video.find_element(By.ID, 'description-text').text
  return {
    'title' : title,
    'url': url,
    'thumbnail_url': thumbnail_url,
    'channel' : channel_name,
    'description': description
  }

def send_email(body):
  try:
    server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server_ssl.ehlo()
    
    subject = 'YouTube Trending Videos'

    email_text = f"""
    From: {SENDER_EMAIL}
    To: {RECEIVER_EMAIL}
    Subject: {subject}
    {body}
    """

    server_ssl.login(SENDER_EMAIL, SENDER_PASSWORD)
    server_ssl.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, email_text)
    server_ssl.close()

  except:
      print('Something went wrong...')
      
if __name__ == '__main__':
  print('Create driver')
  driver = get_driver()

  print('Fetching trending Youtube videos')
  videos = get_videos(driver)
  print(f'Found {len(videos)} videos')

  print('Parse top 10 videos')
  videos_data = [parse_video(video) for video in videos[:10]]

  # print('Save the data to a CSV')
  # video_df = pd.DataFrame(video_data)
  # print(video_df)
  # video_df.to_csv('trending.csv')

  print("Send the results over email")
  body = json.dumps(videos_data, indent=2)
  send_email(body)

  print('Finished.')