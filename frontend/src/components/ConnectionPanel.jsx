export default function ConnectionPanel({ dbType, dbName, connected, schema, onDbTypeChange, onDbNameChange, onConnect }) {
    return (
        <div className="bg-bg-panel border border-border-subtle rounded-xl mb-5 overflow-hidden transition-all duration-300 hover:border-border-default">
            <div className="flex items-center justify-between px-4 py-3 border-b border-border-subtle bg-bg-panel-header">
                <span className="text-[0.72rem] font-semibold uppercase tracking-wider text-text-secondary">Database Connection</span>
                <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[0.68rem] font-semibold uppercase tracking-wide border ${connected ? 'bg-green-bg text-green border-green-border' : 'bg-red-bg text-red border-red-border'}`}>
                    {connected ? '● Connected' : '○ Disconnected'}
                </span>
            </div>
            <div className="p-4">
                <div className="flex items-center gap-2.5 flex-wrap">
                    <select
                        className="w-[100px] bg-bg-input border border-border-default rounded-[5px] text-text-primary px-3 py-2 text-[0.8rem] font-sans transition-colors duration-200 focus:outline-none focus:border-border-focus focus:ring-2 focus:ring-accent-glow"
                        value={dbType}
                        onChange={e => onDbTypeChange(e.target.value)}
                    >
                        <option value="sqlite">SQLite</option>
                        <option value="postgresql">PostgreSQL</option>
                    </select>
                    <input
                        className="flex-1 min-w-[180px] bg-bg-input border border-border-default rounded-[5px] text-text-primary px-3 py-2 text-[0.8rem] font-sans transition-colors duration-200 placeholder:text-text-muted focus:outline-none focus:border-border-focus focus:ring-2 focus:ring-accent-glow"
                        placeholder={dbType === 'sqlite' ? 'Path to .db file (leave empty for :memory:)' : 'database name'}
                        value={dbName}
                        onChange={e => onDbNameChange(e.target.value)}
                    />
                    <button
                        className="inline-flex items-center gap-1.5 px-4 py-2 rounded-[5px] font-sans text-[0.78rem] font-semibold cursor-pointer transition-all duration-200 bg-accent text-[#0b0b0b] hover:bg-accent-hover hover:-translate-y-px disabled:opacity-35 disabled:cursor-not-allowed"
                        onClick={onConnect}
                    >
                        Connect
                    </button>
                </div>
                {schema && (
                    <div className="flex gap-1.5 flex-wrap mt-2.5">
                        {Object.keys(schema).map(t => (
                            <span key={t} className="px-2.5 py-0.5 bg-accent-soft border border-yellow-border rounded-full text-[0.68rem] text-accent font-mono">
                                {t} ({schema[t].length} cols)
                            </span>
                        ))}
                    </div>
                )}
            </div>
        </div>
    )
}
