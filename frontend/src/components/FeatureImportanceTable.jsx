export default function FeatureImportanceTable({ rows = [], columns = [] }) {
  return (
    <div className="overflow-hidden rounded-[24px] border border-slate-800/80 bg-slate-900/80">
      <div className="max-h-[420px] overflow-auto">
        <table className="min-w-full border-separate border-spacing-0 text-sm">
          <thead className="sticky top-0 z-10 bg-slate-950/95 text-left text-slate-400 backdrop-blur">
            <tr>
              {columns.map((column) => (
                <th key={column} className="border-b border-slate-800 px-4 py-3.5 font-medium">
                  {column}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, index) => (
              <tr key={row.feature ?? row.label ?? row.title ?? index} className="transition-colors hover:bg-slate-800/40">
                {Object.values(row).map((value, cellIndex) => (
                  <td key={`${String(value)}-${cellIndex}`} className="border-b border-slate-800 px-4 py-3 text-slate-200">
                    {value}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
