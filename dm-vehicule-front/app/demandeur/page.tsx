"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Navbar from "../../components/Navbar";
import { getToken, authHeaders } from "../../lib/auth";

type Demande = {
  id: number;
  motif: string;
  destination: string;
  date_depart: string;
  statut: "en_attente" | "approuvee" | "rejetee";
};

export default function DashboardDemandeur() {
  const [demandes, setDemandes] = useState<Demande[]>([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    if (!getToken()) {
      router.push("/login");
      return;
    }

    fetch("http://localhost:8000/api/demandes/", { headers: authHeaders() })
      .then((r) => r.json())
      .then((data) => setDemandes(data))
      .finally(() => setLoading(false));
  }, [router]);

  const enAttente = demandes.filter((d) => d.statut === "en_attente").length;
  const approuvees = demandes.filter((d) => d.statut === "approuvee").length;
  const rejetees = demandes.filter((d) => d.statut === "rejetee").length;

  const badge: Record<string, string> = {
    en_attente: "bg-yellow-50 text-yellow-700 border border-yellow-200",
    approuvee: "bg-emerald-50 text-emerald-700 border border-emerald-200",
    rejetee: "bg-red-50 text-red-500 border border-red-200",
  };

  const label: Record<string, string> = {
    en_attente: "En attente",
    approuvee: "Approuvée",
    rejetee: "Rejetée",
  };

  const motifs: Record<string, string> = {
    mission: "Mission terrain",
    transport: "Transport matériel",
    deplacement: "Déplacement officiel",
    autre: "Autre",
  };

  return (
    <div className="relative min-h-screen overflow-hidden bg-[radial-gradient(circle_at_top,_rgba(15,82,58,0.18),_transparent_26%),radial-gradient(circle_at_bottom_right,_rgba(34,197,94,0.16),_transparent_25%),linear-gradient(180deg,#f5f6f6_0%,#eef1f0_100%)]">
      <Navbar />

      <div className="absolute left-[-5rem] top-20 h-56 w-56 rounded-full bg-[#0B7A5E]/20 blur-3xl" />
      <div className="absolute right-[-4rem] top-80 h-64 w-64 rounded-full bg-emerald-300/20 blur-3xl" />
      <div className="absolute left-1/2 top-16 h-40 w-40 -translate-x-1/2 rounded-full bg-white/50 blur-2xl" />

      <main className="relative mx-auto max-w-6xl px-4 pb-16 pt-8 sm:px-6 lg:px-8">
        <section className="mb-8 overflow-hidden rounded-[34px] border border-slate-200/70 bg-white/90 p-6 shadow-[0_24px_90px_-48px_rgba(15,23,42,0.55)] backdrop-blur-sm sm:p-10">
          <div className="flex flex-col gap-8 lg:flex-row lg:items-center lg:justify-between">
            <div className="max-w-2xl">
              <p className="text-xs font-semibold uppercase tracking-[0.3em] text-emerald-700">
                Tableau de bord demandeur
              </p>
              <h1 className="mt-4 text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
                Suivi des demandes de véhicule
              </h1>
              <p className="mt-4 max-w-xl text-sm leading-6 text-slate-600 sm:text-base">
                Un espace clair et moderne pour consulter vos demandes,
                vérifier leurs statuts et créer rapidement une nouvelle demande.
              </p>
            </div>
            <div className="grid gap-4 sm:max-w-md">
              <button
                type="button"
                onClick={() => router.push("/demande/nouvelle")}
                className="inline-flex items-center justify-center rounded-2xl bg-[#166534] px-5 py-3 text-sm font-bold text-white shadow-[0_18px_40px_-26px_rgba(22,101,52,0.8)] transition hover:bg-[#14532d] focus:outline-none focus:ring-4 focus:ring-emerald-200/70"
              >
                + Nouvelle demande
              </button>
              <div className="rounded-[28px] border border-slate-200 bg-[#f8faf9] px-5 py-4 shadow-sm">
                <p className="text-[11px] font-semibold uppercase tracking-[0.3em] text-slate-500">
                  Unité de Coordination des Projets
                </p>
                <p className="mt-3 text-lg font-semibold text-slate-900">
                  Front-end amélioré
                </p>
              </div>
            </div>
          </div>
        </section>

        <section className="grid gap-4 md:grid-cols-3 mb-8">
          {[
            { value: enAttente, title: "En attente", accent: "text-yellow-600", description: "Demandes en attente" },
            { value: approuvees, title: "Approuvées", accent: "text-emerald-700", description: "Demandes validées" },
            { value: rejetees, title: "Rejetées", accent: "text-red-600", description: "Demandes refusées" },
          ].map((item) => (
            <div
              key={item.title}
              className="overflow-hidden rounded-[28px] border border-slate-200 bg-white/95 p-5 shadow-[0_18px_50px_-32px_rgba(15,23,42,0.28)]"
            >
              <p className={`text-4xl font-bold ${item.accent}`}>{item.value}</p>
              <p className="mt-3 text-sm font-semibold text-slate-700">{item.title}</p>
              <p className="mt-2 text-sm text-slate-500">{item.description}</p>
            </div>
          ))}
        </section>

        <section className="overflow-hidden rounded-[34px] border border-slate-200 bg-white/95 shadow-[0_24px_80px_-40px_rgba(15,23,42,0.34)]">
          <div className="flex items-center justify-between border-b border-slate-100 px-6 py-5 sm:px-8">
            <div>
              <p className="text-sm font-semibold text-slate-900">Historique des demandes</p>
              <p className="mt-1 text-xs text-slate-500">
                Dernières demandes et statuts en temps réel.
              </p>
            </div>
            <button
              type="button"
              onClick={() => router.push("/demande/nouvelle")}
              className="rounded-2xl bg-emerald-50 px-4 py-2 text-xs font-semibold text-emerald-700 transition hover:bg-emerald-100"
            >
              Créer une demande
            </button>
          </div>

          {loading ? (
            <div className="px-6 py-16 text-center text-slate-400 sm:px-8">
              Chargement...
            </div>
          ) : demandes.length === 0 ? (
            <div className="px-6 py-16 text-center sm:px-8">
              <p className="text-sm text-slate-500">Aucune demande pour le moment.</p>
              <button
                onClick={() => router.push("/demande/nouvelle")}
                className="mt-4 rounded-2xl bg-[#0B7A5E] px-4 py-2 text-sm font-semibold text-white transition hover:bg-[#14532d]"
              >
                Créer ma première demande
              </button>
            </div>
          ) : (
            <div className="divide-y divide-slate-100">
              {demandes.map((d) => (
                <div key={d.id} className="flex flex-col gap-4 px-6 py-5 sm:flex-row sm:items-center sm:justify-between sm:px-8">
                  <div className="flex items-center gap-4 min-w-0">
                    <div className="flex h-12 w-12 items-center justify-center rounded-3xl bg-emerald-50 text-emerald-700 font-semibold shadow-sm">
                      #{d.id}
                    </div>
                    <div className="min-w-0">
                      <p className="truncate text-sm font-semibold text-slate-900">{d.destination}</p>
                      <p className="mt-1 text-xs text-slate-500">
                        {motifs[d.motif] || d.motif} · {new Date(d.date_depart).toLocaleDateString("fr-FR")}
                      </p>
                    </div>
                  </div>
                  <span className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${badge[d.statut]}`}>
                    {label[d.statut]}
                  </span>
                </div>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
