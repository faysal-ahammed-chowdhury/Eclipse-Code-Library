// Given a number $N^M$, find out the number of integer bases in which it has exactly T trailing zeroes.
int solve_greater_or_equal(vector<int> e, int t) {
  int ans = 1;
  for (auto i : e) {
    ans = 1LL * ans * (i / t + 1) % mod;
  }
  return ans;
}
// e contains e1, e2 -> ${p1}^{e1}$, ${p2}^{e2}$
int solve_equal(vector<int> e, int t) {
  return (solve_greater_or_equal(e, t) - solve_greater_or_equal(e, t + 1) + mod) % mod;
}