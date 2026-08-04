import { motion } from 'framer-motion';
import { ArrowDown, Cpu, Server, ShieldCheck, Triangle, Workflow } from 'lucide-react';
import ChartCard from '../components/ChartCard';
import StatusBadge from '../components/StatusBadge';
import { aboutModels, architectureFlow, appTagline, appName, techStack } from '../data/system';

const architectureIcons = [Server, Workflow, Cpu, Triangle, ShieldCheck];

export default function AboutPage() {
  return (
    <div className="space-y-6">
      <motion.section
        initial={{ opacity: 0, y: 14 }}
        animate={{ opacity: 1, y: 0 }}
        className="rounded-[32px] border border-slate-200 bg-white p-6 shadow-[0_18px_50px_rgba(15,23,42,0.06)]"
      >
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.24em] text-blue-700">System overview</p>
            <h2 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">{appName}</h2>
            <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-600">{appTagline}</p>
          </div>
          <StatusBadge label="Proof-of-concept" tone="success" />
        </div>
      </motion.section>

      <ChartCard title="Architecture flow" subtitle="End-to-end pipeline" note="How the system works">
        <div className="grid gap-4 xl:grid-cols-5">
          {architectureFlow.map((step, index) => {
            const Icon = architectureIcons[index];
            return (
              <div key={step.title} className="relative rounded-[24px] border border-slate-200 bg-slate-50 p-4">
                <div className="flex items-center justify-between">
                  <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-white text-blue-600 shadow-sm">
                    <Icon className="h-5 w-5" />
                  </div>
                  {index < architectureFlow.length - 1 ? <ArrowDown className="h-5 w-5 text-slate-400 xl:hidden" /> : null}
                </div>
                <p className="mt-4 text-sm font-semibold uppercase tracking-[0.18em] text-slate-500">{step.title}</p>
                <p className="mt-3 text-sm leading-6 text-slate-600">{step.detail}</p>
              </div>
            );
          })}
        </div>
      </ChartCard>

      <div className="grid gap-6 xl:grid-cols-3">
        {aboutModels.map((model) => {
          const Icon = model.icon;
          return (
            <ChartCard key={model.title} title={model.title} subtitle="Model responsibilities" note="Explainable">
              <div className="flex items-start gap-4">
                <div className="rounded-2xl border border-slate-200 bg-slate-50 p-3 text-blue-600">
                  <Icon className="h-5 w-5" />
                </div>
                <p className="text-sm leading-6 text-slate-600">{model.description}</p>
              </div>
            </ChartCard>
          );
        })}
      </div>

      <ChartCard title="Technology stack" subtitle="Implementation layer" note="Frontend and ML ecosystem">
        <div className="flex flex-wrap gap-3">
          {techStack.map((item) => (
            <span key={item} className="rounded-full border border-slate-200 bg-slate-50 px-4 py-2 text-sm font-medium text-slate-700">
              {item}
            </span>
          ))}
        </div>
      </ChartCard>

    </div>
  );
}
