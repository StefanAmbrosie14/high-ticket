import React from "react";
import { Link } from "react-router-dom";

function Dashboard() {
  return (
    <div>
      <h1>Admin Dashboard</h1>
      <ul>
        <li><Link to="/events">Manage Events</Link></li>
        <li><Link to="/orders">Manage Orders</Link></li>
      </ul>
    </div>
  );
}

export default Dashboard;
