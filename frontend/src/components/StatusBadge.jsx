const toneClasses = {
  success: 'border-emerald-500/20 bg-emerald-500/10 text-emerald-300',
  warning: 'border-amber-500/20 bg-amber-500/10 text-amber-300',
  critical: 'border-rose-500/20 bg-rose-500/10 text-rose-300',
  info: 'border-cyan-500/20 bg-cyan-500/10 text-cyan-300',
  neutral: 'border-slate-700 bg-slate-800/80 text-slate-300',
};

export default function StatusBadge({ label, tone = 'neutral' }) {
  return (
    <span
      className={`inline-flex items-center rounded-full border px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.2em] ${toneClasses[tone] ?? toneClasses.neutral}`}
    >
      {label}
    </span>
  );
}
