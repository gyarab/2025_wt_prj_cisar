<template>
  <div>
    <button class="back-btn" @click="$router.back()">
      ← Zpět
    </button>

    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      Načítám hráče...
    </div>
    <div v-else-if="error" class="error-msg">{{ error }}</div>
    <template v-else-if="player">

      <div class="player-hero">
        <div class="player-hero-avatar">{{ playerInitials }}</div>
        <div class="player-hero-info">
          <div class="player-jersey">#{{ player.number }}</div>
          <h1 class="player-fullname">{{ player.name }}</h1>
          <div class="player-meta-row">
            <span class="badge badge-accent">{{ player.position }}</span>
            <span class="badge badge-gray">{{ player.team_name }}</span>
            <span class="badge badge-gray">{{ player.age }} let</span>
          </div>
        </div>
      </div>

      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-label">Góly celkem</div>
          <div class="stat-value red">{{ totalGoals }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Asistence celkem</div>
          <div class="stat-value accent">{{ totalAssists }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Body (G+A)</div>
          <div class="stat-value">{{ totalGoals + totalAssists }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Trest. minuty</div>
          <div class="stat-value">{{ totalPenalty }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Odehraných zápasů</div>
          <div class="stat-value">{{ stats.length }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Průměr bodů/zápas</div>
          <div class="stat-value accent">{{ avgPoints }}</div>
        </div>
      </div>

      <div class="card" v-if="stats.length">
        <div class="card-header">
          <span class="card-title">Statistiky po zápasech</span>
          <span class="badge badge-gray">{{ stats.length }} zápasů</span>
        </div>
        <table>
          <thead>
            <tr>
              <th>Zápas</th>
              <th>Datum</th>
              <th>Góly</th>
              <th>Asistence</th>
              <th>Body</th>
              <th>TM</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in stats" :key="s.id">
              <td>
                <span class="match-label">{{ matchLabel(s.match_id) }}</span>
              </td>
              <td class="dim">{{ matchDate(s.match_id) }}</td>
              <td>
                <span class="number-col" :class="{ 'red-text': s.goals > 0 }">{{ s.goals }}</span>
              </td>
              <td>
                <span class="number-col" :class="{ 'accent-text': s.assists > 0 }">{{ s.assists }}</span>
              </td>
              <td class="number-col">{{ s.goals + s.assists }}</td>
              <td class="dim">{{ s.penalty_minutes }}'</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="card">
        <div class="loading">Žádné statistiky k zobrazení.</div>
      </div>

    </template>
  </div>
</template>

<script>
export default {
  name: 'PlayerDetail',
  data() {
    return {
      player: null,
      stats: [],
      matches: [],
      loading: true,
      error: null
    }
  },
  computed: {
    playerId() { return parseInt(this.$route.params.id) },
    playerInitials() {
      return (this.player?.name || '').split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2) || '?'
    },
    totalGoals() { return this.stats.reduce((a, s) => a + s.goals, 0) },
    totalAssists() { return this.stats.reduce((a, s) => a + s.assists, 0) },
    totalPenalty() { return this.stats.reduce((a, s) => a + s.penalty_minutes, 0) },
    avgPoints() {
      if (!this.stats.length) return '0.0'
      return ((this.totalGoals + this.totalAssists) / this.stats.length).toFixed(1)
    }
  },
  methods: {
    async fetchAll() {
      try {
        const [pRes, sRes, mRes] = await Promise.all([
          fetch(`/api/players/${this.playerId}/`),
          fetch(`/api/statistics/player/${this.playerId}/`),
          fetch('/api/matches/')
        ])
        if (!pRes.ok) throw new Error('Hráč nenalezen')
        this.player = await pRes.json()
        this.stats = await sRes.json()
        const mData = await mRes.json()
        this.matches = Array.isArray(mData) ? mData : (mData.results || [])
      } catch (e) {
        this.error = e.message || 'Chyba při načítání dat.'
      } finally {
        this.loading = false
      }
    },
    matchLabel(matchId) {
      const m = this.matches.find(m => m.id === matchId)
      if (!m) return `Zápas #${matchId}`
      return `${m.home_team_name} vs ${m.away_team_name}`
    },
    matchDate(matchId) {
      const m = this.matches.find(m => m.id === matchId)
      if (!m) return ''
      return new Date(m.date).toLocaleDateString('cs-CZ')
    }
  },
  mounted() { this.fetchAll() }
}
</script>

<style scoped>
.back-btn {
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text-secondary);
  padding: 7px 14px;
  border-radius: 8px;
  font-size: 13px; font-weight: 500;
  cursor: pointer; font-family: 'Inter', sans-serif;
  margin-bottom: 28px;
  transition: all 0.15s;
}
.back-btn:hover { color: var(--text-primary); border-color: rgba(255,255,255,0.15); }

.player-hero {
  display: flex; align-items: center; gap: 24px;
  margin-bottom: 32px;
  padding: 28px;
  background: var(--ice-card);
  border: 1px solid var(--border);
  border-radius: 16px;
  position: relative; overflow: hidden;
}
.player-hero::before {
  content: '';
  position: absolute; left: 0; top: 0; bottom: 0;
  width: 4px;
  background: var(--accent);
}
.player-hero-avatar {
  width: 72px; height: 72px; flex-shrink: 0;
  border-radius: 50%;
  background: var(--accent-dim);
  border: 2px solid var(--border-accent);
  display: flex; align-items: center; justify-content: center;
  font-family: 'Oswald', sans-serif;
  font-size: 26px; font-weight: 700;
  color: var(--accent);
}
.player-jersey {
  font-family: 'Oswald', sans-serif;
  font-size: 13px; font-weight: 600;
  color: var(--text-muted); letter-spacing: 1px;
  margin-bottom: 4px;
}
.player-fullname {
  font-family: 'Oswald', sans-serif;
  font-size: 30px; font-weight: 700;
  color: var(--text-primary); letter-spacing: 1px;
  margin-bottom: 10px;
}
.player-meta-row { display: flex; gap: 8px; flex-wrap: wrap; }

.red-text { color: var(--red); }
.accent-text { color: var(--accent); }

.match-label { font-size: 13px; font-weight: 500; }
</style>