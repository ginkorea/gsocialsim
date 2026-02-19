import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Layout } from '@/components/layout/Layout'
import { Dashboard } from '@/pages/Dashboard'
import { ConfigPage } from '@/pages/ConfigPage'
import { SimulationPage } from '@/pages/SimulationPage'
import { TuningPage } from '@/pages/TuningPage'
import { ResultsPage } from '@/pages/ResultsPage'

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/config" element={<ConfigPage />} />
          <Route path="/simulate" element={<SimulationPage />} />
          <Route path="/tune" element={<TuningPage />} />
          <Route path="/results" element={<ResultsPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}
