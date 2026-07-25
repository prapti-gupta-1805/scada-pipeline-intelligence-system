import { useMemo, useState } from 'react';
import { motion } from 'framer-motion';
import { AlertTriangle, BarChart3, CircleDashed, Cpu } from 'lucide-react';
import PredictionCard from '../components/PredictionCard';
import { predictMaintenance } from '../lib/api';

const defaultValues = {
  Pipe_Size_mm: '',
  Thickness_mm: '',
  Material: '',
  Grade: '',
  Max_Pressure_psi: '',
  Temperature_C: '',
  Corrosion_Impact_Percent: '',
  Thickness_Loss_mm: '',
  Material_Loss_Percent: '',
  Time_Years: '',
  explain: false,
};

import { maintenanceFields as fields } from '../data/system';

export default function MaintenancePage() {
  const [form, setForm] = useState(defaultValues);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);

  const validate = useMemo(() => {
    const missing = fields.find((field) => !String(form[field.key]).trim());
    return missing ? `Please complete ${missing.label}.` : '';
  }, [form]);

  const submit = async () => {
    setError('');
    if (validate) {
      setError(validate);
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const payload = {
        ...form,
        Pipe_Size_mm: Number(form.Pipe_Size_mm),
        Thickness_mm: Number(form.Thickness_mm),
        Max_Pressure_psi: Number(form.Max_Pressure_psi),
        Temperature_C: Number(form.Temperature_C),
        Corrosion_Impact_Percent: Number(form.Corrosion_Impact_Percent),
        Thickness_Loss_mm: Number(form.Thickness_Loss_mm),
        Material_Loss_Percent: Number(form.Material_Loss_Percent),
        Time_Years: Number(form.Time_Years),
        explain: Boolean(form.explain),
      };

      const response = await predictMaintenance(payload);
      setResult(response.data?.data?.prediction || null);
    } catch (err) {
      const message = err?.response?.data?.detail || err?.response?.data?.error?.message || 'Prediction failed.';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <PredictionCard title="Predictive maintenance" description="Estimate pipeline condition and forecast whether intervention is needed soon." loading={loading} error={error} onSubmit={submit} submitLabel="Assess maintenance" result={result}>
        <div className="grid gap-4 md:grid-cols-2">
          {fields.map((field) => (
            <label key={field.key} className="block text-sm text-slate-300">
              <span className="mb-1.5 block font-medium text-slate-400">{field.label}</span>
              {field.type === 'select' ? (
                <select
                  value={form[field.key]}
                  onChange={(e) => setForm((prev) => ({ ...prev, [field.key]: e.target.value }))}
                  className="w-full rounded-xl border border-slate-700 bg-slate-900/70 px-3 py-2.5 text-sm text-white outline-none ring-0 transition focus:border-cyan-500"
                >
                  <option value="">Select {field.label}</option>
                  {field.options.map((opt) => (
                    <option key={opt.value} value={opt.value}>
                      {opt.label}
                    </option>
                  ))}
                </select>
              ) : (
                <input
                  type={field.type}
                  step={field.step}
                  value={form[field.key]}
                  onChange={(e) => setForm((prev) => ({ ...prev, [field.key]: e.target.value }))}
                  className="w-full rounded-xl border border-slate-700 bg-slate-900/70 px-3 py-2.5 text-sm text-white outline-none ring-0 transition focus:border-cyan-500"
                />
              )}
            </label>
          ))}
        </div>
      </PredictionCard>

      {result && (
        <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
          <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-5 shadow-2xl shadow-black/20">
            <div className="flex items-center gap-2 text-cyan-300">
              <Cpu className="h-4 w-4" />
              <h3 className="text-lg font-semibold text-white">Maintenance outlook</h3>
            </div>
            <div className="mt-4 space-y-3 text-sm text-slate-300">
              <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-3">
                <p className="text-slate-400">Predicted condition</p>
                <p className="mt-1 text-xl font-semibold text-white">{result.prediction}</p>
              </div>
              <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-3">
                <p className="text-slate-400">Risk level</p>
                <p className="mt-1 text-xl font-semibold text-white">{result.risk_level}</p>
              </div>
              <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-3">
                <p className="text-slate-400">Confidence</p>
                <p className="mt-1 text-xl font-semibold text-white">{(result.confidence * 100).toFixed(1)}%</p>
              </div>
            </div>
          </div>

          <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-5 shadow-2xl shadow-black/20">
            <div className="flex items-center gap-2 text-cyan-300">
              <BarChart3 className="h-4 w-4" />
              <h3 className="text-lg font-semibold text-white">Class probabilities</h3>
            </div>
            <div className="mt-4 space-y-3">
              {result.class_probabilities && Object.entries(result.class_probabilities).map(([label, value]) => (
                <div key={label}>
                  <div className="mb-1 flex justify-between text-sm text-slate-400">
                    <span>{label}</span>
                    <span>{(value * 100).toFixed(1)}%</span>
                  </div>
                  <div className="h-2.5 rounded-full bg-slate-800">
                    <div className="h-2.5 rounded-full bg-cyan-500" style={{ width: `${Math.max(8, value * 100)}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </motion.div>
      )}

      {result?.top_contributing_features && (
        <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="rounded-3xl border border-slate-800 bg-slate-900/80 p-5 shadow-2xl shadow-black/20">
          <div className="flex items-center gap-2 text-cyan-300">
            <CircleDashed className="h-4 w-4" />
            <h3 className="text-lg font-semibold text-white">Feature importance</h3>
          </div>
          <div className="mt-4 overflow-hidden rounded-2xl border border-slate-800">
            <table className="min-w-full divide-y divide-slate-800 text-sm">
              <thead className="bg-slate-950/70 text-left text-slate-400">
                <tr>
                  <th className="px-4 py-3 font-medium">Feature</th>
                  <th className="px-4 py-3 font-medium">Value</th>
                  <th className="px-4 py-3 font-medium">Importance</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800 bg-slate-900/60">
                {result.top_contributing_features.map((feature) => (
                  <tr key={feature.feature}>
                    <td className="px-4 py-3 text-slate-200">{feature.feature}</td>
                    <td className="px-4 py-3 text-slate-400">{feature.value}</td>
                    <td className="px-4 py-3 text-slate-200">{feature.importance}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </motion.div>
      )}
    </div>
  );
}
