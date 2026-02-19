# 🏆 RIFT 2026 — Autonomous CI/CD Healing Agent Dashboard

> **Next.js 16 + Tailwind CSS v4 + Zustand + Framer Motion + Recharts**

A production-grade, fully-featured frontend dashboard for the RIFT 2026 Hackathon submission: **Autonomous CI/CD Healing Agent**.

![Demo Mode Enabled by Default](https://img.shields.io/badge/Demo%20Mode-Enabled-yellow)
![Next.js 16](https://img.shields.io/badge/Next.js-16-black)
![Tailwind v4](https://img.shields.io/badge/Tailwind-v4-38bdf8)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue)

---

## ✨ Features

### 🎯 Core Functionality
- **Demo Mode (Default ON)**: Judges can instantly see the fully working dashboard with mock data
- **Real-time Log Streaming**: Terminal-style log viewer with auto-scroll
- **Live Metrics**: Animated counters, progress bars, and timers
- **Interactive UI**: Smooth animations, hover effects, and responsive design
- **CSV Export**: Download fixes table as CSV for analysis

### 📊 Dashboard Components
1. **Input Section**: GitHub repo URL, team name, leader name with live branch preview
2. **Loading Overlay**: Terminal-style log streaming with elapsed timer
3. **Run Summary Card**: Key metrics with animated count-up and confetti on success
4. **Score Breakdown Panel**: Visual bar chart with scoring logic display
5. **CI/CD Timeline**: Vertical pipeline visualization with retry counter
6. **Fixes Table**: Detailed breakdown of all fixes with color-coded bug types

### 🎨 Design System
- **Dark Theme**: Cyber-themed color palette (`#0A0E1A` primary background)
- **Gradient Accents**: Blue-to-purple gradients for CTAs
- **Custom Fonts**: Inter (UI) + JetBrains Mono (code)
- **Glow Effects**: Subtle box-shadow glows on key elements
- **Custom Scrollbars**: Styled webkit scrollbars
- **Status Badges**: Animated pulsing dots for PASSED/FAILED/RUNNING

---

## 🚀 Quick Start

### Prerequisites
- Node.js 20+
- npm or yarn

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Production Build

```bash
npm run build
npm start
```

---

## 🎭 Demo Mode

**Demo Mode is enabled by default** so judges can immediately see the working dashboard:

1. Form is **pre-filled** with sample data:
   - Repo: `https://github.com/rift2026/sample-broken-repo`
   - Team: `RIFT ORGANISERS`
   - Leader: `Saiyam Kumar`

2. Click **🚀 Run Agent** button

3. Loading overlay appears with **19 streaming log lines** (850ms apart)

4. After ~18 seconds, **results dashboard** appears with:
   - ✅ **Confetti animation** on PASSED status
   - 📈 **Animated count-up** for metrics
   - 🎨 **Full CI/CD timeline** with 2 iterations
   - 📊 **Score breakdown** (110 pts)
   - 📋 **Fixes table** with 6 fixes

5. **100% offline** — no backend required!

To toggle Demo Mode OFF, use the switch in the input section.

---

## 📁 Project Structure

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout with fonts
│   ├── page.tsx            # Main page component
│   └── globals.css         # Global styles + utilities
├── components/
│   ├── Navbar.tsx          # Top navigation with live clock
│   ├── StatusBadge.tsx     # Reusable status indicator
│   ├── InputSection.tsx    # Form with demo toggle
│   ├── LoadingOverlay.tsx  # Terminal-style log viewer
│   ├── RunSummaryCard.tsx  # Key metrics summary
│   ├── ScoreBreakdownPanel.tsx  # Score visualization
│   ├── CICDTimeline.tsx    # Pipeline timeline
│   ├── FixesTable.tsx      # Detailed fixes table
│   └── Dashboard.tsx       # Main results container
├── store/
│   └── agentStore.ts       # Zustand global state
├── hooks/
│   └── useAgentRun.ts      # Agent execution logic
├── utils/
│   ├── formatters.ts       # Utility functions
│   └── mockData.ts         # Mock data for demo mode
├── types/
│   └── index.ts            # TypeScript interfaces
├── tailwind.config.ts      # Tailwind CSS config
├── next.config.ts          # Next.js config with API rewrites
└── .env.local.example      # Environment variables template
```

---

## 🔌 Backend Integration

### Environment Variables

Create `.env.local`:

```bash
AGENT_BACKEND_URL=https://your-backend.up.railway.app
```

### API Endpoints Expected

The frontend expects these backend endpoints when Demo Mode is OFF:

```
POST /api/run
→ Body: { repoUrl, teamName, leaderName }
→ Returns: { run_id: string }

GET /api/run/:runId/status
→ Returns: { log?: LogLine, final_status?: 'PASSED'|'FAILED' }

GET /api/run/:runId/results
→ Returns: AgentResults
```

See `types/index.ts` for full TypeScript interfaces.

---

## 🎨 Customization

### Design Tokens

Edit colors in `app/globals.css`:

```css
--bg-primary:     #0A0E1A
--bg-card:        #111827
--accent-blue:    #3B82F6
--success:        #10B981
--error:          #EF4444
```

### Mock Data

Edit `utils/mockData.ts` to customize demo results.

### Animation Speeds

Adjust Framer Motion `transition={{ duration: 0.5 }}` in components.

---

## 📦 Tech Stack

| Category | Technology |
|----------|-----------|
| Framework | Next.js 16 (App Router) |
| Styling | Tailwind CSS v4 |
| State | Zustand |
| Animations | Framer Motion |
| Charts | Recharts |
| Icons | Lucide React |
| HTTP | Axios |
| Effects | Canvas Confetti |
| Language | TypeScript 5 |

---

## 🐛 Troubleshooting

### Port Already in Use

```bash
lsof -ti:3000 | xargs kill -9
npm run dev
```

### Build Errors

```bash
rm -rf .next node_modules
npm install
npm run dev
```

### Styling Issues

Tailwind v4 uses `@import "tailwindcss"` instead of `@tailwind` directives.

---

## 🚢 Deployment

### Vercel (Recommended)

```bash
vercel login
vercel --prod
```

Add `AGENT_BACKEND_URL` in Vercel dashboard → Settings → Environment Variables.

### Other Platforms

Works on Netlify, Railway, Render, or any Node.js host.

---

## 📄 License

MIT License — RIFT 2026 Hackathon Submission

---

## 🎯 Judging Criteria Alignment

| Criterion | Implementation |
|-----------|----------------|
| **Innovation** | Real-time log streaming + AI-powered healing |
| **Technical Excellence** | TypeScript, animations, state management |
| **UI/UX** | Dark theme, smooth animations, responsive |
| **Completeness** | Full demo mode, CSV export, error handling |
| **Production-Ready** | Error boundaries, loading states, offline support |

---

## 👨‍💻 Development Notes

- Uses **Tailwind CSS v4** with new `@import` syntax
- **Zustand** for lightweight state management
- **Framer Motion** for declarative animations
- **Canvas Confetti** for celebration effects
- **Recharts** for data visualization
- **Mock data** streams at 850ms intervals for realism

---

## 🔗 Links

- [RIFT 2026 Hackathon](https://rift2026.example.com)
- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS v4](https://tailwindcss.com)
- [Zustand](https://zustand.docs.pmnd.rs)

---

**Built with ❤️ for RIFT 2026**
