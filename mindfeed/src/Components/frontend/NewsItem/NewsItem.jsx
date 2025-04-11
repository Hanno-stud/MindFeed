import { useState } from "react";
import PropTypes from "prop-types";
import SavedArticleIcon from "../../../assets/saved-article.png";
import UnsavedArticleIcon from "../../../assets/unsaved-article.png";
import { FaVolumeUp } from "react-icons/fa"; // Icon for text-to-speech
import "./NewsItem.css";

const NewsItem = ({ title, description, src, url, userId }) => {
  const [isSaved, setIsSaved] = useState(false); // Track save state
  const [loading, setLoading] = useState(false); // Add loading to prevent multiple clicks
  
  const toggleSaveArticle = async () => {
    setLoading(true); // Prevent multiple clicks
    const apiEndpoint = isSaved
      ? "http://localhost:5000/delete-article"
      : "http://localhost:5000/save-article";
      console.log("apiEndpoint: ", apiEndpoint);
      console.log("isSaved: ", isSaved);

    try {
      const response = await fetch(apiEndpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          userId,
          article: { title, description, src, url },
        }),
      });

      if (response.ok) {
        // Toggle the state only if the request was successful
        setIsSaved(!isSaved);
      } else {
        console.error("Failed to toggle save state.");
      }
    } catch (error) {
      console.error("Error toggling save state:", error.message);
    } finally {
      setLoading(false);
    }
  };
  
  const handleTextToSpeech = async (option) => {
    let textToSpeak = "";

    switch (option) {
      case "Title":
        textToSpeak = `Title: ${title}`;
        break;
      case "Description":
        textToSpeak = `Description: ${description || "No description available."}`;
        break;
      case "Content":
        textToSpeak = `Content: Full article content will be read after this.`;
        break;
      case "All":
        textToSpeak = `Title: ${title}. Description: ${
          description || "No description available."
        }. Content: Full article content will be read after this.`;
        break;
      default:
        return;
    }
    const apiUrl = "http://localhost:5000/text-to-speech";
    // Send the text to the Python program via a fetch request
    try {
      console.log("Sending request to:", apiUrl);
      console.log("Request body:", { text: textToSpeak });

      // Save the current state of the website
      // const previousState = window.location.href;

      // Send the text to the Python program via a fetch request to the Flask server
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: textToSpeak }),
      });

      if (response.ok) {
        console.log("Text sent to Python program successfully.");

        // Wait for the Python application to finish
        const result = await response.json();
        console.log("Response from Flask server:", result);
        if (result.status === "completed") {
          console.log("Text-to-speech process completed.");
          if (result.stdout) {
            console.log("Python application output:", result.stdout);
          }

          // Display the translated text (if available)
          if (result.translated_text) {
            console.log("Translated text:", result.translated_text);
          }

          // Restore the previous state of the website
          // window.location.href = previousState;
        } else {
          console.error("Text-to-speech process not completed when saving Website previousState: ");
        }
      } else {
        const errorData = await response.json();
        console.error("Failed to send text to Python program.", errorData);
        alert(`Error: ${errorData.message || "Unknown error occurred."}`);
      }
    } catch (error) {
      console.error("Error communicating with Flask Server: ", error.message);
      alert(`Error: ${error.message || "Failed to communicate with the server. Please try again later."}`);
    }
  };

  return (
    <div 
      className="card bg-dark text-light mb-3 d-inline-block my-3 mx-3 px-2 py-2" 
      style={{ maxWidth: "345px" }}>
      <img
        src={
          src
            ? src
            : "https://www.charleston-hub.com/wp-content/uploads/2021/01/news-pixabay-bW.jpg"
        }
        className="card-img-top"
        alt="..."
      />

      <div className="card-body">
        {/*   <h5 className="card-title">{title.slice(0, 50)}</h5>   */}
        <h5 className="card-title">{title}</h5>
        <p className="card-text">
          {description
            ? description.slice(0, 90)
            : "News current event. It is information about something that has just happened."}
        </p>
        <div className="news-actions">
          <a href={url} target="_blank" rel="noopener noreferrer" className="btn btn-primary read-more-btn">
            Read More
          </a>
          <img
            src={isSaved ? SavedArticleIcon : UnsavedArticleIcon}
            className={`save-article-icon ${loading ? "disabled" : ""}`}
            alt="Save Article"
            title={isSaved ? "Unsave Article" : "Save Article"}
            onClick={toggleSaveArticle}
          />
          <div className="dropdown">
            <FaVolumeUp className="text-to-speech-icon" title="Listen to Article" />
            <div className="dropdown-content">
              <button onClick={() => handleTextToSpeech("Title")}>Title</button>
              <button onClick={() => handleTextToSpeech("Description")}>Description</button>
              <button onClick={() => handleTextToSpeech("Content")}>Content</button>
              <button onClick={() => handleTextToSpeech("All")}>All of the above</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

NewsItem.propTypes = {
  title: PropTypes.string.isRequired,
  description: PropTypes.string,
  src: PropTypes.string,
  isSaved: PropTypes.bool.isRequired,
  toggleSaveArticle: PropTypes.func.isRequired,
  url: PropTypes.string.isRequired,
  userId: PropTypes.string, // Add userId for MongoDB actions
};

export default NewsItem;