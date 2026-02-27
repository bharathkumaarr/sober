export default function SimulationPanel({ simulation, simulating }) {
    if (!simulation && !simulating) return null

    return (
        <div className="bg-bg-panel border border-border-subtle rounded-xl overflow-hidden transition-all duration-300 hover:border-border-default">
            <div className="flex items-center justify-between px-4 py-3 border-b border-border-subtle bg-bg-panel-header">
                <span className="text-[0.72rem] font-semibold uppercase tracking-wider text-text-secondary">Simulation</span>
            </div>
            <div className="p-4">
                {simulating ? (
                    <div className="text-center py-8 text-text-muted text-[0.82rem]">
                        <span className="inline-block w-3.5 h-3.5 border-2 border-black/15 border-t-current rounded-full animate-spin mr-2" />
                        Simulating...
                    </div>
                ) : simulation && (
                    <>
                        <div className="flex gap-4 mb-3.5">
                            <div className="flex-1 bg-bg-input border border-border-subtle rounded-lg p-3 text-center transition-colors duration-300">
                                <div className="text-xl font-bold text-accent font-mono">
                                    {simulation.cost_estimate?.rows_scanned_estimate ?? simulation.rows_estimate}
                                </div>
                                <div className="text-[0.65rem] text-text-muted uppercase tracking-wider mt-0.5">Est. Rows</div>
                            </div>
                            <div className="flex-1 bg-bg-input border border-border-subtle rounded-lg p-3 text-center transition-colors duration-300">
                                <div className={`text-xl font-bold font-mono complexity-${simulation.cost_estimate?.complexity || 'low'}`}>
                                    {(simulation.cost_estimate?.complexity || 'low').toUpperCase()}
                                </div>
                                <div className="text-[0.65rem] text-text-muted uppercase tracking-wider mt-0.5">Complexity</div>
                            </div>
                        </div>
                        {simulation.explain_plan?.length > 0 && (
                            <>
                                <div className="text-[0.68rem] font-semibold uppercase tracking-wider text-text-secondary mb-1.5">Explain Plan</div>
                                <div className="bg-bg-input border border-border-subtle rounded-lg px-4 py-3 font-mono text-[0.75rem] text-text-secondary leading-[1.7] overflow-x-auto whitespace-pre-wrap transition-colors duration-300">
                                    {simulation.explain_plan.map((entry, i) => (
                                        <div key={i}>{entry.detail || JSON.stringify(entry)}</div>
                                    ))}
                                </div>
                            </>
                        )}
                    </>
                )}
            </div>
        </div>
    )
}
