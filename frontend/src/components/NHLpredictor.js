import React, { useState } from "react";
import Animate from "react-smooth";
import iceRink from "../assets/ice_rink_bg.jpg";

function NhlPredictor() {
  const [visitorTeam, setVisitorTeam] = useState("");
  const [homeTeam, setHomeTeam] = useState("");
  const [prediction, setPrediction] = useState("");
  const [visitorStats, setVisitorStats] = useState({});
  const [homeStats, setHomeStats] = useState({});
  const [explanation, setExplanation] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!visitorTeam || !homeTeam) {
      setErrorMessage("Please select both teams before making a prediction.");
      return;
    }

    setErrorMessage("");
    setIsLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          visitor_team: visitorTeam,
          home_team: homeTeam,
        }),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }

      const data = await response.json();
      setPrediction(data.prediction);
      setVisitorStats(data.visitor_stats);
      setHomeStats(data.home_stats);
      setExplanation(data.explanation);
    } catch (error) {
      console.error("Error fetching prediction:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const teams = [
    "Boston Bruins",
    "Washington Capitals",
    "Chicago Blackhawks",
    "Detroit Red Wings",
    "New York Rangers",
    "Toronto Maple Leafs",
    "Montreal Canadiens",
    "Vancouver Canucks",
    "Calgary Flames",
    "Edmonton Oilers",
    "Ottawa Senators",
    "Winnipeg Jets",
    "Philadelphia Flyers",
    "Pittsburgh Penguins",
    "St. Louis Blues",
    "Colorado Avalanche",
    "San Jose Sharks",
    "Los Angeles Kings",
    "Anaheim Ducks",
    "Arizona Coyotes",
    "Buffalo Sabres",
    "Carolina Hurricanes",
    "Columbus Blue Jackets",
    "Dallas Stars",
    "Florida Panthers",
    "Minnesota Wild",
    "Nashville Predators",
    "New Jersey Devils",
    "New York Islanders",
    "Tampa Bay Lightning",
    "Vegas Golden Knights",
    "Seattle Kraken",
  ];

  return (
    <div
      className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center"
      style={{
        backgroundImage: `url(${iceRink})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}
    >
      <header className="bg-gray-800 py-4 w-full text-center">
        <h1 className="text-4xl font-bold">NHL Game Outcome Predictor</h1>
        <p className="text-gray-400 mt-2 font-bold">
          Select two teams and the model will predict the winner based on
          statistics from the past twelve NHL seasons.
        </p>
      </header>
      <main className="flex-grow flex items-center justify-center w-full px-4">
        <div className="bg-gray-800 p-8 rounded-lg shadow-lg max-w-md w-full">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label
                htmlFor="visitor-team"
                className="block text-sm font-medium text-lg text-gray-300"
              >
                Select Visitor Team
              </label>
              <select
                id="visitor-team"
                value={visitorTeam}
                onChange={(e) => setVisitorTeam(e.target.value)}
                className="mt-1 block w-full bg-gray-700 border border-gray-600 rounded-md text-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 text-gray-300 cursor-pointer"
              >
                <option value="" disabled>
                  Select Visitor Team
                </option>
                {teams.map((team) => (
                  <option key={team} value={team}>
                    {team}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label
                htmlFor="home-team"
                className="block text-sm font-medium text-lg text-gray-300"
              >
                Select Home Team
              </label>
              <select
                id="home-team"
                value={homeTeam}
                onChange={(e) => setHomeTeam(e.target.value)}
                className="mt-1 block w-full bg-gray-700 border border-gray-600 text-lg rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 text-gray-300 cursor-pointer"
              >
                <option value="" disabled>
                  Select Home Team
                </option>
                {teams.map((team) => (
                  <option key={team} value={team}>
                    {team}
                  </option>
                ))}
              </select>
            </div>
            {errorMessage && (
              <div className="text-red-500 text-center">{errorMessage}</div>
            )}
            <div>
              <button
                type="submit"
                className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 rounded-md text-white font-medium"
              >
                Predict Outcome
              </button>
            </div>
          </form>
          {isLoading && <div className="mt-4 text-center">Loading...</div>}
          <Animate
            to="1"
            from="0"
            attributeName="opacity"
            canBegin={prediction}
            duration={1000}
          >
            <section id="results" className="mt-8">
              {!isLoading && prediction && (
                <>
                  <h2 className="text-2xl font-bold text-center">
                    Prediction Result:
                  </h2>
                  <p
                    id="prediction"
                    className="text-center text-xl font-semibold mt-4"
                  >
                    {prediction}
                  </p>
                  <div className="mt-8">
                    <h2 className="text-2xl font-bold text-center">
                      Statistical Breakdown:
                    </h2>
                    <p id="visitor-stats" className="mt-2">
                      {visitorTeam} Average Goals Scored:{" "}
                      {visitorStats.visitor_goals_avg}, Allowed:{" "}
                      {visitorStats.visitor_allowed_avg}
                    </p>
                    <p id="home-stats" className="mt-2">
                      {homeTeam} Average Goals Scored:{" "}
                      {homeStats.home_goals_avg}, Allowed:{" "}
                      {homeStats.home_allowed_avg}
                    </p>

                    <h2 className="text-2xl font-bold text-center mt-8">
                      Explanation:
                    </h2>
                    <p id="explanation" className="mt-2">
                      {explanation}
                    </p>
                  </div>
                </>
              )}
            </section>
          </Animate>
        </div>
      </main>
      <footer className="bg-gray-800 py-4 text-center w-full">
        <p className="text-gray-500">
          2024 NHL Predictor Project made by Colin Cook.
        </p>
      </footer>
    </div>
  );
}

export default NhlPredictor;
