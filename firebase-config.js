// ============================================================================
// Configuración de sincronización entre dispositivos (opcional)
// ============================================================================
// Si NO quieres sincronizar entre dispositivos, no toques nada de este
// archivo: la app seguirá funcionando igual que antes, guardando los datos
// solo en este navegador.
//
// Si SÍ quieres sincronizar (ver tus registros desde el móvil y el
// ordenador), sigue los pasos del README ("Sincronización entre
// dispositivos") para crear un proyecto gratuito de Firebase, y luego:
//   1. Sustituye los valores de FIREBASE_CONFIG por los de tu proyecto
//      (Firebase console → ⚙️ Configuración del proyecto → tus apps → SDK).
//   2. Cambia SYNC_ENABLED a true.
//   3. Sube este archivo (reemplazando el que ya tienes) a tu repositorio.
// ============================================================================

const SYNC_ENABLED = true;

const FIREBASE_CONFIG = {
  apiKey: "AIzaSyA5OoPBajvjfe_7lO5AljXDvyITkW-nq1U",
  authDomain: "allergylog-824a1.firebaseapp.com",
  projectId: "allergylog-824a1",
  storageBucket: "allergylog-824a1.firebasestorage.app",
  messagingSenderId: "397212086532",
  appId: "1:397212086532:web:722448d503ca93cccde051"
};

