"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import Navbar from "../../../components/Navbar";
import { authHeaders } from "../../../lib/auth";

export default function NouvelleDemande() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [form, setForm] = useState({
    motif: "",
    destination: "",
    description: "",
    date_depart: "",
    date_retour: "",
    nombre_passagers: 1,
  });

  function handleChange(
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >,
  ) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await fetch("http://localhost:8000/api/demandes/", {
        method: "POST",
        headers: authHeaders(),
        body: JSON.stringify(form),
      });
      if (!res.ok) {
        setError("Erreur lors de la création");
        return;
      }
      router.push("/dashboard/demandeur");
    } catch {
      setError("Impossible de contacter le serveur");
    } finally {
      setLoading(false);
    }
  }

  const inputClass =
    "w-full border border-gray-200 rounded-xl px-4 py-3 text-sm bg-gray-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-[#0B7A5E]/20 focus:border-[#0B7A5E] transition-all";

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-2xl mx-auto px-4 py-8">
        <button
          onClick={() => router.back()}
          className="text-gray-400 hover:text-gray-600 text-sm mb-6 flex items-center gap-1"
        >
          ← Retour
        </button>

        <div className="bg-white rounded-2xl border border-gray-200 overflow-hidden">
          <div className="bg-[#0B7A5E] px-6 py-5">
            <h1 className="text-white font-semibold text-lg">
              Nouvelle demande de véhicule
            </h1>
            <p className="text-white/70 text-sm mt-0.5">
              Remplissez tous les champs requis
            </p>
          </div>

          <form onSubmit={handleSubmit} className="p-6 space-y-6">
            {/* Section 1 */}
            <div>
              <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3 flex items-center gap-2">
                <span className="w-5 h-5 bg-[#E1F5EE] text-[#0B7A5E] rounded-full flex items-center justify-center text-xs font-bold">
                  1
                </span>
                Informations générales
              </p>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Motif <span className="text-red-500">*</span>
                  </label>
                  <select
                    name="motif"
                    value={form.motif}
                    onChange={handleChange}
                    required
                    className={inputClass}
                  >
                    <option value="">Sélectionner un motif...</option>
                    <option value="mission">Mission terrain</option>
                    <option value="transport">Transport de matériel</option>
                    <option value="deplacement">Déplacement officiel</option>
                    <option value="autre">Autre</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Destination <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    name="destination"
                    value={form.destination}
                    onChange={handleChange}
                    required
                    placeholder="Ex: Fianarantsoa"
                    className={inputClass}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Nombre de passagers <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="number"
                    name="nombre_passagers"
                    value={form.nombre_passagers}
                    onChange={handleChange}
                    required
                    min={1}
                    max={20}
                    className={inputClass}
                  />
                </div>
              </div>
            </div>

            {/* Section 2 */}
            <div>
              <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3 flex items-center gap-2">
                <span className="w-5 h-5 bg-[#E1F5EE] text-[#0B7A5E] rounded-full flex items-center justify-center text-xs font-bold">
                  2
                </span>
                Dates
              </p>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Date départ <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="datetime-local"
                    name="date_depart"
                    value={form.date_depart}
                    onChange={handleChange}
                    required
                    className={inputClass}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Date retour <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="datetime-local"
                    name="date_retour"
                    value={form.date_retour}
                    onChange={handleChange}
                    required
                    className={inputClass}
                  />
                </div>
              </div>
            </div>

            {/* Section 3 */}
            <div>
              <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3 flex items-center gap-2">
                <span className="w-5 h-5 bg-[#E1F5EE] text-[#0B7A5E] rounded-full flex items-center justify-center text-xs font-bold">
                  3
                </span>
                Description
              </p>
              <textarea
                name="description"
                value={form.description}
                onChange={handleChange}
                rows={3}
                placeholder="Décrivez votre besoin (optionnel)"
                className={`${inputClass} resize-none`}
              />
            </div>

            {error && (
              <div className="bg-red-50 text-red-500 text-sm rounded-xl px-4 py-3 text-center">
                {error}
              </div>
            )}

            <div className="flex gap-3 pt-2">
              <button
                type="button"
                onClick={() => router.back()}
                className="flex-1 border border-gray-200 text-gray-600 rounded-xl py-3 text-sm font-medium hover:bg-gray-50 transition-colors"
              >
                Annuler
              </button>
              <button
                type="submit"
                disabled={loading}
                className="flex-1 bg-[#0B7A5E] hover:bg-[#0a6b52] text-white rounded-xl py-3 text-sm font-semibold transition-colors disabled:opacity-60"
              >
                {loading ? "Envoi..." : "Envoyer la demande"}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
