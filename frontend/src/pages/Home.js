import React from "react";
import { Link } from "react-router-dom";

function Home() {
  return (
    <div>
      <h1>Welcome to High Ticket</h1>
      <p>The best ticketing solution for premium events.</p>
      <Link to="/login">Login</Link>
    </div>
  );
}

export default Home;
