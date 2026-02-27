export default function QueryLogs({ logs }) {
    if (!logs.length) return null

    return (
        <div className="bg-bg-panel border border-border-subtle rounded-xl mb-5 overflow-hidden transition-all duration-300 hover:border-border-default">
            <div className="flex items-center justify-between px-4 py-3 border-b border-border-subtle bg-bg-panel-header">
                <span className="text-[0.72rem] font-semibold uppercase tracking-wider text-text-secondary">Query Logs</span>
                <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[0.68rem] font-semibold uppercase tracking-wide border bg-green-bg text-green border-green-border">
                    {logs.length} entries
                </span>
            </div>
            <div className="p-4">
                <div className="max-h-[350px] overflow-y-auto">
                    <table className="w-full border-collapse text-[0.78rem]">
                        <thead>
                            <tr>
                                <th className="bg-bg-table-header text-text-secondary font-semibold uppercase text-[0.67rem] tracking-wider px-3 py-2 text-left border-b border-border-default sticky top-0">ID</th>
                                <th className="bg-bg-table-header text-text-secondary font-semibold uppercase text-[0.67rem] tracking-wider px-3 py-2 text-left border-b border-border-default sticky top-0">Query</th>
                                <th className="bg-bg-table-header text-text-secondary font-semibold uppercase text-[0.67rem] tracking-wider px-3 py-2 text-left border-b border-border-default sticky top-0">Safe</th>
                                <th className="bg-bg-table-header text-text-secondary font-semibold uppercase text-[0.67rem] tracking-wider px-3 py-2 text-left border-b border-border-default sticky top-0">Time</th>
                                <th className="bg-bg-table-header text-text-secondary font-semibold uppercase text-[0.67rem] tracking-wider px-3 py-2 text-left border-b border-border-default sticky top-0">Error</th>
                                <th className="bg-bg-table-header text-text-secondary font-semibold uppercase text-[0.67rem] tracking-wider px-3 py-2 text-left border-b border-border-default sticky top-0">When</th>
                            </tr>
                        </thead>
                        <tbody>
                            {logs.map(log => (
                                <tr key={log.id} className="hover:bg-bg-table-row-hover">
                                    <td className="px-3 py-2 border-b border-border-subtle text-text-primary font-mono text-[0.75rem]">{log.id}</td>
                                    <td className="px-3 py-2 border-b border-border-subtle text-text-primary font-mono text-[0.75rem]">
                                        <span className="max-w-[280px] overflow-hidden text-ellipsis whitespace-nowrap block" title={log.query_text}>{log.query_text}</span>
                                    </td>
                                    <td className="px-3 py-2 border-b border-border-subtle">
                                        <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[0.68rem] font-semibold uppercase tracking-wide border ${log.safe ? 'bg-green-bg text-green border-green-border' : 'bg-red-bg text-red border-red-border'}`}>
                                            {log.safe ? 'Yes' : 'No'}
                                        </span>
                                    </td>
                                    <td className="px-3 py-2 border-b border-border-subtle text-text-primary font-mono text-[0.75rem]">
                                        {log.execution_time ? `${log.execution_time.toFixed(1)}ms` : '—'}
                                    </td>
                                    <td className="px-3 py-2 border-b border-border-subtle text-red text-[0.72rem]">{log.error || '—'}</td>
                                    <td className="px-3 py-2 border-b border-border-subtle text-text-muted text-[0.72rem]">
                                        {log.created_at ? new Date(log.created_at).toLocaleTimeString() : '—'}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    )
}
