<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Zápasy</h1>
      <p class="page-subtitle">Výsledky a přehled utkání</p>
    </div>

    <div class="stats-grid" v-if="matches.length">
      <div class="stat-card">
        <div class="stat-label">Celkem zápasů</div>
        <div class="stat-value accent">{{ matches.length }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Průměr gólů/zápas</div>
        <div class="stat-value">{{ avgGoals }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Nejvíc gólů v zápase</div>
        <div class="stat-value red">{{ maxGoals }}</div>
      </div>
    </div>

    <div class="toolbar">
      <div class="search-bar search-bar--inline">
        <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
        </svg>
        <input v-model="search" placeholder="Hledat tým..." />
      </div>
      <select v-model="filterTeam" class="team-select">
        <option value="">Všechny týmy</option>
        <option v-for="t in teams" :key="t.id" :value="t.id">{{ t.name }}</option>
      </select>
    </div>

    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      Načítám zápasy...
    </div>
    <div v-else-if="error" class="error-msg">{{ error }}</div>
    <template v-else>
      <div v-for="match in filtered" :key="match.id" class="match-card" @click="openMatch(match)">
        <div class="match-date">
          <div class="match-day">{{ formatDay(match.date) }}</div>
          <div class="match-month">{{ formatMonth(match.date) }}</div>
        </div>

        <div class="match-body">
          <div class="match-teams">
            <span class="team-name home" :class="{ winner: match.score_home > match.score_away }">
              {{ match.home_team_name }}
            </span>
            <div class="score-block">
              <span class="score" :class="{ 'score--home-win': match.score_home > match.score_away }">{{ match.score_home }}</span>
              <span class="score-sep">:</span>
              <span class="score" :class="{ 'score--away-win': match.score_away > match.score_home }">{{ match.score_away }}</span>
            </div>
            <span class="team-name away" :class="{ winner: match.score_away > match.score_home }">
              {{ match.away_team_name }}
            </span>
          </div>
          <div class="match-info">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>
            {{ match.stadium }}
          </div>
        </div>

        <div class="match-result-badge">
          <span v-if="match.score_home === match.score_away" class="badge badge-gray">Remíza</span>
          <span v-else class="badge badge-accent">{{ match.score_home > match.score_away ? match.home_team_name : match.away_team_name }}</span>
        </div>
      </div>

      <div v-if="filtered.length === 0" class="loading">Žádné zápasy nenalezeny.</div>
    </template>
  </div>
</template>

<script>
export default {
  name: 'Matches',
  data() {
    return {
      matches: [],
      teams: [],
      loading: true,
      error: null,
      search: '',
      filterTeam: '',
      selectedMatch: null
    }
  },
  computed: {
    filtered() {
      let result = this.matches
      if (this.filterTeam) {
        result = result.filter(m =>
          m.home_team_id === parseInt(this.filterTeam) ||
          m.away_team_id === parseInt(this.filterTeam)
        )
      }
      const s = this.search.toLowerCase()
      if (s) {
        result = result.filter(m =>
          m.home_team_name?.toLowerCase().includes(s) ||
          m.away_team_name?.toLowerCase().includes(s) ||
          m.stadium?.toLowerCase().includes(s)
        )
      }
      return result
    },
    avgGoals() {
      if (!this.matches.length) return '0.0'
      const total = this.matches.reduce((a, m) => a + m.score_home + m.score_away, 0)
      return (total / this.matches.length).toFixed(1)
    },
    maxGoals() {
      return Math.max(...this.matches.map(m => m.score_home + m.score_away), 0)
    }
  },
  methods: {
    async fetchData() {
      try {
        const [mRes, tRes] = await Promise.all([
          fetch('/api/matches/'),
          fetch('/api/teams/')
        ])
        if (!mRes.ok) throw new Error(`HTTP ${mRes.status}`)
        const mData = await mRes.json()
        const tData = await tRes.json()
        this.matches = Array.isArray(mData) ? mData : (mData.results || [])
        this.teams = Array.isArray(tData) ? tData : (tData.results || [])
      } catch (e) {
        this.error = 'Nepodařilo se načíst zápasy.'
      } finally {
        this.loading = false
      }
    },
    formatDay(date) {
      return new Date(date).getDate()
    },
    formatMonth(date) {
      return new Date(date).toLocaleDateString('cs-CZ', { month: 'short', year: 'numeric' })
    },
    openMatch(match) {
      this.$router.push(`/matches/${match.id}`)
    }
  },
  mounted() { this.fetchData() }
}
</script>

<style scoped>
.toolbar {
  display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap;
}
.search-bar--inline { flex: 1; min-width: 180px; margin-bottom: 0; }

.team-select {
  background: var(--ice-surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  color: var(--text-primary);
  padding: 9px 14px;
  font-size: 14px; font-family: 'Inter', sans-serif;
  outline: none; cursor: pointer;
  transition: border-color 0.15s;
}
.team-select:focus { border-color: var(--border-accent); }

.match-card {
  display: flex; align-items: center; gap: 20px;
  background: var(--ice-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 18px 20px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: all 0.15s;
}
.match-card:hover {
  border-color: var(--border-accent);
  background: rgba(79,195,247,0.04);
}

.match-date {
  text-align: center; min-width: 44px;
  flex-shrink: 0;
}
.match-day {
  font-family: 'Oswald', sans-serif;
  font-size: 28px; font-weight: 700;
  color: var(--text-primary); line-height: 1;
}
.match-month { font-size: 11px; color: var(--text-muted); margin-top: 3px; }

.match-body { flex: 1; }
.match-teams {
  display: flex; align-items: center; gap: 16px;
  margin-bottom: 6px;
}
.team-name {
  font-size: 15px; font-weight: 500;
  flex: 1;
  color: var(--text-secondary);
  transition: color 0.15s;
}
.team-name.home { text-align: right; }
.team-name.away { text-align: left; }
.team-name.winner { color: var(--text-primary); }

.score-block {
  display: flex; align-items: center; gap: 4px;
  flex-shrink: 0;
}
.score {
  font-family: 'Oswald', sans-serif;
  font-size: 26px; font-weight: 700;
  color: var(--text-secondary);
  min-width: 28px; text-align: center;
  transition: color 0.15s;
}
.score--home-win, .score--away-win { color: var(--text-primary); }
.score-sep {
  font-family: 'Oswald', sans-serif;
  font-size: 20px; color: var(--text-muted);
}

.match-info {
  font-size: 12px; color: var(--text-muted);
  display: flex; align-items: center; gap: 5px;
}

.match-result-badge { flex-shrink: 0; }
</style>