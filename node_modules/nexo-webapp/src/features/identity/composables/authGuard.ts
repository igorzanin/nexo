/**
 * features/identity/composables/authGuard.ts
 * Navigation guard que bloqueia rotas com meta.requiresAuth sem token.
 * Registrado em router/index.ts via router.beforeEach(authGuard).
 */
import type { NavigationGuardNext, RouteLocationNormalized } from "vue-router";

export function authGuard(
  to: RouteLocationNormalized,
  _from: RouteLocationNormalized,
  next: NavigationGuardNext
): void {
  const hasToken = !!localStorage.getItem("access_token");

  if (to.meta.requiresAuth && !hasToken) {
    next(`/login?r=${encodeURIComponent(to.fullPath)}`);
  } else {
    next();
  }
}
