# MindFeed 
<!-- <img src="https://github.com/user-attachments/assets/dca2de93-82b4-43ee-8235-e1ddcc4902ca" alt="Mind" width="120" height="auto"/> -->
<!-- MindFeed logo -->
MindFeed is a full-stack, AI-powered personalized news aggregation platform designed to revolutionize how users consume news.I It's mission is to offer an intelligent, bias-mitigated news experience. Its built using React JS, PHP, Bootstrap, Python and optionally MongoDB for strong user preference, MindFeed emphasizes integrity in content delivery. Its designed to provide users with the latest news articles based on different categories.<br/>
At it's core, MindFeed integrates <b>RSS Feeds</b> from trusted national and regional news channels, dynamically fetching and displaying live content accross categories such as <i>Technology, Busines, Sports, and Entertainment</i>. Instead of storing articles redudantly, MindFeed fetches data on demand, ensuring accuracy, performance and freshness of content.
Optionally, it also fetches news content using <b>News API</b>. This provides the user with option to select the medium of news content based on personal interests.

## Features
- Selective medium of news extraction: <b>RSS Feeds</b> or <b>News API</b>
- Category Selection: Users can choose from various news categories such as business, entertainment, health, science, sports, technology, etc.
- Latest News: Displays the latest news articles based on the selected category.
- Responsive Design: Built with Bootstrap, ensuring a responsive and mobile-friendly layout.
- Read More: Provides a link to read the full article on the news source's website.
- AI-Powered Text-to-Speech Functionality: Reads out title, description or news content to the user


## Installation
- Clone the repository: git clone [https://github.com/Hanno-stud/MindFeed.git](https://github.com/Hanno-stud/MindFeed.git)

## Usage
Collect RSS Feeds link from various news platforms(eg: BBC News, Times, Herald, Times of India, Economic Times, etc), parse and extract news content
Obtain an API key from News API and set it in your environment variables or directly in the code.

## Configuration(for API Key)
API Key: Obtain an API key from News API and set it in the src/config.js file or use environment variables for security.

## Technologies Used
- React JS
- Bootstrap
- News API
- Python
- PHP

## Significance of RSS Feeds over API-based news extraction
<b>RSS Feeds</b> functionality are provided by almost every <u>major and established news platforms</u>. News content extracted using APIs are always limited, and are not very flexible to categories and details like location, content, origin of news(News provider platform).
In such a case, RSS Feeds plays an important role in extracting Top Headlines news articles daily. This way, we can also get details about the news like the links, images or videos provided along with the main news content.
We can extract all the necessary information as per our need.

Few examples of News Feeds of various News Platforms are:

## Future Upgrades
- [ ] Integrating Email Newsletter functionality; it offers:<br/>
      1. who wish to get regularly sent email containing news, updates, and other valuable content delivered to a list of subscribers<br/>
      2. email to our Email ID (for@example.com) and get summarized news contents of the day<br/>
- [ ] Adding features: <pre>'Like', 'Share', 'Subscribe' and 'Comment'</pre>('Subscribe' to their favourite News Channel, to get more news stories from that news channel).
- [ ] Emotionally aware news experience that is tailored to each user's interests
- [ ] Personalization for each user interests based on read news articles
- [ ] 'Add to reading list' feature: to check out favourite news stories to be read later
- [ ] Offline availablility: Storing more user data locally for viewing locally, while offline(such as news stories marked under 'Reading' list )
