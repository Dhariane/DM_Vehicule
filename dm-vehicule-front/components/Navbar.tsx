"use client";
import { getUser, logout } from "../lib/auth";

export default function Navbar() {
  const user = getUser();
  const roleLabel: Record<string, string> = {
    Demandeur: "Demandeur",
    Chef: "Chef Direct",
    Logistique: "Responsable Logistique",
  };

  return (
    <nav className="bg-[#0B7A5E] text-white px-6 py-4 flex items-center justify-between shadow-sm">
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 bg-white/15 rounded-xl flex items-center justify-center text-lg">
          🚗
        </div>
        <div>
          <p className="font-semibold text-sm leading-tight">
            UCP — Gestion Véhicules
          </p>
          <p className="text-xs text-white/70 leading-tight">
            {user?.first_name || user?.username} ·{" "}
            {roleLabel[user?.role] || user?.role}
          </p>
        </div>
      </div>
      <button
        onClick={logout}
        className="text-xs bg-white/10 hover:bg-white/20 border border-white/20 px-4 py-2 rounded-lg transition-colors"
      >
        Déconnexion
      </button>
    </nav>
  );
}
