import { AlertTriangle, BarChart3, Cpu, Gauge, Info, ShieldCheck, Sparkles } from 'lucide-react';

export const appName = 'SCADA Pipeline Intelligence System';
export const appTagline =
  'AI-powered monitoring, anomaly detection, fault diagnosis and predictive maintenance for industrial pipeline infrastructure.';

export const navItems = [
  { to: '/', label: 'Dashboard', icon: Gauge, description: 'Live operational overview' },
  { to: '/anomaly', label: 'Anomaly Detection', icon: ShieldCheck, description: 'Spot abnormal telemetry' },
  { to: '/fault', label: 'Fault Classification', icon: AlertTriangle, description: 'Classify failure modes' },
  { to: '/maintenance', label: 'Predictive Maintenance', icon: Cpu, description: 'Forecast intervention risk' },
  { to: '/analytics', label: 'Analytics', icon: BarChart3, description: 'Model performance evidence' },
  { to: '/about', label: 'About', icon: Info, description: 'Project overview and design intent' },
];

export const routeTitles = {
  '/': 'Dashboard',
  '/dashboard': 'Dashboard',
  '/anomaly-detection': 'Anomaly Detection',
  '/anomaly': 'Anomaly Detection',
  '/fault-classification': 'Fault Classification',
  '/fault': 'Fault Classification',
  '/predictive-maintenance': 'Predictive Maintenance',
  '/maintenance': 'Predictive Maintenance',
  '/analytics': 'Analytics',
  '/about': 'About',
};

const sharedTelemetryFields = [
  { key: 'pressure', label: 'Pressure', type: 'number', step: '0.1' },
  { key: 'flow_rate', label: 'Flow Rate', type: 'number', step: '0.1' },
  { key: 'temperature', label: 'Temperature', type: 'number', step: '0.1' },
  {
    key: 'valve_status',
    label: 'Valve Status',
    type: 'select',
    options: [
      { label: 'Closed', value: 0 },
      { label: 'Open', value: 1 },
    ],
  },
  {
    key: 'pump_state',
    label: 'Pump State',
    type: 'select',
    options: [
      { label: 'Stopped', value: 0 },
      { label: 'Running', value: 1 },
    ],
  },
  { key: 'pump_speed', label: 'Pump Speed', type: 'number', step: '10' },
  {
    key: 'compressor_state',
    label: 'Compressor State',
    type: 'select',
    options: [
      { label: 'Idle', value: 0 },
      { label: 'Active', value: 1 },
    ],
  },
  { key: 'energy_consumption', label: 'Energy Consumption', type: 'number', step: '0.1' },
  { key: 'hour', label: 'Hour', type: 'number', step: '1' },
  { key: 'day_of_week', label: 'Day of Week', type: 'number', step: '1' },
  { key: 'day_of_month', label: 'Day of Month', type: 'number', step: '1' },
];

export const anomalyFields = sharedTelemetryFields;
export const faultFields = sharedTelemetryFields;

export const maintenanceFields = [
  { key: 'Pipe_Size_mm', label: 'Pipe Size (mm)', type: 'number', step: '0.1' },
  { key: 'Thickness_mm', label: 'Thickness (mm)', type: 'number', step: '0.1' },
  {
    key: 'Material',
    label: 'Material',
    type: 'select',
    options: [
      { label: 'Carbon Steel', value: 'Carbon Steel' },
      { label: 'Stainless Steel', value: 'Stainless Steel' },
      { label: 'Alloy Steel', value: 'Alloy Steel' },
    ],
  },
  {
    key: 'Grade',
    label: 'Grade',
    type: 'select',
    options: [
      { label: 'API 5L X42', value: 'API 5L X42' },
      { label: 'API 5L X52', value: 'API 5L X52' },
      { label: 'API 5L X60', value: 'API 5L X60' },
    ],
  },
  { key: 'Max_Pressure_psi', label: 'Max Pressure (psi)', type: 'number', step: '0.1' },
  { key: 'Temperature_C', label: 'Temperature (C)', type: 'number', step: '0.1' },
  { key: 'Corrosion_Impact_Percent', label: 'Corrosion Impact (%)', type: 'number', step: '0.1' },
  { key: 'Thickness_Loss_mm', label: 'Thickness Loss (mm)', type: 'number', step: '0.1' },
  { key: 'Material_Loss_Percent', label: 'Material Loss (%)', type: 'number', step: '0.1' },
  { key: 'Time_Years', label: 'Time (Years)', type: 'number', step: '0.1' },
];

export const analyticsModelCards = [
  {
    title: 'Fault classification',
    subtitle: 'Confusion matrix',
    image: '/models/fault-classification/fault_confusion_matrix.png',
    description: 'Saved confusion matrix artifact for the fault classifier.',
  },
  {
    title: 'Fault classification',
    subtitle: 'Feature importance',
    image: '/models/fault-classification/fault_feature_importance.png',
    description: 'Saved feature-importance artifact for the fault classifier.',
  },
  {
    title: 'Fault classification',
    subtitle: 'Class distribution',
    image: '/models/fault-classification/fault_class_distribution.png',
    description: 'Saved class-distribution artifact for the fault dataset.',
  },
  {
    title: 'Anomaly detection',
    subtitle: 'PCA projection',
    image: '/models/anomaly-detection/anomaly_pca_projection.png',
    description: 'Saved PCA projection artifact for anomaly detection inputs.',
  },
  {
    title: 'Anomaly detection',
    subtitle: 'Score distribution',
    image: '/models/anomaly-detection/anomaly_score_distribution.png',
    description: 'Saved anomaly-score distribution artifact.',
  },
  {
    title: 'Predictive maintenance',
    subtitle: 'Feature importance',
    image: '/models/predictive-maintenance/maintenance_feature_importance.png',
    description: 'Saved feature-importance artifact for the maintenance model.',
  },
  {
    title: 'Predictive maintenance',
    subtitle: 'SHAP summary',
    image: '/models/predictive-maintenance/maintenance_shap_feature_importance.png',
    description: 'Saved SHAP summary artifact for the maintenance model.',
  },
  {
    title: 'Predictive maintenance',
    subtitle: 'Model summary',
    image: '/models/predictive-maintenance/maintenance_model_summary.png',
    description: 'Saved model summary artifact for the maintenance pipeline.',
  },
];

export const architectureFlow = [
  {
    title: 'Ingest',
    detail: 'SCADA telemetry is collected from sensors, pumps, valves and other field assets in near real time.',
  },
  {
    title: 'Analyse',
    detail: 'Anomaly detection and fault classification models screen the data for abnormal behaviour and likely failure modes.',
  },
  {
    title: 'Predict',
    detail: 'The maintenance model estimates remaining useful life and highlights the next intervention window.',
  },
  {
    title: 'Prioritise',
    detail: 'Operators receive actionable risk labels and recommendations so they can focus on the highest-impact issues first.',
  },
  {
    title: 'Respond',
    detail: 'The dashboard turns analysis into rapid operational decisions with explainable, review-friendly evidence.',
  },
];

export const aboutModels = [
  {
    title: 'Anomaly detection',
    description:
      'This component flags unusual telemetry patterns that may indicate equipment drift, leaks or process instability before they become critical.',
    icon: ShieldCheck,
  },
  {
    title: 'Fault classification',
    description:
      'This model categorises likely failure modes so engineers can identify the probable root cause quickly and communicate it clearly.',
    icon: AlertTriangle,
  },
  {
    title: 'Predictive maintenance',
    description:
      'The maintenance layer estimates future risk and supports more reliable planning for inspections, servicing and replacements.',
    icon: Cpu,
  },
];

export const techStack = ['React', 'Vite', 'Tailwind CSS', 'FastAPI', 'scikit-learn', 'SHAP', 'XGBoost', 'Isolation Forest'];

export function createEmptyForm(fields, extraValues = {}) {
  return fields.reduce(
    (accumulator, field) => {
      accumulator[field.key] = '';
      return accumulator;
    },
    { ...extraValues },
  );
}
