import { createRouter, createWebHistory } from 'vue-router'
import Teams from '../views/Teams.vue'
import Players from '../views/Players.vue'
import PlayerDetail from '../views/PlayerDetail.vue'
import Matches from '../views/Matches.vue'
import MatchDetail from '../views/MatchDetail.vue'

const routes = [
  { path: '/', redirect: '/teams' },
  { path: '/teams', component: Teams, name: 'teams' },
  { path: '/players', component: Players, name: 'players' },
  { path: '/players/:id', component: PlayerDetail, name: 'player-detail' },
  { path: '/matches', component: Matches, name: 'matches' },
  { path: '/matches/:id', component: MatchDetail, name: 'match-detail' },
]

export default createRouter({
  history: createWebHistory(),
  routes
})