function Dashboard() {
  return (
    <div className="card">

      <h1>Dashboard</h1>

      <div className="dashboard-grid">

        <div className="dashboard-card">
          <h2>Docentes</h2>
          <h1>245</h1>
        </div>

        <div className="dashboard-card">
          <h2>Usuarios</h2>
          <h1>8</h1>
        </div>

        <div className="dashboard-card">
          <h2>Cargos</h2>
          <h1>12</h1>
        </div>

        <div className="dashboard-card">
          <h2>Roles</h2>
          <h1>4</h1>
        </div>

      </div>

    </div>
  );
}

export default Dashboard;