import { NavLink, Outlet } from 'react-router-dom';
import { Activity, AlertTriangle, BarChart3, Cpu, Gauge, LayoutGrid, ShieldCheck, Sparkles } from 'lucide-react';

const navigation = [
  { to: '/', label: 'Dashboard', icon: LayoutGrid },
  { to: '/fault', label: 'Fault Classification', icon: AlertTriangle },
  { to: '/anomaly', label: 'Anomaly Detection', icon: ShieldCheck },
  { to: '/maintenance', label: 'Predictive Maintenance', icon: Cpu },
  { to: '/analytics', label: 'Analytics', icon: BarChart3 },
];

export default function Layout() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto flex max-w-7xl flex-col px-4 py-4 lg:flex-row lg:px-6">
        <aside className="mb-4 w-full rounded-2xl border border-slate-800/80 bg-slate-900/80 p-4 shadow-2xl shadow-black/20 backdrop-blur lg:sticky lg:top-4 lg:mb-0 lg:w-72 lg:self-start">
          <div className="flex items-center gap-3 border-b border-slate-800 pb-4">
            <div className="rounded-xl border border-cyan-500/30 bg-cyan-500/10 p-2 text-cyan-300">
              <Gauge className="h-5 w-5" />
            </div>
            <div>
              <p className="text-sm font-semibold text-white">SCADA Intelligence</p>
              <p className="text-xs text-slate-400">Industrial monitoring suite</p>
            </div>
          </div>

          <nav className="mt-6 space-y-2">
            {navigation.map(({ to, label, icon: Icon }) => (
              <NavLink
                key={to}
                to={to}
                className={({ isActive }) =>
                  `flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition ${
                    isActive ? 'bg-cyan-500/15 text-cyan-300 shadow-inner' : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                  }`
                }
              >
                <Icon className="h-4 w-4" />
                {label}
              </NavLink>
            ))}
          </nav>

          <div className="mt-6 rounded-2xl border border-emerald-500/20 bg-emerald-500/10 p-4">
            <div className="flex items-center gap-2 text-sm font-semibold text-emerald-300">
              <Activity className="h-4 w-4" />
              System active
            </div>
            <p className="mt-2 text-sm text-slate-300">Real-time telemetry and ML predictions are available through the connected backend.</p>
          </div>
        </aside>

        <main className="flex-1 lg:pl-4">
          <header className="mb-4 rounded-2xl border border-slate-800/80 bg-slate-900/70 px-5 py-4 shadow-xl shadow-black/20 backdrop-blur">
            <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
              <div>
                <p className="text-sm uppercase tracking-[0.28em] text-cyan-400">Operations center</p>
                <h1 className="text-2xl font-semibold text-white">Pipeline intelligence dashboard</h1>
              </div>
              <div className="flex items-center gap-2 rounded-full border border-slate-700 bg-slate-800/70 px-3 py-2 text-sm text-slate-300">
                <Sparkles className="h-4 w-4 text-cyan-400" />
                Connected to FastAPI backend
              </div>
            </div>
          </header>

          <Outlet />
        </main>
      </div>
    </div>
  );
}
