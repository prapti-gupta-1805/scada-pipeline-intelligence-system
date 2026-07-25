import { motion } from 'framer-motion';

export default function ChartCard({ title, subtitle, children, note }) {
  return (
    <motion.section
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="overflow-hidden rounded-[28px] border border-slate-800/80 bg-slate-900/80 p-6 shadow-[0_18px_50px_rgba(15,23,42,0.18)] transition-shadow duration-200 hover:shadow-[0_22px_60px_rgba(15,23,42,0.24)]"
    >
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          {subtitle ? <p className="text-xs font-semibold uppercase tracking-[0.24em] text-cyan-400">{subtitle}</p> : null}
          <h3 className="mt-1 text-xl font-semibold tracking-tight text-white">{title}</h3>
        </div>
        {note ? (
          <span className="rounded-full border border-slate-700 bg-slate-800/80 px-3 py-1 text-xs font-medium text-slate-300">
            {note}
          </span>
        ) : null}
      </div>
      <div className="mt-5">{children}</div>
    </motion.section>
  );
}
