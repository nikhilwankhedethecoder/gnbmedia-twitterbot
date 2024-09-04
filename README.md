# GNB Twitter Bot

## Overview

The [GNB](www.x.com/gnbmedia) Twitter Bot automatically fetches the latest news headlines from the NewsAPI and tweets them on Twitter. It ensures no duplicate tweets are posted, logs all activities, handles errors, and sends email notifications for successful tweets and errors. The bot is designed to run every hour, making sure the latest news is always tweeted.

## Features

- **Automatic News Tweeting**: Fetches the latest news from NewsAPI and tweets headlines on your Twitter account.
- **Duplicate Handling**: Avoids posting duplicate tweets by tracking already posted headlines.
- **Error Handling**: Logs errors and handles issues like rate limits and duplicate content gracefully.
- **Email Notifications**: Sends email updates on successful tweets, errors, and script status.
- **Hourly Execution**: Runs automatically every hour to fetch and tweet the latest news.

## Future Features

- **Image Posting**: The bot will post images along with tweets, either using images from the news articles or generating custom images with a blue background, white text, and the GNB logo if no image is available.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/nikhilwankhedethecoder/gnbmedia-twitterbot.git
   cd <repository_directory>
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   Create a `.env` file in the root directory and add the following variables:
   ```plaintext
   TWITTER_API_KEY=your_twitter_api_key
   TWITTER_API_SECRET=your_twitter_api_secret
   TWITTER_BEARER_TOKEN=your_twitter_bearer_token
   TWITTER_ACCESS_TOKEN=your_twitter_access_token
   TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
   NEWS_API_KEY=your_news_api_key
   EMAIL_USER=your_email_address
   EMAIL_PASSWORD=your_email_password
   EMAIL_RECEIVER=receiver_email_address
   ```

## Deployment on PythonAnywhere

1. **Upload the Code**:
   - Zip your project folder and upload it to your PythonAnywhere account.
   - Extract the folder in your home directory.

2. **Set Up Virtual Environment**:
   - Open a Bash console and navigate to your project directory:
     ```bash
     cd ~/your_project_directory
     source venv/bin/activate
     ```
   - Install dependencies if not already installed:
     ```bash
     pip install -r requirements.txt
     ```

3. **Set Up Cron Job**:
   - Go to the "Tasks" tab in PythonAnywhere.
   - Add a new scheduled task with the following command:
     ```bash
     source ~/your_project_directory/venv/bin/activate && python ~/your_project_directory/twitter_bot.py
     ```
   - Set the task to run every hour.

4. **Cron Job Execution Issue**:
   - Note that PythonAnywhere's free tier has limitations on long-running tasks. If the script doesn't seem to run automatically after a certain period, you may need to manually execute the script daily.
   - Execute the script once each day before starting to ensure it runs hourly throughout the day:
     ```bash
     source ~/your_project_directory/venv/bin/activate
     python ~/your_project_directory/twitter_bot.py
     ```

## Notes

- Make sure to check the logs regularly for any errors or issues with the bot.
- If you encounter any rate limits or other Twitter API restrictions, consider upgrading your API plan or adjusting the bot's frequency of execution.

---
