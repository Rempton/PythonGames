# Online-Multiplayer einrichten

Das Browser-Spiel `index.html` verwendet Supabase Realtime für Online-Räume. Die Python-/Turtle-Spiele sind davon unabhängig und laufen nicht direkt auf GitHub Pages.

## Supabase konfigurieren

1. Erstelle ein Projekt bei [Supabase](https://supabase.com/).
2. Kopiere die **Project URL** und den **Publishable key** aus der Supabase-Projektübersicht. Falls dein Projekt noch die älteren Schlüssel anzeigt, kannst du stattdessen den **anon/public key** verwenden.
3. Trage beide Werte oben im Script in `index.html` ein:

   ```js
   const SUPABASE_URL = 'https://dein-projekt.supabase.co';
   const SUPABASE_PUBLIC_KEY = 'dein-public-key';
   ```

4. Verwende niemals den `secret`- oder `service_role`-Key in einer HTML-Datei. Der Spielcode nutzt öffentliche Realtime-Broadcast-Kanäle und speichert keine Spielstände in der Datenbank.

## Auf GitHub Pages veröffentlichen

1. Lege `index.html` und diese Anleitung in ein GitHub-Repository.
2. Öffne im Repository **Settings → Pages**.
3. Wähle als Quelle den gewünschten Branch und den Ordner `/ (root)` und speichere.
4. Öffne die angezeigte Pages-Adresse. Ein Spieler erstellt einen Raum und teilt den sechsstelligen Code; der andere tritt mit diesem Code bei.

Der Raum funktioniert, solange der Spieler, der ihn erstellt hat, verbunden bleibt. Für Online-Verbindungen ist Internetzugriff auf Supabase sowie auf das Supabase-JavaScript-CDN erforderlich.
