import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Activity, AlertTriangle, BarChart3, ChevronRight, Cpu, ShieldCheck } from 'lucide-react';
import { Link } from 'react-router-dom';
import { LineChart, Line, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import StatCard from '../components/StatCard';
import { getHealth, getMetadata } from '../lib/api';

const healthSeries = [
  { name: '06:00', value: 82 },
  { name: '08:00', value: 77 },
  { name: '10:00', value: 84 },
  { name: '12:00', value: 88 },
  { name: '14:00', value: 91 },
  { name: '16:00', value: 86 },
  { name: '18:00', value: 90 },
];

export default function DashboardPage() {
  const [health, setHealth] = useState(null);
  const [metadata, setMetadata] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const [healthRes, metadataRes] = await Promise.all([getHealth(), getMetadata()]);
        setHealth(healthRes.data?.data || null);
        setMetadata(metadataRes.data?.data || null);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    load();
  }, []);

  return (
    <div className="space-y-6">
      <motion.section
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        className="overflow-hidden rounded-[28px] border border-slate-800 bg-gradient-to-br from-slate-900 via-slate-900 to-slate-800 p-6 shadow-2xl shadow-black/20"
      >
        <div className="grid gap-8 lg:grid-cols-[1.2fr_0.8fr]">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.3em] text-cyan-400">Mission control</p>
            <h2 className="mt-3 text-3xl font-semibold text-white">Monitor pipeline health with AI-driven insight.</h2>
            <p className="mt-4 max-w-2xl text-sm leading-7 text-slate-400">
              Detect faults, surface anomalies, and forecast maintenance needs from a single operations workspace.
            </p>
            <div className="mt-6 flex flex-wrap gap-3">
              <Link to="/fault" className="rounded-xl bg-cyan-500 px-4 py-2 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400">Run fault analysis</Link>
              <Link to="/analytics" className="rounded-xl border border-slate-700 bg-slate-800/70 px-4 py-2 text-sm font-semibold text-slate-200 transition hover:bg-slate-700">Review analytics</Link>
            </div>
          </div>

          <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-5">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-semibold text-white">Backend connection</p>
                <p className="text-sm text-slate-400">{loading ? 'Checking availability…' : health?.status || 'Unavailable'}</p>
              </div>
              <div className={`rounded-full px-3 py-1 text-sm ${health?.status === 'ok' ? 'bg-emerald-500/15 text-emerald-300' : 'bg-amber-500/15 text-amber-300'}`}>
                {health?.status === 'ok' ? 'Stable' : 'Degraded'}
              </div>
            </div>
            <div className="mt-4 space-y-3 text-sm text-slate-400">
              <div className="flex items-center justify-between rounded-xl border border-slate-800 bg-slate-900/80 px-3 py-2">
                <span>Fault model</span>
                <span className="text-slate-200">{health?.models?.fault ? 'Loaded' : 'Pending'}</span>
              </div>
              <div className="flex items-center justify-between rounded-xl border border-slate-800 bg-slate-900/80 px-3 py-2">
                <span>Anomaly model</span>
                <span className="text-slate-200">{health?.models?.anomaly ? 'Loaded' : 'Pending'}</span>
              </div>
              <div className="flex items-center justify-between rounded-xl border border-slate-800 bg-slate-900/80 px-3 py-2">
                <span>Maintenance model</span>
                <span className="text-slate-200">{health?.models?.maintenance ? 'Loaded' : 'Pending'}</span>
              </div>
            </div>
          </div>
        </div>
      </motion.section>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard title="Operational health" value="92%" detail="System stability across active pipelines" accent="cyan" />
        <StatCard title="Risk exposure" value="Low" detail="No critical incidents flagged this shift" accent="emerald" />
        <StatCard title="Model coverage" value="3/3" detail="Fault, anomaly, and maintenance models active" accent="amber" />
        <StatCard title="Insights" value={metadata ? `${Object.keys(metadata).length} modules` : '—'} detail="Connected to backend metadata" accent="rose" />
      </div>

      <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
        <motion.section initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} className="rounded-3xl border border-slate-800 bg-slate-900/80 p-5 shadow-2xl shadow-black/20">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.24em] text-cyan-400">System health</p>
              <h3 className="mt-1 text-lg font-semibold text-white">Telemetry trend over the day</h3>
            </div>
            <div className="rounded-full border border-slate-700 bg-slate-800/70 px-2.5 py-1 text-sm text-slate-300">Last 7 intervals</div>
          </div>
          <div className="mt-5 h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={healthSeries}>
                <XAxis dataKey="name" tickLine={false} axisLine={false} tick={{ fill: '#64748b' }} />
                <YAxis domain={[70, 100]} tickLine={false} axisLine={false} tick={{ fill: '#64748b' }} />
                <Tooltip />
                <Line type="monotone" dataKey="value" stroke="#22d3ee" strokeWidth={3} dot={{ r: 4, fill: '#22d3ee' }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </motion.section>

        <motion.section initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} className="rounded-3xl border border-slate-800 bg-slate-900/80 p-5 shadow-2xl shadow-black/20">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.24em] text-cyan-400">Quick actions</p>
              <h3 className="mt-1 text-lg font-semibold text-white">Jump into a workflow</h3>
            </div>
          </div>
          <div className="mt-4 space-y-3">
            {[
              { to: '/fault', label: 'Fault classification', icon: AlertTriangle, description: 'Classify pipeline faults and view probabilities' },
              { to: '/anomaly', label: 'Anomaly detection', icon: ShieldCheck, description: 'Highlight deviations from normal operating ranges' },
              { to: '/maintenance', label: 'Predictive maintenance', icon: Cpu, description: 'Assess asset condition and intervention risk' },
            ].map(({ to, label, icon: Icon, description }) => (
              <Link key={to} to={to} className="flex items-start justify-between rounded-2xl border border-slate-800 bg-slate-950/60 p-3 transition hover:border-cyan-500/40 hover:bg-slate-800/70">
                <div className="flex items-start gap-3">
                  <div className="rounded-xl border border-cyan-500/20 bg-cyan-500/10 p-2 text-cyan-300">
                    <Icon className="h-4 w-4" />
                  </div>
                  <div>
                    <p className="font-semibold text-white">{label}</p>
                    <p className="mt-1 text-sm text-slate-400">{description}</p>
                  </div>
                </div>
                <ChevronRight className="mt-1 h-4 w-4 text-slate-500" />
              </Link>
            ))}
          </div>
        </motion.section>
      </div>

      <motion.section initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} className="rounded-3xl border border-slate-800 bg-slate-900/80 p-5 shadow-2xl shadow-black/20">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.24em] text-cyan-400">Recent predictions</p>
            <h3 className="mt-1 text-lg font-semibold text-white">Latest inference activity</h3>
          </div>
          <div className="rounded-full border border-slate-700 bg-slate-800/70 px-2.5 py-1 text-sm text-slate-300">Live</div>
        </div>
        <div className="mt-5 overflow-hidden rounded-2xl border border-slate-800">
          <table className="min-w-full divide-y divide-slate-800 text-sm">
            <thead className="bg-slate-950/70 text-left text-slate-400">
              <tr>
                <th className="px-4 py-3 font-medium">Model</th>
                <th className="px-4 py-3 font-medium">Outcome</th>
                <th className="px-4 py-3 font-medium">Confidence</th>
                <th className="px-4 py-3 font-medium">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 bg-slate-900/60">
              {[{ model: 'Fault classification', outcome: 'Normal', confidence: '0.91', status: 'Healthy' }, { model: 'Anomaly detection', outcome: 'Anomaly', confidence: '0.84', status: 'Investigate' }, { model: 'Predictive maintenance', outcome: 'Moderate', confidence: '0.78', status: 'Monitor' }].map((row) => (
                <tr key={row.model}>
                  <td className="px-4 py-3 text-slate-200">{row.model}</td>
                  <td className="px-4 py-3 text-slate-200">{row.outcome}</td>
                  <td className="px-4 py-3 text-slate-200">{row.confidence}</td>
                  <td className="px-4 py-3">
                    <span className="rounded-full border border-emerald-500/20 bg-emerald-500/10 px-2.5 py-1 text-xs text-emerald-300">{row.status}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </motion.section>
    </div>
  );
}
