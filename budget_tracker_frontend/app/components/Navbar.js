"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Navbar() {
  const pathname = usePathname();

  const links = [
    { href: "/dashboard", label: "Dashboard" },
    { href: "/transactions", label: "Transactions" },
    { href: "/categories", label: "Categories" },
    { href: "/budgets", label: "Budgets" },
  ];

  return (
    <nav style={{
      background: "#1e293b",
      padding: "0 2rem",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      height: "64px",
      position: "sticky",
      top: 0,
      zIndex: 100,
    }}>
     
     <Link href="/" style={{ color: "white", fontWeight: "bold", fontSize: "1.2rem", textDecoration: "none" }}>
  Marys Budget Tracker
</Link>

      <div style={{ display: "flex", gap: "0.5rem" }}>
        {links.map((link) => (
          <Link
            key={link.href}
            href={link.href}
            style={{
              padding: "0.5rem 1rem",
              borderRadius: "8px",
              textDecoration: "none",
              color: pathname === link.href ? "white" : "#94a3b8",
              background: pathname === link.href ? "#6366f1" : "transparent",
              fontWeight: pathname === link.href ? "bold" : "normal",
              fontSize: "0.9rem",
            }}
          >
            {link.label}
          </Link>
        ))}
      </div>

      <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
        <Link
          href="/login"
          style={{
            color: "#94a3b8",
            textDecoration: "none",
            fontSize: "0.9rem",
          }}
        >
          Login
        </Link>
        <Link
          href="/register"
          style={{
            background: "#6366f1",
            color: "white",
            padding: "0.5rem 1rem",
            borderRadius: "8px",
            textDecoration: "none",
            fontSize: "0.9rem",
          }}
        >
          Register
        </Link>
      </div>
    </nav>
  );
}