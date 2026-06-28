export default function Footer() {
  return (
    <footer style={{
      background: "#1e293b",
      color: "#94a3b8",
      textAlign: "center",
      padding: "2rem",
      fontFamily: "sans-serif",
      fontSize: "0.9rem",
    }}>
      <p style={{ margin: "0 0 0.5rem" }}>
        Marys Budget Tracker. Made with love by Macharia
      </p>
      <p style={{ margin: 0, fontSize: "0.8rem" }}>
        © {new Date().getFullYear()} Mary. All rights reserved.
      </p>
    </footer>
  );
}