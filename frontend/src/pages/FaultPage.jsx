import { useMemo, useState } from 'react';
import { motion } from 'framer-motion';
import { AlertTriangle, BarChart3, CircleDashed } from 'lucide-react';
import PredictionCard from '../components/PredictionCard';
import { predictFault } from '../lib/api';

const defaultValues = {
  segment_id: 10,
  pressure: 72.1,
  flow_rate: 4.5,
  temperature: 31.6,
  valve_status: 1,
  pump_state: 1,
  pump_speed: 1380,
  compressor_state: 1,
  energy_consumption: 33.2,
  alarm_triggered: 0,
  hour: 14,
  day_of_week: 2,
  day_of_month: 12,
  explain: true,
};

const fields = [
  { key: 'segment_id', label: 'Segment ID', type: 'number' },
  { key: 'pressure', label: 'Pressure', type: 'number', step: '0.1' },
  { key: 'flow_rate', label: 'Flow Rate', type: 'number', step: '0.1' },
  { key: 'temperature', label: 'Temperature', type: 'number', step: '0.1' },
  { key: 'valve_status', label: 'Valve Status', type: 'number' },
  { key: 'pump_state', label: 'Pump State', type: 'number' },
  { key: 'pump_speed', label: 'Pump Speed', type: 'number' },
  { key: 'compressor_state', label: 'Compressor State', type: 'number' },
  { key: 'energy_consumption', label: 'Energy Consumption', type: 'number', step: '0.1' },
  { key: 'alarm_triggered', label: 'Alarm Triggered', type: 'number' },
  { key: 'hour', label: 'Hour', type: 'number' },
  { key: 'day_of_week', label: 'Day of Week', type: 'number' },
  { key: 'day_of_month', label: 'Day of Month', type: 'number' },
];

export default function FaultPage() {
  const [form, setForm] = useState(defaultValues);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);

  const handleChange = (key, value) => {
    setForm((prev) => ({ ...prev, [key]: value }));
  };

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

      const response = await predictFault(payload);
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
      <PredictionCard title="Fault classification" description="Submit pipeline telemetry to classify whether the segment is normal or exhibits a known fault pattern." loading={loading} error={error} onSubmit={submit} submitLabel="Classify fault" result={result}>
        <div className="grid gap-4 md:grid-cols-2">
          {fields.map((field) => (
            <label key={field.key} className="block text-sm text-slate-300">
              <span className="mb-1.5 block font-medium text-slate-400">{field.label}</span>
              <input
                type={field.type}
                step={field.step}
                value={form[field.key]}
                onChange={(e) => handleChange(field.key, e.target.value)}
                className="w-full rounded-xl border border-slate-700 bg-slate-900/70 px-3 py-2.5 text-sm text-white outline-none ring-0 transition focus:border-cyan-500"
              />
            </label>
          ))}
        </div>
      </PredictionCard>

      {result && (
        <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
          <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-5 shadow-2xl shadow-black/20">
            <div className="flex items-center gap-2 text-cyan-300">
              <AlertTriangle className="h-4 w-4" />
              <h3 className="text-lg font-semibold text-white">Prediction summary</h3>
            </div>
            <div className="mt-4 space-y-3 text-sm text-slate-300">
              <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-3">
                <p className="text-slate-400">Predicted class</p>
                <p className="mt-1 text-xl font-semibold text-white">{result.predicted_class}</p>
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

      {result?.shap_explanation && typeof result.shap_explanation !== 'string' && (
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
                  <th className="px-4 py-3 font-medium">SHAP impact</th>
                  <th className="px-4 py-3 font-medium">Direction</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800 bg-slate-900/60">
                {result.shap_explanation.top_features.map((feature) => (
                  <tr key={feature.feature}>
                    <td className="px-4 py-3 text-slate-200">{feature.feature}</td>
                    <td className="px-4 py-3 text-slate-400">{feature.value}</td>
                    <td className="px-4 py-3 text-slate-200">{feature.shap_value.toFixed(3)}</td>
                    <td className="px-4 py-3 text-slate-400">{feature.direction}</td>
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
