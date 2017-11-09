export const mutations = {
  authorized (state) {
    state.authorized = true
  },
  lastResult (state, result) {
    state.lastResult = result
  }
}
