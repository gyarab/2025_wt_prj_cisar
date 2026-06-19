<template>
  <div>
    <button class="back-btn" @click="$router.back()">← Zpět na zápasy</button>

    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>Načítám zápas...
    </div>
    <div v-else-if="error" class="error-msg">{{ error }}</div>
    <template v-else-if="match">

      <div class="scoreboard">
        <div class="sb-team home">
          <div class="sb-avatar">{{ initials(match.home_team_name) }}</div>
          <div class="sb-name">{{ match.home_team_name }}</div>
          <div class="sb-label">Domácí</div>
        </div>
        <div class="sb-center">
          <div class="sb-score">
            <span :class="{ 'score-winner': match.score_home > match.score_away }">{{ match.score_home }}</span>
            <span class="score-colon">:</span>
            <span :class="{ 'score-winner': match.score_away > match.score_home }">{{ match.score_away }}</span>
          </div>
          <div class="sb-meta">
            <div>{{ formatDate(match.date) }}</div>
            <div class="sb-stadium">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>
              {{ match.stadium }}
            </div>
          </div>
          <span v-if="match.score_home === match.score_away" class="badge badge-gray">Remíza</span>
          <span v-else class="badge badge-accent">Výhra: {{ match.score_home > match.score_away ? match.home_team_name : match.away_team_name }}</span>
        </div>
        <div class="sb-team away">
          <div class="sb-avatar away-av">{{ initials(match.away_team_name) }}</div>
          <div class="sb-name">{{ match.away_team_name }}</div>
          <div class="sb-label">Hosté</div>
        </div>
      </div>

      <div class="stats-grid" v-if="stats.length">
        <div class="stat-card">
          <div class="stat-label">Góly celkem</div>
          <div class="stat-value red">{{ match.score_home + match.score_away }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Asistence</div>
          <div class="stat-value accent">{{ totalAssists }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Trest. minuty</div>
          <div class="stat-value">{{ totalPenalty }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Zúčastněných hráčů</div>
          <div class="stat-value">{{ stats.length }}</div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <span class="card-title">Statistiky hráčů</span>
          <span class="badge badge-gray">{{ stats.length }} hráčů</span>
        </div>

        <div v-if="stats.length === 0" class="loading">Žádné statistiky k tomuto zápasu.</div>
        <table v-else>
          <thead>
            <tr>
              <th>Hráč</th>
              <th>Post</th>
              <th>Góly</th>
              <th>Asistence</th>
              <th>Body</th>
              <th>Trest. min.</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="s in statsSorted"
              :key="s.id"
              @click="$router.push(`/players/${s.player_id}`)"
            >
              <td>
                <div class="player-cell">
                  <div class="player-avatar">{{ (s.player_name || '').split(' ').map(w => w[0]).join('').toUpperCase().slice(0,2) }}</div>
                  <div>
                    <div style="font-weight:500">{{ s.player_name }}</div>
                    <div class="dim" style="font-size:12px">#{{ s.player_number }}</div>
                  </div>
                </div>
              </td>
              <td><span class="badge badge-gray">{{ s.player_position }}</span></td>
              <td><span class="number-col" :class="{ 'red-text': s.goals > 0 }">{{ s.goals }}</span></td>
              <td><span class="number-col" :class="{ 'accent-text': s.assists > 0 }">{{ s.assists }}</span></td>
              <td class="number-col">{{ s.goals + s.assists }}</td>
              <td class="dim">{{ s.penalty_minutes }}'</td>
            </tr>
          </tbody>
        </table>
      </div>

    </template>
  </div>
</template>

<script>
export default {
  name: 'MatchDetail',
  data() {
    return { match: null, stats: [], loading: true, error: null }
  },
  computed: {
    matchId() { return parseInt(this.$route.params.id) },
    totalAssists() { return this.stats.reduce((a, s) => a + s.assists, 0) },
    totalPenalty() { return this.stats.reduce((a, s) => a + s.penalty_minutes, 0) },
    statsSorted() {
      return [...this.stats].sort((a, b) => (b.goals + b.assists) - (a.goals + a.assists))
    }
  },
  methods: {
    async fetchAll() {
      try {
        const [mRes, sRes] = await Promise.all([
          fetch(`/api/matches/${this.matchId}/`),
          fetch(`/api/statistics/?match_id=${this.matchId}`)
        ])
        if (!mRes.ok) throw new Error('Zápas nenalezen')
        this.match = await mRes.json()
        this.stats = await sRes.json()
      } catch (e) {
        this.error = e.message || 'Chyba při načítání dat.'
      } finally {
        this.loading = false
      }
    },
    initials(name) {
      return (name || '').split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
    },
    formatDate(d) {
      return new Date(d).toLocaleDateString('cs-CZ', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })
    }
  },
  mounted() { this.fetchAll() }
}
</script>

<style scoped>
.back-btn {
  background: transparent; border: 1px solid var(--border);
  color: var(--text-secondary); padding: 7px 14px;
  border-radius: 8px; font-size: 13px; font-weight: 500;
  cursor: pointer; font-family: 'Inter', sans-serif;
  margin-bottom: 28px; transition: all 0.15s;
}
.back-btn:hover { color: var(--text-primary); border-color: rgba(255,255,255,0.15); }

.scoreboard {
  display: flex; align-items: center; gap: 16px;
  background: var(--ice-card); border: 1px solid var(--border);
  border-radius: 16px; padding: 32px 24px;
  margin-bottom: 28px;
}
.sb-team { flex: 1; text-align: center; }
.sb-team.away { }
.sb-avatar, .away-av {
  width: 60px; height: 60px; border-radius: 14px;
  background: var(--accent-dim); border: 1px solid var(--border-accent);
  display: flex; align-items: center; justify-content: center;
  font-family: 'Oswald', sans-serif; font-size: 20px; font-weight: 700;
  color: var(--accent); margin: 0 auto 10px;
}
.away-av { background: var(--red-dim); border-color: rgba(229,57,53,0.3); color: var(--red); }
.sb-name { font-family: 'Oswald', sans-serif; font-size: 18px; font-weight: 600; }
.sb-label { font-size: 12px; color: var(--text-muted); margin-top: 4px; }

.sb-center { text-align: center; flex-shrink: 0; }
.sb-score {
  font-family: 'Oswald', sans-serif;
  font-size: 56px; font-weight: 700; line-height: 1;
  display: flex; align-items: center; gap: 8px;
  justify-content: center; margin-bottom: 10px;
  color: var(--text-muted);
}
.score-winner { color: var(--text-primary); }
.score-colon { color: var(--text-muted); font-size: 40px; }
.sb-meta { font-size: 13px; color: var(--text-secondary); margin-bottom: 10px; }
.sb-stadium { display: flex; align-items: center; gap: 4px; justify-content: center; margin-top: 4px; }

.player-cell { display: flex; align-items: center; gap: 10px; }
.player-avatar {
  width: 32px; height: 32px; border-radius: 50%;
  background: rgba(79,195,247,0.12); border: 1px solid rgba(79,195,247,0.2);
  display: flex; align-items: center; justify-content: center;
  font-family: 'Oswald', sans-serif; font-size: 12px; font-weight: 600;
  color: var(--accent); flex-shrink: 0;
}
.red-text { color: var(--red); }
.accent-text { color: var(--accent); }
</style>