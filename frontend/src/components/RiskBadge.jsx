import StatusBadge from './StatusBadge';

const riskTone = {
  low: 'success',
  medium: 'warning',
  high: 'critical',
  stable: 'info',
};

export default function RiskBadge({ label, tone = 'neutral' }) {
  return <StatusBadge label={label} tone={riskTone[tone.toLowerCase()] ?? tone} />;
}

