import { Bell, Menu, UserCircle2 } from 'lucide-react';
import { useEffect, useState } from 'react';
import { appName } from '../data/system';

function formatClock(date) {
  return new Intl.DateTimeFormat('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  }).format(date);
}

export default function Navbar({ pageTitle, onMenuClick }) {
  const [clock, setClock] = useState(() => formatClock(new Date()));

  useEffect(() => {
    const timer = window.setInterval(() => setClock(formatClock(new Date())), 1000 * 30);
    return () => window.clearInterval(timer);
  }, []);

  return (
    <header className="border-b border-slate-200 bg-white">
      <div className="flex items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={onMenuClick}
            className="inline-flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 bg-white text-slate-700 transition hover:border-slate-300 hover:text-slate-950 lg:hidden"
            aria-label="Open navigation"
          >
            <Menu className="h-5 w-5" />
          </button>
          <div>
            <p className="text-[11px] font-semibold uppercase tracking-[0.24em] text-slate-500">{appName}</p>
            <h1 className="mt-1 text-xl font-semibold tracking-tight text-slate-950">{pageTitle}</h1>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="hidden text-sm font-medium text-slate-500 xl:block">
            {clock}
          </div>
          <button type="button" className="inline-flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 bg-white text-slate-600 transition hover:border-slate-300 hover:text-slate-950">
            <Bell className="h-5 w-5" />
          </button>
          <button type="button" className="inline-flex h-10 items-center gap-3 rounded-xl border border-slate-200 bg-white px-3 pr-4 transition hover:border-slate-300">
            <span className="inline-flex h-7 w-7 items-center justify-center rounded-full bg-slate-900 text-xs font-semibold text-white">OP</span>
            <span className="hidden text-sm font-medium text-slate-700 sm:block">Operations</span>
            <UserCircle2 className="h-5 w-5 text-slate-500 sm:hidden" />
          </button>
        </div>
      </div>
    </header>
  );
}
