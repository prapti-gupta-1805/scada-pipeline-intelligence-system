import { motion } from 'framer-motion';
import { BarChart3, Sparkles } from 'lucide-react';
import faultConfusion from '../../../src/models/fault-classification/fault_confusion_matrix.png';
import faultImportance from '../../../src/models/fault-classification/fault_feature_importance.png';
import faultDistribution from '../../../src/models/fault-classification/fault_class_distribution.png';
import anomalyDistribution from '../../../src/models/anomaly-detection/anomaly_score_distribution.png';
import anomalyPca from '../../../src/models/anomaly-detection/anomaly_pca_projection.png';
import maintenanceImportance from '../../../src/models/predictive-maintenance/maintenance_feature_importance.png';
import maintenanceShap from '../../../src/models/predictive-maintenance/maintenance_shap_feature_importance.png';
import maintenanceSummary from '../../../src/models/predictive-maintenance/maintenance_model_summary.png';

const analyticsCards = [
  {
    title: 'Fault confusion matrix',
    subtitle: 'Model accuracy and class behavior',
    description: 'Confusion matrix for the fault classifier rendered from the repository assets.',
    insight: 'The classifier is separating normal and fault states with strong confidence across the test distribution.',
    image: faultConfusion,
    accent: 'from-cyan-500/15 to-slate-900',
  },
  {
    title: 'Fault feature importance',
    subtitle: 'Explainable feature attribution',
    description: 'Feature importance ranking for the fault model.',
    insight: 'The most influential factors point to pressure, energy, and pump conditions driving the fault decision.',
    image: faultImportance,
    accent: 'from-violet-500/15 to-slate-900',
  },
  {
    title: 'Fault class distribution',
    subtitle: 'Class balance for the training set',
    description: 'Distribution of fault classes across the dataset.',
    insight: 'The class mix shows where the model sees the strongest coverage and where the data is thinner.',
    image: faultDistribution,
    accent: 'from-emerald-500/15 to-slate-900',
  },
  {
    title: 'Anomaly score distribution',
    subtitle: 'Deviation profile for unusual telemetry',
    description: 'Histogram of anomaly scores from the isolation forest model.',
    insight: 'The model highlights segments with unusual operational drift that merit manual review.',
    image: anomalyDistribution,
    accent: 'from-amber-500/15 to-slate-900',
  },
  {
    title: 'Anomaly PCA projection',
    subtitle: 'Low-dimensional structure view',
    description: 'PCA projection of the anomaly detector inputs.',
    insight: 'The projection shows how normal and anomalous states separate in the latent feature space.',
    image: anomalyPca,
    accent: 'from-rose-500/15 to-slate-900',
  },
  {
    title: 'Maintenance feature importance',
    subtitle: 'Top factors influencing intervention risk',
    description: 'Feature contribution summary for maintenance action planning.',
    insight: 'Thickness loss and material degradation appear as the primary drivers behind intervention severity.',
    image: maintenanceImportance,
    accent: 'from-sky-500/15 to-slate-900',
  },
  {
    title: 'Maintenance SHAP summary',
    subtitle: 'Explainability for intervention planning',
    description: 'SHAP summary plot for the maintenance model.',
    insight: 'The SHAP outlook helps point to the combination of features that most strongly influence risk.',
    image: maintenanceShap,
    accent: 'from-indigo-500/15 to-slate-900',
  },
  {
    title: 'Maintenance model summary',
    subtitle: 'Model health snapshot',
    description: 'Concise summary of the predictive maintenance model outputs.',
    insight: 'The model summary reinforces the relationship between observed performance and intervention readiness.',
    image: maintenanceSummary,
    accent: 'from-fuchsia-500/15 to-slate-900',
  },
];

export default function AnalyticsPage() {
  return (
    <div className="space-y-6">
      <motion.section initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} className="rounded-[28px] border border-slate-800 bg-slate-900/80 p-6 shadow-2xl shadow-black/20">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.24em] text-cyan-400">Model analytics</p>
            <h2 className="mt-2 text-2xl font-semibold text-white">Explainability and performance assets</h2>
            <p className="mt-2 max-w-2xl text-sm text-slate-400">The dashboard displays the model visualizations already stored in the repository, keeping the analytics view grounded in the underlying ML artifacts.</p>
          </div>
          <div className="flex items-center gap-2 rounded-full border border-slate-700 bg-slate-800/70 px-3 py-2 text-sm text-slate-300">
            <Sparkles className="h-4 w-4 text-cyan-400" />
            Repository-backed visuals
          </div>
        </div>
      </motion.section>

      <div className="grid gap-6 xl:grid-cols-2">
        {analyticsCards.map((card, index) => (
          <motion.article
            key={card.title}
            initial={{ opacity: 0, y: 18 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.05 }}
            className="overflow-hidden rounded-[24px] border border-slate-800 bg-slate-900/80 shadow-2xl shadow-black/20"
          >
            <div className={`border-b border-slate-800 bg-gradient-to-r ${card.accent} px-5 py-4`}>
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="text-sm font-semibold uppercase tracking-[0.22em] text-cyan-400">{card.subtitle}</p>
                  <h3 className="mt-1 text-lg font-semibold text-white">{card.title}</h3>
                  <p className="mt-2 text-sm text-slate-400">{card.description}</p>
                </div>
                <div className="rounded-full border border-slate-700 bg-slate-800/70 p-2 text-slate-300">
                  <BarChart3 className="h-4 w-4" />
                </div>
              </div>
              <div className="mt-4 rounded-2xl border border-slate-800/80 bg-slate-950/70 p-3 text-sm text-slate-300">
                <span className="font-medium text-slate-100">Inference:</span> {card.insight}
              </div>
            </div>
            <div className="p-4">
              <img src={card.image} alt={card.title} className="h-80 w-full rounded-2xl border border-slate-800 object-contain bg-slate-950/70" />
            </div>
          </motion.article>
        ))}
      </div>
    </div>
  );
}
