// frontend/src/App.js

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import JourneyForm from './components/JourneyForm';
import './App.css';

// The base URL for all backend API calls.
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

function App() {
  // --- STATE MANAGEMENT ---
  // 'journeys' holds the list of journey objects. Each object will contain
  // from_zone, to_zone, and its calculated fare.
  const [journeys, setJourneys] = useState([]);
  
  // 'isLoading' is a boolean flag to track when an API call is in progress.
  // Used to show loading feedback in the UI (e.g., disable buttons).
  const [isLoading, setIsLoading] = useState(false);

  // 'error' holds any error message to be displayed to the user.
  const [error, setError] = useState('');

  // 'appConfig' stores configuration data fetched from the backend on load,
  // primarily the list of available zones for the dropdowns.
  const [appConfig, setAppConfig] = useState({ available_zones: [] });

  // 'useEffect' hook to fetch configuration from the backend when the app first loads.
  // The empty dependency array `[]` ensures this runs only once.
  useEffect(() => {
    const fetchConfig = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/config`);
        setAppConfig(response.data);
      } catch (err) {
        setError('Failed to load configuration from server.');
      }
    };
    fetchConfig();
  }, []);

  // --- EVENT HANDLERS ---

  /**
   * Handles adding a new journey. This is an async function because it
   * makes an API call to fetch the fare for the new journey in real-time.
   */
  const handleAddJourney = async (journey) => {
    setIsLoading(true);
    setError('');
    try {
      // Step 1: Call the `/fare` endpoint to get the fare for this single journey.
      const response = await axios.get(`${API_BASE_URL}/fare`, {
        params: {
          from_zone: journey.from_zone,
          to_zone: journey.to_zone,
        },
      });

      // Step 2: Create a new journey object that includes the fetched fare.
      const journeyWithFare = { ...journey, fare: response.data.fare };
      // Add the complete journey object to the state array.
      setJourneys([...journeys, journeyWithFare]);

    } catch (err) {
      setError('Could not calculate fare for this journey.');
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Handles deleting a journey from the list using its index.
   */
  const handleDeleteJourney = (journeyIndexToRemove) => {
    // Creates a new array that excludes the item at the specified index.
    const updatedJourneys = journeys.filter((_, index) => index !== journeyIndexToRemove);
    setJourneys(updatedJourneys);
  };

  /**
   * Resets the application state, clearing all journeys and errors.
   */
  const handleReset = () => {
    setJourneys([]);
    setError('');
  };

  // --- DERIVED STATE ---
  // The total fare is now calculated directly from the 'journeys' state array
  // using the .reduce() method. This is more efficient than storing it in a separate state.
  const totalFare = journeys.reduce((total, journey) => total + journey.fare, 0);

  // --- RENDER LOGIC ---
  return (
    <div className="App">
      <header className="App-header">
        <h1>PearlCard Fare Calculator</h1>
      </header>
      <main>
        <JourneyForm
          onAddJourney={handleAddJourney}
          journeyCount={journeys.length}
          availableZones={appConfig.available_zones}
          isLoading={isLoading} 
        />
        
        <div className="journeys-list">
          <h4>Your Daily Journeys ({journeys.length})</h4>

          {/* Display a header row for the list only if there are journeys */}
          {journeys.length > 0 && (
            <div className="journey-item list-header">
              <span>Journey</span>
              <span className="fare-header">Fare</span>
              <span></span> 
            </div>
          )}

          <ul>
            {journeys.length > 0 ? (
              // Map over the journeys array to render each trip as a list item
              journeys.map((j, index) => (
                <li key={index} className="journey-item">
                  <span>{`Trip ${index + 1}: Zone ${j.from_zone} → Zone ${j.to_zone}`}</span>
                  
                  {/* The fare is now always present on the journey object */}
                  <span className="fare-display">{j.fare}</span>
                  
                  <button
                    onClick={() => handleDeleteJourney(index)}
                    className="delete-journey-button"
                    title="Delete this journey"
                  >
                    &times; 
                  </button>
                </li>
              ))
            ) : (
              // Display a message if no journeys have been added yet
              <li>No journeys added yet.</li>
            )}
          </ul>

          {/* Display the total fare container only if there are journeys */}
          {journeys.length > 0 && (
            <div className="total-fare-container journey-item">
              <span><strong>Total Daily Fare</strong></span>
              <span className="fare-display total-value">{totalFare}</span>
              {/* Empty span placeholder to maintain grid alignment with the delete button column */}
              <span></span>
            </div>
          )}
        </div>

        {/* The main action buttons */}
        <div className="controls">
          <button onClick={handleReset} className="reset-button">Reset</button>
        </div>
        
        {/* Display any error message */}
        {error && <p className="error">{error}</p>}
      </main>
    </div>
  );
}

export default App;