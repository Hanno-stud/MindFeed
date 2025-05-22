import { useEffect, useState } from "react";
import NewsItem from "../NewsItem/NewsItem";
import PropTypes from "prop-types";
import "./NewsBoard.css";

const NewsBoard = ({ category }) => {
  const [articles, setArticles] = useState([]);
  const [error, setError] = useState(null);
  const [fetchMode, setFetchMode] = useState("API"); // "API" or "RSS"
  const [rssFilter, setRssFilter] = useState("Source"); // "Source", "Location", "Category"
  const [rssFeedData, setRssFeedData] = useState([]);
  const [filteredArticles, setFilteredArticles] = useState([]);

  const rssFeeds = {
    // Indian News Channels
    "Aaj Tak": "https://www.aajtak.in/rssfeeds?id=home",
    "India TV": "https://www.indiatvnews.com/rssnews/topstory.xml",
    "Times of India": "https://timesofindia.indiatimes.com/rssfeeds/1221656.cms",
    "NDTV India": "https://feeds.feedburner.com/ndtvnews-top-stories",
    "ABP News": "https://news.abplive.com/home/feed",
    "Zee News": "	https://zeenews.india.com/rss/india-national-news.xml",
    // World News Channels
    "BBC News": "https://feeds.bbci.co.uk/news/rss.xml",
    "The New York Times": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "Fox News": "https://moxie.foxnews.com/google-publisher/latest.xml",
    "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "The Guardian": "https://www.theguardian.com/international/rss",
    "Bloomberg": "https://feeds.megaphone.fm/BLM1892394744",
    "The Wall Street Journal": "https://feeds.content.dowjones.io/public/rss/RSSWSJD",
    "France 24": "https://www.france24.com/en/rss"
  };

  // Fetch news content via API
  useEffect(() => {
    if (fetchMode === "API") {
      const url = `https://newsapi.org/v2/top-headlines?country=us&category=${category}&apiKey=${import.meta.env.VITE_API_KEY}`;
      fetch(url)
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          if (data.articles) {
            setArticles(data.articles);
          } else {
            setError("No articles found");
          }
        })
        .catch((error) => {
          setError(error.message);
        });
    }
  }, [category, fetchMode]);

  // Fetch news content via RSS Feeds
  useEffect(() => {
    if (fetchMode === "RSS") {
      const fetchRSSFeeds = async () => {
        try {
          const allArticles = [];
          for (const [source, url] of Object.entries(rssFeeds)) {
            const response = await fetch(url);
            const text = await response.text();
            const parser = new DOMParser();
            const xml = parser.parseFromString(text, "application/xml");
            const items = xml.querySelectorAll("item");

            items.forEach((item) => {
              const title = item.querySelector("title")?.textContent || "No Title";
              const description =
                item.querySelector("description")?.textContent || "No Description";
              const link = item.querySelector("link")?.textContent || "#";
              const pubDate = item.querySelector("pubDate")?.textContent || "Unknown Date";
              console.log("RSS DataFields fetched:", { title, description, link, pubDate });
              allArticles.push({
                source,
                title,
                description,
                link,
                pubDate,
              });
            });
          }
          setRssFeedData(allArticles);
          setFilteredArticles(allArticles); // Default to all articles
        } catch (error) {
          setError("Failed to fetch RSS feeds");
        }
      };

      fetchRSSFeeds();
    }
  }, [fetchMode]);

  // Filter RSS feed articles based on the selected filter
  useEffect(() => {
    if (fetchMode === "RSS") {
      let filtered = [...rssFeedData];
      if (rssFilter === "Source") {
        filtered.sort((a, b) => a.source.localeCompare(b.source));
      } else if (rssFilter === "Location") {
        // Example: Filter by location (if location data is available in the RSS feed)
        filtered = filtered.filter((article) =>
          article.description.toLowerCase().includes("india")
        );
      } else if (rssFilter === "Category") {
        // Example: Filter by category (if category data is available in the RSS feed)
        filtered = filtered.filter((article) =>
          article.description.toLowerCase().includes(category.toLowerCase())
        );
      }
      setFilteredArticles(filtered);
    }
  }, [rssFilter, rssFeedData, category, fetchMode]);

  if (error) {
    return <div>Error: {error}</div>;
  }

  const toggleSaveArticle = (article) => {
    setSavedArticles((prevSavedArticles) => {
      // Check if the article is already saved
      const isAlreadySaved = prevSavedArticles.some((saved) => saved.url === article.url);
      if (isAlreadySaved) {
        // Remove the article from savedArticles
        return prevSavedArticles.filter((saved) => saved.url !== article.url);
      } else {
        // Add the article to savedArticles
        return [...prevSavedArticles, article];
      }
    });
  };

  if (error) {
    return <div>Error: {error}</div>;
  }
  

  return (
    <div>
      <h2 className="text-center">
        Latest <span className="badge bg-danger">News</span>
      </h2>

      {/* Fetch Mode Selector */}
      <div className="fetch-mode-selector">
        <button
          className={`btn ${fetchMode === "API" ? "btn-primary" : "btn-secondary"}`}
          onClick={() => setFetchMode("API")}
        >
          Fetch via API
        </button>
        <button
          className={`btn ${fetchMode === "RSS" ? "btn-primary" : "btn-secondary"}`}
          onClick={() => setFetchMode("RSS")}
        >
          Fetch via RSS Feeds
        </button>
      </div>

      {/* RSS Feed Filter Dropdown */}
      {fetchMode === "RSS" && (
        <div className="rss-filter-dropdown">
          <label htmlFor="rssFilter">Filter By:</label>
          <select
            id="rssFilter"
            value={rssFilter}
            onChange={(e) => setRssFilter(e.target.value)}
          >
            <option value="/">Select any 1--</option>
            <option value="Source">Source</option>
            <option value="Location">Location</option>
            <option value="Category">Category</option>
          </select>
        </div>
      )}

      {/* Display Articles */}
      {fetchMode === "API" && articles.length > 0 ? (
        articles.map((news, index) => (
          <NewsItem
            key={index}
            title={news.title}
            description={news.description}
            src={news.urlToImage}
            url={news.url}
          />
        ))
      ) : fetchMode === "RSS" && filteredArticles.length > 0 ? (
        filteredArticles.map((news, index) => (
          <NewsItem
            key={index}
            title={news.title}
            description={news.description}
            src={null} // RSS feeds may not have images
            url={news.link}
          />
        ))
      ) : (
        <div>No news articles available</div>
      )}
    </div>
  );
};

NewsBoard.propTypes = {
  category: PropTypes.string.isRequired,
};

export default NewsBoard;