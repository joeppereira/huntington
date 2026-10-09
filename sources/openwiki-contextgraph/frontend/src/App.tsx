import { Navigate, useLocation } from 'react-router'
import { NavBar } from './components/NavBar'
import { useBackendConfig } from './hooks/useBackendConfig'
import { AgentPage } from './pages/AgentPage'
import { SemanticGraphPage } from './pages/SemanticGraphPage'

const ROUTES = ['/semantic', '/agent'] as const

/**
 * Both pages stay mounted and the inactive one is hidden, so switching routes never reloads the
 * OpenWiki visualizer iframes (BUILD_SPEC 8.6).
 */
export default function App() {
  const { pathname } = useLocation()
  const { config, error } = useBackendConfig()

  if (!ROUTES.some((route) => pathname === route)) {
    return <Navigate to="/semantic" replace />
  }

  return (
    <div className="app">
      <NavBar backendError={error} />
      <SemanticGraphPage config={config} hidden={pathname !== '/semantic'} />
      <AgentPage config={config} hidden={pathname !== '/agent'} />
    </div>
  )
}
