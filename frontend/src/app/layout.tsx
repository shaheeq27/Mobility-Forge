import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = { title: "MobilityForge | Urban Mobility Intelligence", description: "Building Better Mobility Systems." };
export default function RootLayout({ children }: LayoutProps<"/">) {
  const init = `(()=>{try{const s=localStorage.getItem('mobilityforge-theme');const t=s==='light'||s==='dark'?s:(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light');document.documentElement.dataset.theme=t;document.documentElement.style.colorScheme=t}catch(_){}})()`;
  return <html lang="en" suppressHydrationWarning><head><script dangerouslySetInnerHTML={{ __html: init }} /></head><body>{children}</body></html>;
}
