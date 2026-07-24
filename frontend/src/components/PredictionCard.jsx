import { motion } from 'framer-motion';
import { ArrowRight, CheckCircle2, LoaderCircle, ShieldAlert } from 'lucide-react';

export default function PredictionCard({ title, description, children, result, loading, error, onSubmit, submitLabel = 'Run prediction' }) {
  return (
    <motion.section
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25 }}
      className="rounded-3xl border border-slate-800 bg-slate-900/80 p-5 shadow-2xl shadow-black/20"
    >
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.24em] text-cyan-400">Model workflow</p>
          <h2 className="mt-1 text-xl font-semibold text-white">{title}</h2>
          <p className="mt-2 max-w-2xl text-sm text-slate-400">{description}</p>
        </div>
        <div className="rounded-full border border-slate-700 bg-slate-800/70 px-3 py-1 text-sm text-slate-300">
          {loading ? 'Evaluating…' : 'Ready'}
        </div>
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
        <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
          {children}
          <button
            type="button"
            onClick={onSubmit}
            className="mt-5 inline-flex items-center gap-2 rounded-xl bg-cyan-500 px-4 py-2.5 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400"
          >
            {loading ? <LoaderCircle className="h-4 w-4 animate-spin" /> : <ArrowRight className="h-4 w-4" />}
            {submitLabel}
          </button>
        </div>

        <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
          <div className="flex items-center gap-2 text-sm font-semibold text-slate-200">
            {loading ? <LoaderCircle className="h-4 w-4 animate-spin text-cyan-400" /> : <CheckCircle2 className="h-4 w-4 text-emerald-400" />}
            Output
          </div>
          {error ? (
            <div className="mt-4 rounded-2xl border border-rose-500/30 bg-rose-500/10 p-4 text-sm text-rose-200">
              <div className="flex items-center gap-2 font-semibold">
                <ShieldAlert className="h-4 w-4" />
                {error}
              </div>
            </div>
          ) : result ? (
            <div className="mt-4 rounded-2xl border border-slate-800 bg-slate-950/60 p-4 text-sm text-slate-400">
              {typeof result === 'string' ? (
                <p>{result}</p>
              ) : (
                <p>Prediction output is ready. Review the detailed result panels below.</p>
              )}
            </div>
          ) : (
            <div className="mt-4 rounded-2xl border border-dashed border-slate-700 p-4 text-sm text-slate-400">
              Results appear here once the model is executed.
            </div>
          )}
        </div>
      </div>
    </motion.section>
  );
}
