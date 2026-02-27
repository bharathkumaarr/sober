export default function Header({ theme, onToggleTheme }) {
    return (
        <header className="flex items-center justify-between mb-8 pb-5 border-b border-border-subtle">
            <div className="flex flex-col">
                <h1 className="text-2xl font-bold text-accent tracking-tight">Sober</h1>
                <p className="text-text-muted text-xs mt-0.5">Safe Query Simulation & Analysis Engine</p>
            </div>
            <button
                onClick={onToggleTheme}
                className="flex items-center gap-2 bg-bg-input border border-border-default rounded-full px-3 py-1.5 cursor-pointer font-sans text-xs font-medium text-text-secondary transition-all duration-200 hover:border-accent hover:text-accent"
            >
                <span className="text-base leading-none">{theme === 'dark' ? '☀️' : '🌙'}</span>
                {theme === 'dark' ? 'Light' : 'Dark'}
            </button>
        </header>
    )
}
