// src/pages/dashboard/Dashboard.jsx

const Dashboard = () => {
  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Cards de estatísticas - placeholder */}
        {[
          { title: 'Clientes', value: '0', color: 'blue' },
          { title: 'Processos', value: '0', color: 'green' },
          { title: 'Prazos Hoje', value: '0', color: 'yellow' },
          { title: 'Documentos', value: '0', color: 'purple' },
        ].map((stat) => (
          <div key={stat.title} className="bg-white rounded-lg shadow p-6">
            <h3 className="text-gray-600 text-sm font-medium mb-2">{stat.title}</h3>
            <p className="text-3xl font-bold text-gray-900">{stat.value}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;