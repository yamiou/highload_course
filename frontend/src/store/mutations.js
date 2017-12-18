export const mutations = {
  authorized (state) {
    state.authorized = true
  },
  lastResult (state, result) {
    state.lastResult = result
  },
  lastLibResult (state, result) {
    state.lastLibResult = result
  },
  access_token (state, token) {
    state.access_token = token
  },
  username (state, token) {
    state.username = token
  }
}
