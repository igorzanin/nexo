import { createRouter, createWebHistory } from "vue-router";

function isAuthenticated(): boolean {
  return !!localStorage.getItem("access_token");
}

const routes = [
  {
    path: "/login",
    component: () => import("../pages/LoginPage.vue"),
  },
  {
    path: "/register",
    component: () => import("../pages/RegisterPage.vue"),
  },
  {
    path: "/change_password",
    component: () => import("../pages/ChangePasswordPage.vue"),
  },
  {
    path: "/error",
    component: () => import("../pages/ErrorPage.vue"),
  },
  {
    path: "/board/:boardId?/:viewId?/:cardId?",
    component: () => import("../pages/board/BoardPage.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/team/:teamId/:boardId?/:viewId?/:cardId?",
    component: () => import("../pages/board/BoardPage.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/team/:teamId/shared/:boardId?/:viewId?/:cardId?",
    component: () => import("../pages/board/BoardPage.vue"),
    meta: { readonly: true },
  },
  {
    path: "/shared/:boardId?/:viewId?/:cardId?",
    component: () => import("../pages/board/BoardPage.vue"),
    meta: { readonly: true },
  },
  {
    path: "/:pathMatch(.*)*",
    redirect: "/board",
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, _from) => {
  if (to.meta.requiresAuth && !isAuthenticated()) {
    return `/login?r=${encodeURIComponent(to.fullPath)}`;
  }
});

export default router;
