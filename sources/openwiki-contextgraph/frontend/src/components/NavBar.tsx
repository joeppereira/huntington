import { NavLink } from 'react-router'

interface NavBarProps {
  backendError: string | null
}

const linkClass = ({ isActive }: { isActive: boolean }) => (isActive ? 'nav__link nav__link--active' : 'nav__link')

export function NavBar({ backendError }: NavBarProps) {
  return (
    <header className="nav">
      <span className="nav__brand">MHFC · OpenWiki graphs</span>
      <nav className="nav__links">
        <NavLink to="/semantic" className={linkClass}>
          Semantic Graph
        </NavLink>
        <NavLink to="/agent" className={linkClass}>
          Agent &amp; Memory
        </NavLink>
      </nav>
      {backendError ? (
        <span className="nav__status nav__status--error" title={backendError}>
          Backend not reachable, retrying…
        </span>
      ) : null}
    </header>
  )
}
