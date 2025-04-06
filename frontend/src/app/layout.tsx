import "./globals.css";
import { Inter } from "next/font/google";
import { FirebaseProvider } from "@/lib/firebase/FirebaseContext";
import Header from "./components/Header";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} font-sans antialiased min-h-screen`} style={{ backgroundColor: '#F9F4F2' }}>
        <FirebaseProvider>
          <Header />
          <main>
            {children}
          </main>
        </FirebaseProvider>
      </body>
    </html>
  );
}
