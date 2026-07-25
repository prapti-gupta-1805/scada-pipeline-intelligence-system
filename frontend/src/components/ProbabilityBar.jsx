const toneMap = {
  blue: '#2563EB',
  amber: '#F59E0B',
  rose: '#EF4444',
  emerald: '#22C55E',
  sky: '#0EA5E9',
  slate: '#64748B',
};

export default function ProbabilityBar({ label, value, tone = 'blue', note }) {
  const percent = Math.max(0, Math.min(100, value));
  const fill = toneMap[tone] ?? toneMap.blue;

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between gap-4 text-sm">
        <span className="font-medium text-slate-200">{label}</span>
        <div className="text-right">
          <span className="font-semibold text-white">{percent.toFixed(1)}%</span>
          {note ? <span className="ml-2 text-slate-400">{note}</span> : null}
        </div>
      </div>
      <div className="h-2.5 rounded-full bg-slate-800">
        <div className="h-2.5 rounded-full transition-all duration-300" style={{ width: `${percent}%`, backgroundColor: fill }} />
      </div>
    </div>
  );
}
