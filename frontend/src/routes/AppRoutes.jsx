// src/routes/AppRoutes.jsx

import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

// Páginas
import Login from '../pages/auth/Login';
import Dashboard from '../pages/dashboard/Dashboard';
import CustomerList from '../pages/customers/CustomerList';
{/*import CustomerForm from '../pages/customers/CustomerForm';
import CustomerDetail from '../pages/customers/CustomerDetail';
import ProcessList from '../pages/processes/ProcessList';
import DeadlineList from '../pages/deadlines/DeadlineList';
import DocumentList from '../pages/documents/DocumentList';
import FinanceList from '../pages/finance/FinanceList';*/}

// Layout
import Layout from '../components/layout/Layout';
import ProtectedRoute from './ProtectedRoute';

const AppRoutes = () => {
  const { isAuthenticated } = useAuth();

  return (
    <BrowserRouter>
      <Routes>
        {/* Rota pública - Login */}
        <Route 
          path="/login" 
          element={
            isAuthenticated ? <Navigate to="/dashboard" replace /> : <Login />
          } 
        />

        {/* Rotas protegidas */}
        <Route
          path="/*"
          element={
            <ProtectedRoute>
              <Layout>
                <Routes>
                  {/* Dashboard */}
                  <Route path="/dashboard" element={<Dashboard />} />

                  {/* Customers */}
                  <Route path="/customers" element={<CustomerList />} />
                  <Route path="/customers/new" element={<CustomerForm />} />
                  <Route path="/customers/:id" element={<CustomerDetail />} />
                  <Route path="/customers/:id/edit" element={<CustomerForm />} />

                  {/* Processes */}
                  <Route path="/processes" element={<ProcessList />} />

                  {/* Deadlines */}
                  <Route path="/deadlines" element={<DeadlineList />} />

                  {/* Documents */}
                  <Route path="/documents" element={<DocumentList />} />

                  {/* Finance */}
                  <Route path="/finance" element={<FinanceList />} />

                  {/* Redirect root to dashboard */}
                  <Route path="/" element={<Navigate to="/dashboard" replace />} />
                  
                  {/* 404 */}
                  <Route path="*" element={<Navigate to="/dashboard" replace />} />
                </Routes>
              </Layout>
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
};

export default AppRoutes;