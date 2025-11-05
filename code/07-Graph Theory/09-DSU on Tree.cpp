// Problem: Distinct Colors CSES (Number of distinct color in a subtree)
// Complexity: $O(n(logn)^2)$
set<int> se[N];
int col[N], ans[N], par[N]; // $par[i]=i$ initially
int find(int i) {
  return (i == par[i] ? i : par[i] = find(par[i]));
}
void merge(int u, int v) {
  if ((u = find(u)) == (v = find(v))) return;
  if (se[u].size() > se[v].size()) swap(u, v);
  for (auto x : se[u]) {
    se[v].insert(x);
  }
  se[u].clear();
  par[u] = v;
}
void dfs(int u, int p) {
  se[find(u)].insert(col[u]);
  for (auto v : g[u]) {
    if (v != p) {
      dfs(v, u);
      merge(u, v);
    }
  }
  ans[u] = se[find(u)].size();
}