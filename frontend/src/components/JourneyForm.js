import React, { useState, useEffect } from 'react';

const JourneyForm = ({ onAddJourney, journeyCount, availableZones = [],isLoading }) => {
  const [fromZone, setFromZone] = useState(1);
  const [toZone, setToZone] = useState(1);

  useEffect(() => {
    if (availableZones.length > 0) {
      setFromZone(availableZones[0]);
      setToZone(availableZones[0]);
    }
  }, [availableZones]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (journeyCount < 20) {
      onAddJourney({ from_zone: fromZone, to_zone: toZone });
    }
  };

  if (availableZones.length === 0) {
    return <p>Loading zone configuration...</p>;
  }
  
  return (
    <form onSubmit={handleSubmit} className="journey-form">
      <h3>Add a Journey (Max 20)</h3>
      <div className="form-group">
      <label htmlFor="from-zone-select">From Zone: </label>
        <select id="from-zone-select" value={fromZone} onChange={(e) => setFromZone(Number(e.target.value))}>
          {availableZones.map(z => <option key={`from-${z}`} value={z}>Zone {z}</option>)}
        </select>
      </div>
      <div className="form-group">
      <label htmlFor="to-zone-select">To Zone: </label>
        <select  id="to-zone-select" value={toZone} onChange={(e) => setToZone(Number(e.target.value))}>
          {availableZones.map(z => <option key={`to-${z}`} value={z}>Zone {z}</option>)}
        </select>
      </div>
      <button type="submit" disabled={journeyCount >= 20 || isLoading}>
        {isLoading ? 'Adding...' : 'Add Journey'}
      </button>
       {journeyCount >= 20 && <p className="error">Daily limit of 20 journeys reached.</p>}
    </form>
  );
};

export default JourneyForm;