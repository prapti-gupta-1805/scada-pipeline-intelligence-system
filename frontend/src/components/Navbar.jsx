import { Menu, Gauge } from 'lucide-react';
import { useState } from 'react';
import { NavLink, Link } from 'react-router-dom';
import { appName, navItems } from '../data/system';

export default function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-40 border-b border-slate-800/80 bg-slate-950/95 shadow-sm shadow-black/20 backdrop-blur-xl">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between gap-4 px-4 sm:px-6 lg:px-8">
        <Link to="/" className="inline-flex items-center gap-3 rounded-2xl bg-slate-900/70 px-3 py-2 text-sm font-semibold text-white transition hover:bg-slate-900">
          <span className="inline-flex h-9 w-9 items-center justify-center rounded-2xl bg-cyan-500/10 text-cyan-300">
            <Gauge className="h-5 w-5" />
          </span>
          <span>{appName}</span>
        </Link>

        <nav className="hidden flex-1 items-center justify-center gap-2 md:flex">
          {navItems.map(({ to, label }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `rounded-full px-4 py-2 text-sm font-medium transition ${
                  isActive ? 'bg-cyan-500/15 text-cyan-300 shadow-inner' : 'text-slate-300 hover:bg-slate-900 hover:text-white'
                }`
              }
            >
              {label}
            </NavLink>
          ))}
        </nav>

        <button
          type="button"
          onClick={() => setMenuOpen((open) => !open)}
          className="inline-flex h-10 w-10 items-center justify-center rounded-xl border border-slate-800 bg-slate-900 text-slate-300 transition hover:border-slate-700 hover:text-white md:hidden"
          aria-expanded={menuOpen}
          aria-label="Toggle navigation"
        >
          <Menu className="h-5 w-5" />
        </button>
      </div>

      {menuOpen && (
        <div className="border-t border-slate-800/80 bg-slate-950/95 px-4 py-3 md:hidden">
          <nav className="flex flex-col gap-2">
            {navItems.map(({ to, label }) => (
              <NavLink
                key={to}
                to={to}
                onClick={() => setMenuOpen(false)}
                className={({ isActive }) =>
                  `rounded-2xl px-4 py-3 text-sm font-medium transition ${
                    isActive ? 'bg-cyan-500/15 text-cyan-300' : 'text-slate-300 hover:bg-slate-900 hover:text-white'
                  }`
                }
              >
                {label}
              </NavLink>
            ))}
          </nav>
        </div>
      )}
    </header>
  );
}
