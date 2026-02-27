export default function SafetyPanel({ analysis }) {
    if (!analysis) return null

    return (
        <div className="bg-bg-panel border border-border-subtle rounded-xl overflow-hidden transition-all duration-300 hover:border-border-default">
            <div className="flex items-center justify-between px-4 py-3 border-b border-border-subtle bg-bg-panel-header">
                <span className="text-[0.72rem] font-semibold uppercase tracking-wider text-text-secondary">Safety Analysis</span>
                <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[0.68rem] font-semibold uppercase tracking-wide border ${analysis.safe ? 'bg-green-bg text-green border-green-border' : 'bg-red-bg text-red border-red-border'}`}>
                    {analysis.safe ? '✓ Safe' : '✗ Blocked'}
                </span>
            </div>
            <div className="p-4">
                {analysis.block_reason && (
                    <div className="flex items-start gap-1.5 px-3 py-2 bg-red-bg border border-red-border rounded-[5px] mb-1.5 text-[0.78rem] text-red">
                        🚫 {analysis.block_reason}
                    </div>
                )}
                {analysis.warnings?.map((w, i) => (
                    <div key={i} className="flex items-start gap-1.5 px-3 py-2 bg-yellow-bg border border-yellow-border rounded-[5px] mb-1.5 text-[0.78rem] text-yellow">
                        ⚠ {w}
                    </div>
                ))}
                {analysis.safe && analysis.warnings?.length === 0 && (
                    <div className="text-green text-[0.82rem]">✅ Query passed all safety checks</div>
                )}
                {analysis.validation_errors?.length > 0 && (
                    <div className="mt-1.5">
                        {analysis.validation_errors.map((e, i) => (
                            <div key={i} className="flex items-start gap-1.5 px-3 py-2 bg-red-bg border border-red-border rounded-[5px] mb-1.5 text-[0.78rem] text-red">
                                ❌ {e}
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    )
}
