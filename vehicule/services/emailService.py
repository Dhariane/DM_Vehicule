import threading
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def _envoyer(subject, body_text, body_html, to_list):
    def _run():
        try:
            msg = EmailMultiAlternatives(
                subject=subject,
                body=body_text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=to_list,
            )
            msg.attach_alternative(body_html, "text/html")
            msg.send()
        except Exception as e:
            print(f"[EMAIL ERROR] {e}")
    threading.Thread(target=_run, daemon=True).start()


def _base_html(titre, contenu):
    return f"""
    <html>
    <body style="font-family:Arial,sans-serif;background:#f4f4f4;padding:20px;">
      <div style="max-width:600px;margin:auto;background:#fff;
                  border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,.1);">
        <div style="background:#1a5c38;padding:20px 30px;">
          <h2 style="color:#fff;margin:0;">🚗 UCP Santé — Gestion des Véhicules</h2>
        </div>
        <div style="padding:30px;">
          <h3 style="color:#1a5c38;">{titre}</h3>
          {contenu}
        </div>
        <div style="background:#f4f4f4;padding:12px 30px;font-size:12px;color:#888;">
          Message généré automatiquement — merci de ne pas y répondre.
        </div>
      </div>
    </body>
    </html>
    """


def _ligne(label, valeur, gris=False):
    bg = "background:#f0f7f3;" if gris else ""
    return f"""
    <tr style="{bg}">
      <td style="padding:8px 12px;font-weight:bold;">{label}</td>
      <td style="padding:8px 12px;">{valeur}</td>
    </tr>
    """


def envoyer_email_chef(demande):
    demandeur = demande.demandeur
    chef = demandeur.chef_direct

    if not chef or not chef.email:
        print(f"[EMAIL] Pas de chef avec email pour {demandeur.username}")
        return

    contenu = f"""
    <p>Bonjour <strong>{chef.get_full_name() or chef.username}</strong>,</p>
    <p>
      <strong>{demandeur.get_full_name() or demandeur.username}</strong>
      ({demandeur.poste}) a soumis une demande de véhicule
      qui nécessite votre validation.
    </p>
    <table style="width:100%;border-collapse:collapse;margin:16px 0;">
      {_ligne('Destination', demande.destination, gris=True)}
      {_ligne('Motif', demande.get_motif_display())}
      {_ligne('Date départ', demande.date_depart.strftime('%d/%m/%Y %H:%M'), gris=True)}
      {_ligne('Date retour', demande.date_retour.strftime('%d/%m/%Y %H:%M'))}
      {_ligne('Passagers', demande.nombre_passagers, gris=True)}
    </table>
    <p>Connectez-vous à l'application pour traiter cette demande.</p>
    """

    _envoyer(
        subject=f"[Validation requise] Demande de {demandeur.get_full_name()}",
        body_text=f"Demande de {demandeur.get_full_name()} vers {demande.destination}",
        body_html=_base_html("Demande en attente de votre validation", contenu),
        to_list=[chef.email],
    )


def envoyer_email_decision(demande, etape, decision, commentaire=''):
    demandeur = demande.demandeur
    if not demandeur.email:
        return

    couleur = "#1a5c38" if decision == 'approuve' else "#c0392b"
    icone = "✅" if decision == 'approuve' else "❌"
    label = "approuvée" if decision == 'approuve' else "rejetée"

    etape_labels = {
        'chef': 'Chef Direct',
        'logistique': 'Responsable Logistique',
        'directeur': 'Directeur',
    }

    commentaire_html = (
        f"<p><strong>Commentaire :</strong> {commentaire}</p>"
        if commentaire else ""
    )

    contenu = f"""
    <p>Bonjour <strong>{demandeur.get_full_name() or demandeur.username}</strong>,</p>
    <p>
      Votre demande pour <strong>{demande.destination}</strong> a été
      <span style="color:{couleur};font-weight:bold;">{label}</span>
      par le <strong>{etape_labels.get(etape, etape)}</strong>.
    </p>
    <table style="width:100%;border-collapse:collapse;margin:16px 0;">
      {_ligne('Destination', demande.destination, gris=True)}
      {_ligne('Motif', demande.get_motif_display())}
      {_ligne('Statut', f'<span style="color:{couleur};font-weight:bold;">{icone} {demande.get_statut_display()}</span>', gris=True)}
    </table>
    {commentaire_html}
    """

    _envoyer(
        subject=f"[Demande véhicule] {icone} {label.capitalize()} — {demande.destination}",
        body_text=f"Votre demande vers {demande.destination} a été {label}.",
        body_html=_base_html(f"Demande {label}", contenu),
        to_list=[demandeur.email],
    )


def envoyer_email_approbation_finale(demande):
    demandeur = demande.demandeur
    if not demandeur.email:
        return

    vehicule_info = "Non affecté"
    if demande.vehicule:
        v = demande.vehicule
        vehicule_info = f"{v.marque} {v.modele} ({v.immatriculation})"

    chauffeur_info = "Non affecté"
    if demande.chauffeur:
        c = demande.chauffeur
        chauffeur_info = f"{c.prenom} {c.nom} — 📞 {c.telephone}"

    contenu = f"""
    <p>Bonjour <strong>{demandeur.get_full_name() or demandeur.username}</strong>,</p>
    <p>Votre demande a été
       <strong style="color:#1a5c38;">entièrement approuvée</strong>.
    </p>
    <table style="width:100%;border-collapse:collapse;margin:16px 0;">
      {_ligne('Destination', demande.destination, gris=True)}
      {_ligne('Date départ', demande.date_depart.strftime('%d/%m/%Y %H:%M'))}
      {_ligne('Date retour', demande.date_retour.strftime('%d/%m/%Y %H:%M'), gris=True)}
      {_ligne('🚗 Véhicule', vehicule_info)}
      {_ligne('👤 Chauffeur', chauffeur_info, gris=True)}
    </table>
    <p>Bonne mission !</p>
    """

    _envoyer(
        subject=f"✅ Demande approuvée — {demande.destination}",
        body_text=f"Votre demande vers {demande.destination} est approuvée.",
        body_html=_base_html("Mission approuvée — Véhicule & Chauffeur affectés", contenu),
        to_list=[demandeur.email],
    )