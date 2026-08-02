import { navItems, appName } from '../data/system';

const githubUrl = 'https://github.com/prapti-gupta-1805';
const linkedinUrl = 'https://www.linkedin.com/in/prapti-gupta/';

function GitHubIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden>
      <path d="M12 .5C5.73.5.5 5.73.5 12c0 5.08 3.29 9.39 7.86 10.91.58.11.79-.25.79-.56 0-.28-.01-1.02-.02-2-3.2.7-3.88-1.54-3.88-1.54-.53-1.36-1.3-1.72-1.3-1.72-1.06-.72.08-.71.08-.71 1.18.08 1.8 1.21 1.8 1.21 1.04 1.78 2.73 1.27 3.4.97.11-.76.41-1.27.75-1.56-2.56-.29-5.26-1.28-5.26-5.7 0-1.26.45-2.3 1.2-3.11-.12-.29-.52-1.46.11-3.05 0 0 .98-.31 3.2 1.19a11.1 11.1 0 0 1 2.92-.39c.99 0 1.99.13 2.92.39 2.22-1.5 3.2-1.19 3.2-1.19.63 1.59.23 2.76.11 3.05.75.81 1.2 1.85 1.2 3.11 0 4.43-2.7 5.4-5.27 5.69.42.36.8 1.07.8 2.16 0 1.56-.01 2.82-.01 3.2 0 .31.21.68.8.56C20.71 21.39 24 17.08 24 12c0-6.27-5.23-11.5-12-11.5z" />
    </svg>
  );
}

function LinkedInIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden>
      <path d="M20.45 20.45h-3.56v-5.4c0-1.29-.02-2.95-1.8-2.95-1.8 0-2.07 1.4-2.07 2.85v5.5H9.5V9.5h3.42v1.5h.05c.48-.9 1.66-1.85 3.42-1.85 3.66 0 4.34 2.4 4.34 5.52v6.78zM5.34 8c-1.14 0-2.06-.92-2.06-2.06 0-1.14.92-2.06 2.06-2.06 1.14 0 2.06.92 2.06 2.06 0 1.14-.92 2.06-2.06 2.06zM7.12 20.45H3.56V9.5h3.56v10.95z" />
    </svg>
  );
}

export default function Footer() {
  return (
    <footer className="border-t border-slate-800/80 bg-slate-950/90 text-slate-400">
      <div className="mx-auto flex w-full max-w-7xl flex-col gap-4 px-4 py-8 sm:px-6 lg:flex-row lg:items-center lg:justify-between lg:px-8">
        <div className="flex flex-col gap-1 text-sm">
          <span className="text-slate-300 font-semibold">{appName}</span>
          <span className="text-slate-500">AI-powered Pipeline Monitoring</span>
        </div>

        <div className="flex items-center gap-4">
          {navItems.map(({ to, label }) => (
            <a key={to} href={to} className="text-slate-300 text-sm transition hover:text-white">
              {label}
            </a>
          ))}
        </div>

        <div className="flex items-center gap-3">
          <span className="text-sm text-slate-300">Prapti Gupta</span>
          <a href={linkedinUrl} target="_blank" rel="noreferrer" aria-label="LinkedIn" className="text-slate-400 transition hover:text-white">
            <LinkedInIcon />
          </a>
          <a href={githubUrl} target="_blank" rel="noreferrer" aria-label="GitHub" className="text-slate-400 transition hover:text-white">
            <GitHubIcon />
          </a>
        </div>
      </div>

      <div className="border-t border-slate-800/70 bg-slate-950/90">
        <div className="mx-auto flex w-full max-w-7xl items-center justify-between gap-4 px-4 py-3 text-sm text-slate-500 sm:px-6 lg:px-8">
          <span>© 2026 SCADA Pipeline Intelligence System</span>
          <span>Built with React • FastAPI</span>
        </div>
      </div>
    </footer>
  );
}
