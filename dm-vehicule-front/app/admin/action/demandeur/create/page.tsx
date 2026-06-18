"use client";

import  { useState, useEffect, ChangeEvent, FormEvent } from 'react';
import Image from 'next/image';

interface DemandeurFormData {
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  password: string;
  role: 'Demandeur' | 'Chef' | 'Logistique' | 'Directeur';
  telephone: string;
  service: string;
  poste: string;
  chef_direct: string;
}

interface ChefOption {
  id: number;
  username: string;
  first_name?: string;
  last_name?: string;
}
export default function RegisterDemandeur() {
  const [formData, setFormData] = useState<DemandeurFormData>({
    username: '',
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    role: 'Demandeur',
    telephone: '',
    service: '',
    poste: '',
    chef_direct: ''
  });

  const [chefs, setChefs] = useState<ChefOption[]>([]);
  const [showPassword, setShowPassword] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<boolean>(false);

  useEffect(() => {
    fetch(`${vehicule_api}/demandeurs/?role=Chef`)
      .then((res) => res.json())
      .then((data: ChefOption[]) => setChefs(data))
      .catch((err) => console.error("Erreur lors de la récupération des chefs:", err));
  }, []);

  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value
    }));
  };

  const handleRegister = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);

    const dataToSend = {
      ...formData,
      chef_direct: formData.chef_direct === "" ? null : parseInt(formData.chef_direct, 10)
    };

    try {
      const response = await fetch(`${vehicule_api}/demandeurs/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(dataToSend)
      });

      const data = await response.json();

      if (!response.ok) {
        if (data && typeof data === 'object') {
          const firstKey = Object.keys(data)[0];
          const errorMessage = Array.isArray(data[firstKey]) ? data[firstKey][0] : data[firstKey];
          throw new Error(`${firstKey}: ${errorMessage}`);
        }
        throw new Error("Une erreur est survenue.");
      }

      setSuccess(true);
      setFormData({
        username: '', first_name: '', last_name: '', email: '', password: '',
        role: 'Demandeur', telephone: '', service: '', poste: '', chef_direct: ''
      });
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Une erreur inconnue s'est produite.");
      }
    } finally {
      setLoading(false);
    }
  };

  // Styles Tailwind réutilisables
  const inputStyle = "w-full rounded-xl border border-slate-200 bg-slate-50/60 px-4 py-2.5 text-sm text-slate-900 placeholder:text-slate-400 outline-none transition focus:border-emerald-400 focus:bg-white focus:ring-2 focus:ring-emerald-100";
  const labelStyle = "block text-xs font-semibold text-slate-700 mb-1";

  return (
    <>
      <div className="fixed inset-0 -z-10 bg-[#eaeceb] overflow-hidden pointer-events-none">
        <div className="absolute top-[-8rem] left-1/2 -translate-x-1/2 h-[30rem] w-[30rem] rounded-full bg-emerald-400/10 blur-3xl" />
        <div className="absolute bottom-[-6rem] right-[-5rem] h-64 w-64 rounded-full bg-emerald-500/10 blur-3xl" />
        <div className="absolute bottom-[-4rem] left-[-4rem] h-52 w-52 rounded-full bg-[#0B7A5E]/10 blur-3xl" />
      </div>

      <main className="min-h-screen flex items-center justify-center px-4 py-10">
        <div className="w-full max-w-[650px]">
          <div className="overflow-hidden rounded-3xl bg-white shadow-[0_16px_56px_-12px_rgba(0,0,0,0.16),0_0_0_1px_rgba(16,185,129,0.12)]">
            <div className="h-[3px] bg-gradient-to-r from-emerald-300/40 via-emerald-500 to-emerald-300/40" />

            <div className="px-6 py-8 sm:px-10">
              <div className="flex justify-center mb-4">
                <div className="relative flex h-[64px] w-[64px] items-center justify-center rounded-2xl bg-gradient-to-br from-white to-slate-50 shadow-md ring-1 ring-slate-200">
                  <span className="absolute -top-1 -right-1 h-2.5 w-2.5 rounded-full bg-emerald-500 ring-2 ring-white" />
                  <Image
                    src="/ucp-sante-logo-color.png"
                    alt="Logo UCP"
                    width={48}
                    height={48}
                    className="object-contain"
                    priority
                  />
                </div>
              </div>

              {/* ── En-tête ── */}
              <div className="text-center mb-6">
                <p className="text-[10px] font-bold uppercase tracking-[0.28em] text-emerald-700 mb-1">
                  Gestion des Véhicules
                </p>
                <h1 className="text-[26px] font-bold tracking-tight text-slate-900">
                  Création de Compte
                </h1>
                <div className="mt-2 mx-auto h-px w-12 bg-gradient-to-r from-transparent via-emerald-400 to-transparent" />
              </div>

              {error && (
                <div className="mb-5 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">
                  {error}
                </div>
              )}

              {success && (
                <div className="mb-5 rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-800">
                  Le compte demandeur a été créé avec succès !
                </div>
              )}

              <form onSubmit={handleRegister} className="space-y-4">
                
                {/* Ligne 1 : Identifiant & Password */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className={labelStyle}>Nom d utilisateur *</label>
                    <input
                      type="text"
                      name="username"
                      value={formData.username}
                      onChange={handleChange}
                      placeholder="Identifiant unique"
                      required
                      className={inputStyle}
                    />
                  </div>
                  <div>
                    <label className={labelStyle}>Mot de passe *</label>
                    <div className="relative">
                      <input
                        type={showPassword ? "text" : "password"}
                        name="password"
                        value={formData.password}
                        onChange={handleChange}
                        placeholder="Min. 6 caractères"
                        required
                        className={`${inputStyle} pr-11`}
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-3 top-1/2 -translate-y-1/2 flex h-7 w-7 items-center justify-center rounded-lg text-slate-400 hover:text-emerald-600 transition"
                      >
                        {showPassword ? (
                          <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                            <path strokeLinecap="round" strokeLinejoin="round" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                          </svg>
                        ) : (
                          <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                            <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                            <path strokeLinecap="round" strokeLinejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                          </svg>
                        )}
                      </button>
                    </div>
                  </div>
                </div>

                {/* Ligne 2 : Prénom & Nom */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className={labelStyle}>Prénom</label>
                    <input
                      type="text"
                      name="first_name"
                      value={formData.first_name}
                      onChange={handleChange}
                      placeholder="Votre prénom"
                      className={inputStyle}
                    />
                  </div>
                  <div>
                    <label className={labelStyle}>Nom</label>
                    <input
                      type="text"
                      name="last_name"
                      value={formData.last_name}
                      onChange={handleChange}
                      placeholder="Votre nom"
                      className={inputStyle}
                    />
                  </div>
                </div>

                {/* Ligne 3 : Email & Téléphone */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className={labelStyle}>Email *</label>
                    <input
                      type="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      placeholder="exemple@ucp.sante"
                      required
                      className={inputStyle}
                    />
                  </div>
                  <div>
                    <label className={labelStyle}>Téléphone</label>
                    <input
                      type="tel"
                      name="telephone"
                      value={formData.telephone}
                      onChange={handleChange}
                      placeholder="Numéro de contact"
                      className={inputStyle}
                    />
                  </div>
                </div>

                {/* Ligne 4 : Service & Poste */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className={labelStyle}>Service</label>
                    <input
                      type="text"
                      name="service"
                      value={formData.service}
                      onChange={handleChange}
                      placeholder="Ex: Logistique, RH..."
                      className={inputStyle}
                    />
                  </div>
                  <div>
                    <label className={labelStyle}>Poste occupé</label>
                    <input
                      type="text"
                      name="poste"
                      value={formData.poste}
                      onChange={handleChange}
                      placeholder="Ex: Chauffeur, Manager..."
                      className={inputStyle}
                    />
                  </div>
                </div>

                {/* Ligne 5 : Rôle & Chef Direct */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className={labelStyle}>Rôle affecté</label>
                    <select
                      name="role"
                      value={formData.role}
                      onChange={handleChange}
                      className={inputStyle}
                    >
                      <option value="Demandeur">Demandeur</option>
                      <option value="Chef">Chef Direct</option>
                      <option value="Logistique">Responsable Logistique</option>
                      <option value="Directeur">Directeur</option>
                    </select>
                  </div>
                  <div>
                    <label className={labelStyle}>Chef Direct (Facultatif)</label>
                    <select
                      name="chef_direct"
                      value={formData.chef_direct}
                      onChange={handleChange}
                      className={inputStyle}
                    >
                      <option value="">Sélectionner un chef...</option>
                      {chefs.map((chef) => (
                        <option key={chef.id} value={chef.id}>
                          {chef.first_name || chef.last_name 
                            ? `${chef.first_name} ${chef.last_name}` 
                            : chef.username}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="mt-3 w-full rounded-xl bg-[#1b5e30] py-3 text-sm font-semibold text-white shadow-[0_8px_24px_-6px_rgba(27,94,48,0.50)] transition hover:bg-[#14532d] active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {loading ? "Création en cours..." : "Créer le compte demandeur"}
                </button>
              </form>

              <div className="mt-6 flex items-center justify-center gap-3 text-xs text-slate-400">
                <span className="h-px w-10 bg-gradient-to-r from-transparent to-emerald-300" />
                <span>Unité de Coordination des Projets</span>
                <span className="h-px w-10 bg-gradient-to-l from-transparent to-emerald-300" />
              </div>
            </div>
          </div>
        </div>
      </main>
    </>
  );
}
