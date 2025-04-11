import { useState } from "react";
import { HelmetProvider, Helmet } from "react-helmet-async";
import NewsBoard from "./Components/frontend/NewsBoard/NewsBoard";
import Navbar from "./Components/frontend/NavBar/Navbar";
import WebsiteLogo from "./assets/mindfeed_logo.png";

const App = () => {
  const [category, setCategory] = useState("general");
  return (
    <>
      <HelmetProvider>
        <Helmet>
        <title>MindFeed</title>
          <link rel="icon" href={WebsiteLogo} />
        </Helmet>
        <div>
          <Navbar setCategory={setCategory} />
          <NewsBoard category={category} />
        </div>
      </HelmetProvider>
    </>
  );
};

export default App;