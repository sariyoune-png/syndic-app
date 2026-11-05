# Syndic – documentation

## Architecture
- `www/index.html` : application web unique (Supabase Auth + RPC), servie par Netlify.
- Supabase `nactxqbnqcdbklddmraa` : Postgres + RLS (accès administrateur uniquement), bucket privé `syndic-documents`.
- Android : projet Android Studio (WebView) qui affiche le site Netlify.

## Règles financières
- Trésorerie = somme du journal `treasury_movements` (écritures jamais modifiées ni supprimées ; une annulation crée une écriture inverse).
- Paiements via `record_payment` (partiels possibles, affectation automatique aux mois les plus anciens, reçu généré, idempotent via `p_request_id`).
- Dépenses via `record_expense`, `pay_expense`, `cancel_expense`. Paiements annulés via `cancel_payment`.
- Solde de référence au 05/11/2026 : 814,00 MAD (Excel).

## Sécurité
- RLS activée sur toutes les tables, politique `admin_all` (`is_admin()`), aucune clé service_role dans le client.
- Réglages manuels Supabase : désactiver les inscriptions publiques, activer la protection des mots de passe compromis.
- Vérification publique d'un reçu uniquement via `verify_receipt(token)`.

## Liste de tests
1. Connexion avec un compte non administrateur : refusée.
2. Paiement partiel (50 MAD) : cotisation « partiel », reçu PDF + QR, trésorerie +50.
3. Même formulaire envoyé deux fois : un seul paiement.
4. Annulation du paiement : écriture inverse, cotisation de nouveau due, reçu invalide à la vérification.
5. Dépense payée : trésorerie diminue ; dépense en attente : pas d'effet jusqu'au paiement.
6. Justificatif (📎) : fichier dans le bucket privé, lien non public.
7. Accès anonyme aux tables : aucune ligne.
8. Arabe : interface en RTL. APK : hors-ligne = page « Pas de connexion ».
