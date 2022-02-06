import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

YOUTUBE_TRENDING_URL = 'https://www.youtube.com/feed/trending'
VIDEO_DIV_TAG = 'ytd-video-renderer'
  
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

if __name__ == '__main__':
  print('Create driver')
  driver = get_driver()

  print('Fetching trending Youtube videos')
  videos = get_videos(driver)
  print(f'Found {len(videos)} videos')

  print('Parse top 10 videos')
  video_data = [parse_video(video) for video in videos[:10]]

  print('Save the data to a CSV')
  video_df = pd.DataFrame(video_data)
  print(video_df)
  video_df.to_csv('trending.csv')