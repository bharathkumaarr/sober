export default function QueryEditor({ query, connected, safe, analyzing, executing, onChange, onAnalyze, onExecute, onFetchLogs }) {
    return (
        <div className="bg-bg-panel border border-border-subtle rounded-xl mb-5 overflow-hidden transition-all duration-300 hover:border-border-default">
            <div className="flex items-center justify-between px-4 py-3 border-b border-border-subtle bg-bg-panel-header">
                <span className="text-[0.72rem] font-semibold uppercase tracking-wider text-text-secondary">Query Editor</span>
            </div>
            <div className="p-4">
                <textarea
                    className="w-full min-h-[110px] bg-bg-input border border-border-default rounded-lg text-text-primary px-4 py-3.5 font-mono text-[0.82rem] leading-[1.7] resize-y transition-all duration-200 placeholder:text-text-muted focus:outline-none focus:border-border-focus focus:ring-2 focus:ring-accent-glow"
                    placeholder="SELECT id, name FROM users WHERE id = 1;"
                    value={query}
                    onChange={e => onChange(e.target.value)}
                    onKeyDown={e => { if (e.key === 'Enter' && e.metaKey) onAnalyze() }}
                />
                <div className="flex gap-2.5 mt-3.5">
                    <button
                        className="inline-flex items-center gap-1.5 px-4 py-2 rounded-[5px] font-sans text-[0.78rem] font-semibold cursor-pointer transition-all duration-200 bg-accent text-[#0b0b0b] hover:bg-accent-hover hover:-translate-y-px disabled:opacity-35 disabled:cursor-not-allowed"
                        onClick={onAnalyze}
                        disabled={!connected || !query.trim() || analyzing}
                    >
                        {analyzing ? <><span className="inline-block w-3.5 h-3.5 border-2 border-black/15 border-t-current rounded-full animate-spin" /> Analyzing...</> : '🔍 Analyze'}
                    </button>
                    <button
                        className="inline-flex items-center gap-1.5 px-4 py-2 rounded-[5px] font-sans text-[0.78rem] font-semibold cursor-pointer transition-all duration-200 bg-green text-[#0b0b0b] hover:-translate-y-px hover:brightness-110 disabled:opacity-35 disabled:cursor-not-allowed"
                        onClick={onExecute}
                        disabled={!connected || !safe || executing}
                    >
                        {executing ? <><span className="inline-block w-3.5 h-3.5 border-2 border-black/15 border-t-current rounded-full animate-spin" /> Executing...</> : '▶ Execute'}
                    </button>
                    <button
                        className="inline-flex items-center gap-1.5 px-4 py-2 rounded-[5px] font-sans text-[0.78rem] font-semibold cursor-pointer transition-all duration-200 bg-bg-hover text-text-primary border border-border-default hover:border-accent hover:text-accent disabled:opacity-35 disabled:cursor-not-allowed"
                        onClick={onFetchLogs}
                        disabled={!connected}
                    >
                        📋 Logs
                    </button>
                </div>
            </div>
        </div>
    )
}
