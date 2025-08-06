import React from 'react';

const ResultsTable = ({ results }) => {
  if (!results) return null;

  return (
    <div className="results-container">
      <h3>Fare Calculation Results</h3>
      <table>
        <thead>
          <tr>
            <th>Trip</th>
            <th>From Zone</th>
            <th>To Zone</th>
            <th>Fare</th>
          </tr>
        </thead>
        <tbody>
          {results.trip_results.map((trip, index) => (
            <tr key={index}>
              <td>{index + 1}</td>
              <td>{trip.from_zone}</td>
              <td>{trip.to_zone}</td>
              <td>{trip.fare}</td>
            </tr>
          ))}
        </tbody>
        <tfoot>
          <tr>
            <td colSpan="3"><strong>Total Daily Fare</strong></td>
            <td><strong>{results.total_daily_fare}</strong></td>
          </tr>
        </tfoot>
      </table>
    </div>
  );
};

export default ResultsTable;