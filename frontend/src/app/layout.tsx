import type { Metadata, Viewport } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Perplexity Clone - AI-Powered Search Assistant',
  description: 'Your AI-powered search assistant that understands context and provides intelligent answers. Search the web, get AI-powered insights, and discover information faster.',
  keywords: 'AI search, artificial intelligence, search engine, machine learning, web search, AI assistant',
  authors: [{ name: 'Perplexity Clone Team' }],
  robots: 'index, follow',
  openGraph: {
    title: 'Perplexity Clone - AI-Powered Search Assistant',
    description: 'Your AI-powered search assistant that understands context and provides intelligent answers.',
    type: 'website',
    locale: 'en_US',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Perplexity Clone - AI-Powered Search Assistant',
    description: 'Your AI-powered search assistant that understands context and provides intelligent answers.',
  },
}

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        {children}
      </body>
    </html>
  )
}
