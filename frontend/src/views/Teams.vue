<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Týmy</h1>
      <p class="page-subtitle">Přehled všech týmů v soutěži</p>
    </div>

    <div class="stats-grid" v-if="teams.length">
      <div class="stat-card">
        <div class="stat-label">Celkem týmů</div>
        <div class="stat-value accent">{{ teams.length }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Průměr hráčů</div>
        <div class="stat-value">{{ avgPlayers }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Nejv. počet hráčů</div>
        <div class="stat-value">{{ maxPlayers }}</div>
      </div>
    </div>

    <div class="search-bar">
      <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
      </svg>
      <input v-model="search" placeholder="Hledat tým..." />
    </div>

    <div class="card">
      <div class="card-header">
        <span class="card-title">Všechny týmy</span>
        <span class="badge badge-gray">{{ filtered.length }} týmů</span>
      </div>

      <div v-if="loading" class="loading">
        <div class="loading-spinner"></div>
        Načítám týmy...
      </div>
      <div v-else-if="error" class="error-msg">{{ error }}</div>
      <table v-else>
        <thead>
          <tr>
            <th>#</th>
            <th>Název týmu</th>
            <th>Město</th>
            <th>Rok vzniku</th>
            <th>Hráči</th>
            <th>Akce</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(team, i) in filtered" :key="team.id" @click="goToTeam(team)">
            <td class="number-col dim">{{ i + 1 }}</td>
            <td>
              <div class="team-name-cell">
                <div class="team-avatar" :style="{ background: teamColor(team.id) }">
                  {{ teamInitials(team.name) }}
                </div>
                <span>{{ team.name }}</span>
              </div>
            </td>
            <td class="dim">{{ team.city || '—' }}</td>
            <td class="dim">{{ team.founded || '—' }}</td>
            <td>
              <span class="badge badge-accent" v-if="team.player_count">
                {{ team.player_count }} hráčů
              </span>
              <span class="dim" v-else>—</span>
            </td>
            <td>
              <button class="btn-detail" @click.stop="goToPlayers(team)">
                Hráči →
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="!loading && !error && filtered.length === 0" class="loading">
        Žádné výsledky pro „{{ search }}"
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Teams',
  data() {
    return {
      teams: [],
      loading: true,
      error: null,
      search: ''
    }
  },
  computed: {
    filtered() {
      const s = this.search.toLowerCase()
      if (!s) return this.teams
      return this.teams.filter(t =>
        t.name?.toLowerCase().includes(s) ||
        t.city?.toLowerCase().includes(s)
      )
    },
    avgPlayers() {
      if (!this.teams.length) return 0
      const total = this.teams.reduce((a, t) => a + (t.player_count || 0), 0)
      return Math.round(total / this.teams.length)
    },
    maxPlayers() {
      return Math.max(...this.teams.map(t => t.player_count || 0)) || 0
    }
  },
  methods: {
    async fetchTeams() {
      try {
        const res = await fetch('/api/teams/')
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        const data = await res.json()
        this.teams = Array.isArray(data) ? data : (data.results || [])
      } catch (e) {
        this.error = 'Nepodařilo se načíst týmy. Zkontrolujte spojení s API.'
        console.error(e)
      } finally {
        this.loading = false
      }
    },
    teamInitials(name) {
      if (!name) return '?'
      return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
    },
    teamColor(id) {
      const colors = [
        'rgba(79,195,247,0.25)', 'rgba(229,57,53,0.25)', 'rgba(102,187,106,0.25)',
        'rgba(255,167,38,0.25)', 'rgba(171,71,188,0.25)', 'rgba(41,182,246,0.25)'
      ]
      return colors[id % colors.length]
    },
    goToTeam(team) {
      this.$router.push({ path: '/players', query: { team: team.id } })
    },
    goToPlayers(team) {
      this.$router.push({ path: '/players', query: { team: team.id } })
    }
  },
  mounted() {
    this.fetchTeams()
  }
}
</script>

<style scoped>
.team-name-cell {
  display: flex; align-items: center; gap: 10px;
}
.team-avatar {
  width: 32px; height: 32px;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-family: 'Oswald', sans-serif;
  font-size: 12px; font-weight: 700;
  color: var(--text-primary);
  flex-shrink: 0;
}
.btn-detail {
  background: transparent;
  border: 1px solid var(--border);
  color: var(--accent);
  padding: 5px 12px;
  border-radius: 6px;
  font-size: 12px; font-weight: 500;
  cursor: pointer;
  font-family: 'Inter', sans-serif;
  transition: all 0.15s;
  white-space: nowrap;
}
.btn-detail:hover {
  background: var(--accent-dim);
  border-color: var(--border-accent);
}
</style>


