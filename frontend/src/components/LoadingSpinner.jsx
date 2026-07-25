import { LoaderCircle } from 'lucide-react';

export default function LoadingSpinner({ label = 'Loading' }) {
  return (
    <div className="inline-flex items-center gap-2 text-sm font-medium text-slate-500">
      <LoaderCircle className="h-4 w-4 animate-spin text-blue-600" />
      <span>{label}</span>
    </div>
  );
}

