export const mutations = {
  authorized (state) {
    state.authorized = true
  },
  lastResult (state, result) {
    state.lastResult = result
  },
  access_token (state, token) {
    state.access_token = token
  }
}
