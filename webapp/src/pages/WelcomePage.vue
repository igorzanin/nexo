<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "../stores";

const router = useRouter();
const userStore = useUserStore();
const step = ref(1);
const totalSteps = 3;
const completing = ref(false);

function next() {
  if (step.value < totalSteps) {
    step.value++;
  }
}

function prev() {
  if (step.value > 1) {
    step.value--;
  }
}

async function finish() {
  completing.value = true;
  try {
    await userStore.updateMyConfig({ onboardingComplete: true });
    router.push("/board");
  } finally {
    completing.value = false;
  }
}

function skip() {
  userStore.updateMyConfig({ onboardingComplete: true });
  router.push("/board");
}
</script>

<template>
  <div class="d-flex align-items-center justify-content-center vh-100 bg-body-secondary">
    <div class="card shadow" style="width: 560px;">
      <div class="card-body p-5 text-center">
        <div class="d-flex justify-content-center gap-1 mb-4">
          <span v-for="s in totalSteps" :key="s"
            class="rounded-circle d-inline-block"
            :class="s === step ? 'bg-primary' : s < step ? 'bg-success' : 'bg-secondary bg-opacity-25'"
            style="width: 10px; height: 10px;"
          ></span>
        </div>

        <div v-if="step === 1">
          <i class="bi bi-kanban fs-1 text-primary mb-3 d-block"></i>
          <h4 class="card-title">Welcome to Nexo</h4>
          <p class="text-muted small">Boards are where you organize your work. Create a board for your project, team, or personal tasks.</p>
          <div class="border rounded p-4 bg-body text-start mb-3">
              <div>
                <strong>Board</strong>
                <p class="small text-muted mb-0">A board contains cards organized in views like Kanban, Table, or Calendar.</p>
              </div>
            </div>
          </div>
        </div>

        <div v-else-if="step === 2">
          <i class="bi bi-card-text fs-1 text-primary mb-3 d-block"></i>
          <h4 class="card-title">Create Cards</h4>
          <p class="text-muted small">Cards represent tasks, ideas, or items. Add properties, descriptions, comments, and attachments.</p>
          <div class="border rounded p-4 bg-body text-start mb-3">
            <div class="d-flex align-items-center gap-3">
              <i class="bi bi-list-columns fs-3 text-primary"></i>
              <div>
                <strong>Properties</strong>
                <p class="small text-muted mb-0">Customize cards with text, numbers, dates, people, and more.</p>
              </div>
            </div>
          </div>
        </div>

        <div v-else-if="step === 3">
          <i class="bi bi-share fs-1 text-primary mb-3 d-block"></i>
          <h4 class="card-title">Share with Your Team</h4>
          <p class="text-muted small">Invite team members to collaborate on boards in real-time.</p>
          <div class="border rounded p-4 bg-body text-start mb-3">
            <div class="d-flex align-items-center gap-3">
              <i class="bi bi-people fs-3 text-primary"></i>
              <div>
                <strong>Team Collaboration</strong>
                <p class="small text-muted mb-0">Share boards publicly or invite specific members with custom permissions.</p>
              </div>
            </div>
          </div>
        </div>

        <div class="d-flex justify-content-between mt-4">
          <button v-if="step > 1" class="btn btn-outline-secondary" @click="prev">
            <i class="bi bi-arrow-left me-1"></i> Back
          </button>
          <span v-else></span>
          <div class="d-flex gap-2">
            <button class="btn btn-link text-muted small" @click="skip">Skip tour</button>
            <button v-if="step < totalSteps" class="btn btn-primary" @click="next">
              Next <i class="bi bi-arrow-right ms-1"></i>
            </button>
            <button v-else class="btn btn-success" :disabled="completing" @click="finish">
              <span v-if="completing" class="spinner-border spinner-border-sm me-1"></span>
              Get Started <i class="bi bi-check-lg ms-1"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
