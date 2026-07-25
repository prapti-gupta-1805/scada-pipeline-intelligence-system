import { NavLink } from 'react-router-dom';
import { X } from 'lucide-react';
import { appName, navItems } from '../data/system';

export default function Sidebar({ open, onClose, health }) {
  const loadedModels = Object.values(health?.models ?? {}).filter(Boolean).length;
  const totalModels = Object.keys(health?.models ?? {}).length;
  const backendStatus = health?.status === 'ok' ? 'Operational' : health ? 'Degraded' : 'Checking';

  return (
    <>
      <div
        className={`fixed inset-0 z-30 bg-slate-950/40 transition-opacity duration-300 lg:hidden ${open ? 'opacity-100' : 'pointer-events-none opacity-0'}`}
        onClick={onClose}
      />
      <aside
        className={`fixed inset-y-0 left-0 z-40 w-80 border-r border-slate-800 bg-slate-950 text-slate-100 shadow-2xl shadow-slate-950/40 transition-transform duration-300 lg:translate-x-0 ${open ? 'translate-x-0' : '-translate-x-full'} lg:static lg:z-auto lg:flex lg:flex-col`}
      >
        <div className="flex items-center justify-between border-b border-slate-800 px-6 py-6">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.28em] text-sky-400">Industrial AI</p>
            <h2 className="mt-2 text-lg font-semibold tracking-tight text-white">{appName}</h2>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="inline-flex h-10 w-10 items-center justify-center rounded-2xl border border-slate-800 bg-slate-900 text-slate-300 transition hover:text-white lg:hidden"
            aria-label="Close navigation"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <div className="border-b border-slate-800 px-6 py-5">
          <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-4">
            <p className="text-xs font-semibold uppercase tracking-[0.24em] text-sky-400">System status</p>
            <div className="mt-3 flex items-center justify-between">
              <div>
                <p className="text-sm font-semibold text-white">Backend {backendStatus}</p>
                <p className="mt-1 text-sm text-slate-400">
                  {loadedModels} of {totalModels || 0} models loaded
                </p>
              </div>
              <span className={`rounded-full px-3 py-1 text-xs font-semibold ${health?.status === 'ok' ? 'bg-emerald-500/15 text-emerald-300' : 'bg-amber-500/15 text-amber-300'}`}>
                {health?.status === 'ok' ? 'Stable' : health ? 'Attention' : 'Waiting'}
              </span>
            </div>
          </div>
        </div>

        <nav className="flex-1 px-4 py-5">
          <div className="space-y-2">
            {navItems.map(({ to, label, icon: Icon, description }) => (
              <NavLink
                key={to}
                to={to}
                onClick={onClose}
                className={({ isActive }) => `group flex items-center gap-3 rounded-2xl px-4 py-3 transition ${isActive ? 'bg-white text-slate-950 shadow-lg shadow-white/10' : 'text-slate-300 hover:bg-slate-900 hover:text-white'}`}
              >
                <span className="rounded-xl border border-slate-800 bg-slate-900 p-2 text-slate-300 transition">
                  <Icon className="h-4 w-4" />
                </span>
                <span>
                  <span className="block text-sm font-semibold">{label}</span>
                  <span className="block text-xs text-slate-400 group-hover:text-slate-300">{description}</span>
                </span>
              </NavLink>
            ))}
          </div>
        </nav>

        <div className="border-t border-slate-800 p-5">
          <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-4 text-sm text-slate-300">
            <p className="text-xs font-semibold uppercase tracking-[0.24em] text-sky-400">Prepared for engineers</p>
            <p className="mt-2 leading-6 text-slate-400">
              Designed for operations teams who need fast triage, explainable predictions and a calm interface during incidents.
            </p>
          </div>
        </div>
      </aside>
    </>
  );
}
