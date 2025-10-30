// dis[i][j] = min distance to reach i to j, works for neg edge (no neg cycle)
// Time: $O(n^3)$
void floyd_warshall() {
  for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= n; j++) {
      if (i == j) dis[i][j] = 0;
      else if (g[i][j] == 0) dis[i][j] = inf;
      else dis[i][j] = g[i][j];
    }
  }
  for (int k = 1; k <= n; ++k) {
    for (int i = 1; i <= n; ++i) {
      for (int j = 1; j <= n; ++j) {
        if (dis[i][k] < inf and dis[k][j] < inf)
          dis[i][j] = min(dis[i][j], dis[i][k] + dis[k][j]);
      }
    }
  }
}
int32_t main() {
  int q; cin >> n >> m >> q;
  while (m--) {
    int u, v, w; cin >> u >> v >> w;
    g[u][v] = (g[u][v] != 0 ? min(g[u][v], w) : w);
    g[v][u] = (g[v][u] != 0 ? min(g[v][u], w) : w);
  }
  floyd_warshall();
  while (q--) {
    int u, v; cin >> u >> v;
    cout << (dis[u][v] == inf ? -1 : dis[u][v]) << '\n';
  }
  return 0;
}