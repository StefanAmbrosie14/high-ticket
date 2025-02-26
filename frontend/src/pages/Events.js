import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

function Events() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/api/events/")
      .then(response => {
        setEvents(response.data);  // Store events from API
        setLoading(false);
      })
      .catch(error => {
        setError("Failed to load events");
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading events...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div>
      <h1>Events</h1>
      <ul>
        {events.map(event => (
          <li key={event.id}>
            <Link to={`/events/${event.id}`}>{event.title} - {event.start_date}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Events;
