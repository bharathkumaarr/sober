export default function ResultsTable({ execution }) {
    if (!execution) return null

    return (
        <div className="bg-bg-panel border border-border-subtle rounded-xl mb-5 overflow-hidden transition-all duration-300 hover:border-border-default">
            <div className="flex items-center justify-between px-4 py-3 border-b border-border-subtle bg-bg-panel-header">
                <span className="text-[0.72rem] font-semibold uppercase tracking-wider text-text-secondary">Execution Results</span>
                <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[0.68rem] font-semibold uppercase tracking-wide border bg-green-bg text-green border-green-border">
                    {execution.row_count} rows • {execution.execution_time_ms}ms
                </span>
            </div>
            <div className="p-4">
                {execution.warnings?.length > 0 && execution.warnings.map((w, i) => (
                    <div key={i} className="flex items-start gap-1.5 px-3 py-2 bg-yellow-bg border border-yellow-border rounded-[5px] mb-1.5 text-[0.78rem] text-yellow">
                        ⚠ {w}
                    </div>
                ))}
                {execution.rows?.length > 0 ? (
                    <div className="overflow-x-auto rounded-lg border border-border-subtle">
                        <table className="w-full border-collapse text-[0.78rem]">
                            <thead>
                                <tr>
                                    {Object.keys(execution.rows[0]).map(col => (
                                        <th key={col} className="bg-bg-table-header text-text-secondary font-semibold uppercase text-[0.67rem] tracking-wider px-3 py-2 text-left border-b border-border-default sticky top-0">
                                            {col}
                                        </th>
                                    ))}
                                </tr>
                            </thead>
                            <tbody>
                                {execution.rows.map((row, i) => (
                                    <tr key={i} className="hover:bg-bg-table-row-hover">
                                        {Object.values(row).map((val, j) => (
                                            <td key={j} className="px-3 py-2 border-b border-border-subtle text-text-primary font-mono text-[0.75rem]">
                                                {val === null ? <em className="text-text-muted">NULL</em> : String(val)}
                                            </td>
                                        ))}
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                ) : (
                    <div className="text-center py-8 text-text-muted text-[0.82rem]">
                        <div className="text-3xl mb-1.5 opacity-50">📭</div>
                        No rows returned
                    </div>
                )}
            </div>
        </div>
    )
}
