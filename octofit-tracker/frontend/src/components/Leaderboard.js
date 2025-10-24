import React, { useEffect, useState } from 'react';

const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/leaderboard/`;

function Leaderboard() {
  const [entries, setEntries] = useState([]);
  useEffect(() => {
    console.log('Fetching leaderboard from:', API_URL);
    fetch(API_URL)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setEntries(results);
        console.log('Fetched leaderboard:', results);
      })
      .catch(err => console.error('Error fetching leaderboard:', err));
  }, []);
  return (
    <div>
      <h2>Leaderboard</h2>
      <ul>
        {entries.map((e, i) => (
          <li key={e.id || i}>{e.team?.name || 'Team'}: {e.points} pts</li>
        ))}
      </ul>
    </div>
  );
}
export default Leaderboard;
