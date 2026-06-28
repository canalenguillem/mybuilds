import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import ProtectedRoute from './components/auth/ProtectedRoute'
import LoginPage from './pages/LoginPage'
import Dashboard from './pages/Dashboard'
import Placeholder from './pages/Placeholder'
import TemplatesPage from './pages/Templates/TemplatesPage'
import TemplateBuilder from './pages/Templates/TemplateBuilder'
import SubmittalsPage from './pages/Submittals/SubmittalsPage'
import CompliancePage from './pages/Compliance/CompliancePage'

const protect = (el) => <ProtectedRoute>{el}</ProtectedRoute>

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/" element={protect(<Dashboard />)} />
          <Route path="/templates" element={protect(<TemplatesPage />)} />
          <Route path="/templates/new" element={protect(<TemplateBuilder />)} />
          <Route path="/templates/:id/edit" element={protect(<TemplateBuilder />)} />
          <Route path="/documents" element={protect(<Placeholder title="Documents" />)} />
          <Route path="/submittals" element={protect(<SubmittalsPage />)} />
          <Route path="/compliance" element={protect(<CompliancePage />)} />
          <Route path="/analytics" element={protect(<Placeholder title="Analytics" />)} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}
