"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Navbar from "../../../components/Navbar";
import { getToken, authHeaders } from "../../../lib/auth";

type Demande = {
  id: number;
  demandeur: { username: string; first_name: string; last_name: string };
  motif: string;
  destination: string;
  date_depart: string;
  date_retour: string;
  nombre_passagers: number;
  description: string;
};

export default function DashboardChef() {
  const [demandes, setDemandes] = useState<Demande[]>([]);
  const [loading, setLoading] = useState(true);
  const [commentaires, setCommentaires] = useState<Record<number, string>>({});
  const [actionLoading, setActionLoading] = useState<number | null>(null);
  const router = useRouter();

  useEffect(() => {
    if (!getToken()) {
      router.push("/login");
      return;
    }
    fetchDemandes();
  }, []);

  async function fetchDemandes() {
    const res = await fetch(
      "http://localhost:8000/api/demandes/?etape=chef&statut=en_attente",
      { headers: authHeaders() },
    );
    setDemandes(await res.json());
    setLoading(false);
  }

  async function handleDecision(id: number, decision: "approuve" | "rejete") {
    setActionLoading(id);
    await fetch(`http://localhost:8000/api/demandes/${id}/valider/`, {
      method: "PATCH",
      headers: authHeaders(),
      body: JSON.stringify({ decision, commentaire: commentaires[id] || "" }),
    });
    setActionLoading(null);
    fetchDemandes();
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-2xl font-semibold text-gray-800">
            Demandes à valider
          </h1>
          <p className="text-sm text-gray-500 mt-1">
            {demandes.length} demande(s) en attente
          </p>
        </div>

        {loading ? (
          <div className="text-center py-16 text-gray-400 text-sm">
            Chargement...
          </div>
        ) : demandes.length === 0 ? (
          <div className="bg-white rounded-2xl border border-gray-200 py-16 text-center">
            <p className="text-4xl mb-3">✅</p>
            <p className="text-gray-500 text-sm">Aucune demande en attente</p>
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
                      {d.demandeur.first_name}{" "}
                      {d.demandeur.last_name || d.demandeur.username}
                    </p>
                    <p className="text-xs text-gray-400">{d.destination}</p>
                  </div>
                  <span className="ml-auto text-xs bg-yellow-50 text-yellow-700 border border-yellow-200 px-3 py-1 rounded-full">
                    En attente
                  </span>
                </div>

                <div className="px-6 py-4 grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-xs text-gray-400 mb-0.5">Départ</p>
                    <p className="font-medium text-gray-700">
                      {new Date(d.date_depart).toLocaleDateString("fr-FR")}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-400 mb-0.5">Retour</p>
                    <p className="font-medium text-gray-700">
                      {new Date(d.date_retour).toLocaleDateString("fr-FR")}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-400 mb-0.5">Passagers</p>
                    <p className="font-medium text-gray-700">
                      {d.nombre_passagers}
                    </p>
                  </div>
                  {d.description && (
                    <div className="col-span-2">
                      <p className="text-xs text-gray-400 mb-0.5">
                        Description
                      </p>
                      <p className="text-gray-700">{d.description}</p>
                    </div>
                  )}
                </div>

                <div className="px-6 py-4 bg-gray-50 border-t border-gray-100">
                  <textarea
                    placeholder="Commentaire (optionnel)..."
                    value={commentaires[d.id] || ""}
                    onChange={(e) =>
                      setCommentaires({
                        ...commentaires,
                        [d.id]: e.target.value,
                      })
                    }
                    rows={2}
                    className="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-[#0B7A5E]/20 focus:border-[#0B7A5E] transition-all resize-none mb-3"
                  />
                  <div className="flex gap-3">
                    <button
                      onClick={() => handleDecision(d.id, "rejete")}
                      disabled={actionLoading === d.id}
                      className="flex-1 border border-red-200 text-red-500 hover:bg-red-50 rounded-xl py-2.5 text-sm font-medium transition-colors disabled:opacity-50"
                    >
                      ✗ Rejeter
                    </button>
                    <button
                      onClick={() => handleDecision(d.id, "approuve")}
                      disabled={actionLoading === d.id}
                      className="flex-1 bg-[#0B7A5E] hover:bg-[#0a6b52] text-white rounded-xl py-2.5 text-sm font-semibold transition-colors disabled:opacity-50"
                    >
                      ✓ Valider
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
