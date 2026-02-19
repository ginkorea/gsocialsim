import { NavLink } from 'react-router-dom'
import { cn } from '@/lib/utils'
import {
  LayoutDashboard,
  Settings2,
  Play,
  FlaskConical,
  BarChart3,
} from 'lucide-react'

const navItems = [
  { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/config', icon: Settings2, label: 'Configure' },
  { to: '/simulate', icon: Play, label: 'Simulate' },
  { to: '/tune', icon: FlaskConical, label: 'Tune' },
  { to: '/results', icon: BarChart3, label: 'Results' },
]

export function Sidebar() {
  return (
    <aside className="w-16 lg:w-56 h-screen flex flex-col border-r border-border bg-card/50 backdrop-blur-sm">
      <div className="p-4 flex items-center gap-2">
        <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center text-white font-bold text-sm">
          G
        </div>
        <span className="hidden lg:block font-semibold text-sm tracking-tight">
          gsocialsim
        </span>
      </div>
      <nav className="flex-1 px-2 py-4 space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              cn(
                'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200',
                isActive
                  ? 'bg-primary/15 text-primary'
                  : 'text-muted-foreground hover:bg-accent hover:text-foreground'
              )
            }
          >
            <item.icon className="w-5 h-5 shrink-0" />
            <span className="hidden lg:block">{item.label}</span>
          </NavLink>
        ))}
      </nav>
      <div className="p-4 border-t border-border">
        <div className="hidden lg:block text-xs text-muted-foreground">
          v0.1.0
        </div>
      </div>
    </aside>
  )
}
