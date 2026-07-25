import { useMemo, useState } from 'react';
import { motion } from 'framer-motion';
import { AlertTriangle, BarChart3, CircleDashed, ShieldAlert } from 'lucide-react';
import PredictionCard from '../components/PredictionCard';
import { predictAnomaly } from '../lib/api';

const defaultValues = {
  segment_id: '',
  pressure: '',
  flow_rate: '',
  temperature: '',
  valve_status: '',
  pump_state: '',
  pump_speed: '',
  compressor_state: '',
  energy_consumption: '',
  alarm_triggered: '',
  hour: '',
  day_of_week: '',
  day_of_month: '',
  explain: false,
};

import { anomalyFields as fields } from '../data/system';

export default function AnomalyPage() {
  const [form, setForm] = useState(defaultValues);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);

  const validate = useMemo(() => {
    const missing = fields.find((field) => form[field.key] === '' || form[field.key] === null);
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
        segment_id: Number(form.segment_id),
        pressure: Number(form.pressure),
        flow_rate: Number(form.flow_rate),
        temperature: Number(form.temperature),
        valve_status: Number(form.valve_status),
        pump_state: Number(form.pump_state),
        pump_speed: Number(form.pump_speed),
        compressor_state: Number(form.compressor_state),
        energy_consumption: Number(form.energy_consumption),
        alarm_triggered: Number(form.alarm_triggered),
        hour: Number(form.hour),
        day_of_week: Number(form.day_of_week),
        day_of_month: Number(form.day_of_month),
        explain: Boolean(form.explain),
      };

      const response = await predictAnomaly(payload);
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
      <PredictionCard title="Anomaly detection" description="Assess whether a new telemetry sample diverges from expected operating conditions." loading={loading} error={error} onSubmit={submit} submitLabel="Check anomaly" result={result}>
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
              <ShieldAlert className="h-4 w-4" />
              <h3 className="text-lg font-semibold text-white">Detection summary</h3>
            </div>
            <div className="mt-4 space-y-3 text-sm text-slate-300">
              <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-3">
                <p className="text-slate-400">Status</p>
                <p className="mt-1 text-xl font-semibold text-white">{result.status}</p>
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
              <h3 className="text-lg font-semibold text-white">Feature deviations</h3>
            </div>
            <div className="mt-4 space-y-3">
              {result.top_deviating_features?.map((feature) => (
                <div key={feature.feature} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-3 text-sm text-slate-300">
                  <div className="flex items-center justify-between">
                    <span className="font-medium text-white">{feature.feature}</span>
                    <span className="text-cyan-300">z={feature.z_score}</span>
                  </div>
                  <p className="mt-1 text-slate-400">Observed {feature.value} vs expected {feature.expected}</p>
                </div>
              ))}
            </div>
          </div>
        </motion.div>
      )}

      {result && !result.top_deviating_features && (
        <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="rounded-3xl border border-slate-800 bg-slate-900/80 p-5 shadow-2xl shadow-black/20">
          <div className="flex items-center gap-2 text-cyan-300">
            <CircleDashed className="h-4 w-4" />
            <h3 className="text-lg font-semibold text-white">Interpretation</h3>
          </div>
          <p className="mt-3 text-sm text-slate-400">The backend returned a condensed anomaly result without additional explanation details.</p>
        </motion.div>
      )}
    </div>
  );
}
