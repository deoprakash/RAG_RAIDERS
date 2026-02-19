import type { Metadata } from 'next';
import { Inter, JetBrains_Mono } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' });
const mono = JetBrains_Mono({ subsets: ['latin'], variable: '--font-mono' });

export const metadata: Metadata = {
  title: 'RIFT 2026 — Autonomous CI/CD Healing Agent',
  description: 'Autonomous DevOps Agent Dashboard — RIFT 2026 Hackathon',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${inter.variable} ${mono.variable}`}>
      <body className="bg-[#0A0E1A] text-[#F9FAFB] font-sans antialiased min-h-screen">
        {children}
      </body>
    </html>
  );
}
