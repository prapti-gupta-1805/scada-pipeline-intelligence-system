import { motion } from 'framer-motion';

export default function StatCard({ title, value, detail, accent = 'cyan' }) {
  const accentStyles = {
    cyan: 'from-cyan-500/20 to-cyan-400/5 text-cyan-300',
    emerald: 'from-emerald-500/20 to-emerald-400/5 text-emerald-300',
    amber: 'from-amber-500/20 to-amber-400/5 text-amber-300',
    rose: 'from-rose-500/20 to-rose-400/5 text-rose-300',
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25 }}
      className={`rounded-2xl border border-slate-800 bg-gradient-to-br ${accentStyles[accent]} p-4 shadow-lg shadow-black/10`}
    >
      <p className="text-sm text-slate-300">{title}</p>
      <p className="mt-3 text-2xl font-semibold text-white">{value}</p>
      <p className="mt-2 text-sm text-slate-400">{detail}</p>
    </motion.div>
  );
}
