import _ from 'lodash'
import Vue from 'vue'

let debounceInterval = 300
export default {
    namespaced: true,
    modules: {
    },
    state: {
        activeTab: 1,
        categories: [
            'Всё',
            'Фрукты и Ягоды',
            'Овощи',
            'Зелень',
            'Грибы',
            'Сезонное',
        ],
        items: [],
        fullItems: [],

        rowsPerPageItems: [12],
    },
    mutations: {
        update: (state, items) => {
            state.fullItems = items
            state.items = state.fullItems.slice (0, 11)
        },

        updateTab: (state, tabId) => {
            state.activeTab = tabId
        },

        nextItems: state => {
            state.items = state.fullItems.slice(0, state.items.length + 12)
        },
    },
    actions: {
        setActiveTab: ({commit, dispatch}, tabId) => {
            commit('updateTab', tabId)
            dispatch('load')
        },

        load: _.debounce (({commit, state, rootState}) => {
            fetch('/api/market/list', {
                method: 'POST',
                body: JSON.stringify({
                    category: state.activeTab,
                    search_text: rootState.searchText || null,
                }),
            })
            .then(response => {
                return response.json()})
            .then(result => {
                commit('update', result)})
            .catch(exp => {
                console.error(exp)});
        }, debounceInterval)
    },
    getters: {
        total: state => {
            return state.items.length
        },

        hasMore: state => {
            return (state.fullItems.slice(0, state.items.length + 12).length
                        > state.items.length)
        }
    }
}
