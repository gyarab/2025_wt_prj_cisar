<template>
  <div id="app">
    <header class="site-header">
      <div class="header-inner">
        <div class="logo">
          <span class="logo-text">HOCKEYSTATS</span>
        </div>
        <nav class="main-nav">
          <router-link to="/teams" class="nav-link" active-class="nav-link--active">Tymy</router-link>
          <router-link to="/players" class="nav-link" active-class="nav-link--active">Hraci</router-link>
          <router-link to="/matches" class="nav-link" active-class="nav-link--active">Zapasy</router-link>
        </nav>
      </div>
    </header>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script>
export default { name: 'App' }
</script>