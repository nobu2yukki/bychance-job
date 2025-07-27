import ClientProviders from "@/components/ClientProviders";
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "byChance-job",
  description: "直感的な求人マッチングアプリ",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ja">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <ClientProviders>
          <div className="mobile-only">
            {children}
          </div>
          <div className="desktop-only">
            <div className="flex items-center justify-center min-h-screen bg-gray-100">
              <div className="text-center p-8 bg-white rounded-lg shadow-lg">
                <h1 className="text-2xl font-bold mb-4">📱 スマートフォンでアクセスしてください</h1>
                <p className="text-gray-600">このアプリはスマートフォン専用です。<br />スマートフォンからアクセスしてご利用ください。</p>
              </div>
            </div>
          </div>
        </ClientProviders>
      </body>
    </html>
  );
}
