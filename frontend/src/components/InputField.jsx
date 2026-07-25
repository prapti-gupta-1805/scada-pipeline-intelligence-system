export default function InputField({
  label,
  value,
  onChange,
  type = 'text',
  placeholder,
  step,
  min,
  max,
  helpText,
}) {
  return (
    <label className="block">
      <span className="mb-2 block text-sm font-medium text-slate-400">{label}</span>
      <input
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        step={step}
        min={min}
        max={max}
        className="h-11 w-full rounded-2xl border border-slate-700 bg-slate-900/80 px-4 text-sm text-white outline-none transition placeholder:text-slate-500 focus:border-cyan-500 focus:ring-4 focus:ring-cyan-500/10"
      />
      {helpText ? <span className="mt-2 block text-xs text-slate-500">{helpText}</span> : null}
    </label>
  );
}
