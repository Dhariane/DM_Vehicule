"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Navbar from "../../../components/Navbar";
import { getToken, authHeaders } from "../../../lib/auth";

type Demande = {
  id: number;
  demandeur: { first_name: string; last_name: string };
  destination: string;
  nombre_passagers: number;
  date_depart: string;
  date_retour: string;
};
type Vehicule = {
  id: number;
  marque: string;
  modele: string;
  immatriculation: string;
  capacite: number;
};
type Chauffeur = { id: number; nom: string; prenom: string };

export default function DashboardLogistique() {
  const [demandes, setDemandes] = useState<Demande[]>([]);
  const [vehicules, setVehicules] = useState<Vehicule[]>([]);
  const [chauffeurs, setChauffeurs] = useState<Chauffeur[]>([]);
  const [loading, setLoading] = useState(true);
  const [assignments, setAssignments] = useState<
    Record<number, { vehicule: string; chauffeur: string }>
  >({});
  const [actionLoading, setActionLoading] = useState<number | null>(null);
  const router = useRouter();

  useEffect(() => {
    if (!getToken()) {
      router.push("/login");
      return;
    }
    Promise.all([
      fetch("http://localhost:8000/api/demandes/?etape=logistique", {
        headers: authHeaders(),
      }).then((r) => r.json()),
      fetch("http://localhost:8000/api/vehicules/?disponible=true", {
        headers: authHeaders(),
      }).then((r) => r.json()),
      fetch("http://localhost:8000/api/chauffeurs/?disponible=true", {
        headers: authHeaders(),
      }).then((r) => r.json()),
    ])
      .then(([d, v, c]) => {
        setDemandes(d);
        setVehicules(v);
        setChauffeurs(c);
      })
      .finally(() => setLoading(false));
  }, []);

  async function handleAssigner(id: number) {
    const a = assignments[id];
    if (!a?.vehicule || !a?.chauffeur) {
      alert("Sélectionnez un véhicule et un chauffeur");
      return;
    }
    setActionLoading(id);
    await fetch(`http://localhost:8000/api/demandes/${id}/assigner/`, {
      method: "PATCH",
      headers: authHeaders(),
      body: JSON.stringify({ vehicule: a.vehicule, chauffeur: a.chauffeur }),
    });
    setActionLoading(null);
    // Recharge
    const res = await fetch(
      "http://localhost:8000/api/demandes/?etape=logistique",
      { headers: authHeaders() },
    );
    setDemandes(await res.json());
  }

  const selectClass =
    "w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm bg-gray-50 focus:outline-none focus:ring-2 focus:ring-[#0B7A5E]/20 focus:border-[#0B7A5E] transition-all";

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-2xl font-semibold text-gray-800">
            Assignation véhicules
          </h1>
          <p className="text-sm text-gray-500 mt-1">
            {demandes.length} demande(s) à traiter
          </p>
        </div>

        {loading ? (
          <div className="text-center py-16 text-gray-400 text-sm">
            Chargement...
          </div>
        ) : demandes.length === 0 ? (
          <div className="bg-white rounded-2xl border border-gray-200 py-16 text-center">
            <p className="text-4xl mb-3">🚗</p>
            <p className="text-gray-500 text-sm">Aucune demande à traiter</p>
          </div>
        ) : (
          <div className="space-y-4">
            {demandes.map((d) => (
              <div
                key={d.id}
                className="bg-white rounded-2xl border border-gray-200 overflow-hidden"
              >
                <div className="px-6 py-4 border-b border-gray-100 flex items-center gap-3">
                  <div className="w-9 h-9 rounded-xl bg-[#E1F5EE] text-[#0B7A5E] flex items-center justify-center font-semibold text-sm">
                    #{d.id}
                  </div>
                  <div>
                    <p className="font-medium text-gray-800 text-sm">
                      {d.demandeur.first_name} {d.demandeur.last_name}
                    </p>
                    <p className="text-xs text-gray-400">
                      {d.destination} · {d.nombre_passagers} passager(s)
                    </p>
                  </div>
                  <span className="ml-auto text-xs bg-blue-50 text-blue-600 border border-blue-200 px-3 py-1 rounded-full">
                    À assigner
                  </span>
                </div>

                <div className="px-6 py-4 grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-medium text-gray-500 mb-1">
                      Véhicule <span className="text-red-500">*</span>
                    </label>
                    <select
                      className={selectClass}
                      value={assignments[d.id]?.vehicule || ""}
                      onChange={(e) =>
                        setAssignments({
                          ...assignments,
                          [d.id]: {
                            ...assignments[d.id],
                            vehicule: e.target.value,
                          },
                        })
                      }
                    >
                      <option value="">Choisir un véhicule...</option>
                      {vehicules
                        .filter((v) => v.capacite >= d.nombre_passagers)
                        .map((v) => (
                          <option key={v.id} value={v.id}>
                            {v.marque} {v.modele} — {v.immatriculation} (
                            {v.capacite} places)
                          </option>
                        ))}
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-gray-500 mb-1">
                      Chauffeur <span className="text-red-500">*</span>
                    </label>
                    <select
                      className={selectClass}
                      value={assignments[d.id]?.chauffeur || ""}
                      onChange={(e) =>
                        setAssignments({
                          ...assignments,
                          [d.id]: {
                            ...assignments[d.id],
                            chauffeur: e.target.value,
                          },
                        })
                      }
                    >
                      <option value="">Choisir un chauffeur...</option>
                      {chauffeurs.map((c) => (
                        <option key={c.id} value={c.id}>
                          {c.prenom} {c.nom}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                <div className="px-6 py-4 border-t border-gray-100 bg-gray-50">
                  <button
                    onClick={() => handleAssigner(d.id)}
                    disabled={actionLoading === d.id}
                    className="w-full bg-[#0B7A5E] hover:bg-[#0a6b52] text-white rounded-xl py-2.5 text-sm font-semibold transition-colors disabled:opacity-60"
                  >
                    {actionLoading === d.id
                      ? "Enregistrement..."
                      : "✓ Confirmer l'assignation"}
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
