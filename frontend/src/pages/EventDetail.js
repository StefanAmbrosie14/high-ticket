import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

function EventDetail() {
  const { id } = useParams();
  const [event, setEvent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get(`http://127.0.0.1:8000/api/events/${id}/`)
      .then(response => {
        setEvent(response.data);
        setLoading(false);
      })
      .catch(error => {
        setError("Failed to load event details");
        setLoading(false);
      });
  }, [id]);

  if (loading) return <p>Loading event details...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div>
      <h1>{event.title}</h1>
      <p><strong>Date:</strong> {event.start_date}</p>
      <p><strong>Location:</strong> {event.location}</p>
      <p>{event.description}</p>
    </div>
  );
}

export default EventDetail;
