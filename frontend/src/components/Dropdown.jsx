export default function Dropdown({ label, value, onChange, options = [], helpText }) {
  return (
    <label className="block">
      <span className="mb-2 block text-sm font-medium text-slate-400">{label}</span>
      <select
        value={value}
        onChange={onChange}
        className="h-11 w-full rounded-2xl border border-slate-700 bg-slate-900/80 px-4 text-sm text-white outline-none transition focus:border-cyan-500 focus:ring-4 focus:ring-cyan-500/10"
      >
        <option value="">Select...</option>
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {helpText ? <span className="mt-2 block text-xs text-slate-500">{helpText}</span> : null}
    </label>
  );
}
