import Vue from 'vue'

import _ from 'lodash'


export default {
    namespaced: true,
    state: {
        nodesOpened: [],
        selection: [],
    },
    mutations: {
        replaceOffer (state, {changedOffer, newOffer, item, meta, getters}) {
            let nodeIdx = getters.nodeIdx(meta.parent)
            let newSelection = state.selection[nodeIdx].slice()

            newSelection[newSelection.findIndex(selectionItem => {
                return selectionItem.offerModel.offer.id === item.offerModel.offer.id
            })] = {
                parentModel: item.parentModel,
                offerModel: newOffer,
                count: item.count,
            }

            Vue.set(state.selection, nodeIdx, newSelection)
        },

        toggleItem (state, {item, idx}) {
            let nodeIdx = state.nodesOpened.findIndex (openedItem => {
                return (openedItem.offerModel.offer.id
                        === item.offerModel.offer.id)
            })

            if (nodeIdx !== -1) {
                state.nodesOpened = _.remove (state.nodesOpened,
                        openedItem => (openedItem.offerModel.offer.id
                                       !== item.offerModel.offer.id))
                state.selection[nodeIdx] = []
            } else {
                state.nodesOpened.push(item)
            }
        },

        removeSelected (state, {item, meta, nodeIdx }) {
            let newSelection = _.remove (state.selection[nodeIdx].slice(),
                    selectionItem => selectionItem.offerModel.offer.id !== item.offerModel.offer.id)

            Vue.set (state.selection, nodeIdx, newSelection)
        },

        addSelection (state, {parentItem, model}) {
            let nodeIdx = state.nodesOpened.findIndex (openedItem => {
                return openedItem.offerModel.offer.id === parentItem.offerModel.offer.id
            })

            state.selection[nodeIdx] = state.selection[nodeIdx] ?
                    state.selection[nodeIdx] : []

            let newSelection = state.selection[nodeIdx].slice ()
            newSelection.push (model)
            Vue.set (state.selection, nodeIdx, newSelection)
        }
    },
    actions: {
        selectOffer ({commit, state, getters, rootState},
                {changedOffer, newOffer, item, meta}) {
            if (item.count === 0 && item.offerModel.offer.id !== meta.parent.offerModel.offer.id) {
                commit ('replaceOffer', {
                        changedOffer, newOffer, item, meta, getters})
            } else {
                let offerItem
                state.selection.find (selection => {
                    let offerItemIdx = selection.findIndex (offerItem => {
                        return offerItem.offerModel.offer.id === newOffer.offer.id
                    })

                    offerItem = offerItemIdx !== -1 ? selection[offerItemIdx] :
                            offerItem

                    return offerItem ? true : false
                }) 

                let model = offerItem ? offerItem : ({
                    parentModel: item.parentModel,
                    offerModel: newOffer,
                    count: 0,
                })

                commit('addSelection', { parentItem: meta.parent, model })
            }
        },

        removeSelected ({commit, state, dispatch, getters},
                {offer, item, meta}) {
            let nodeIdx = getters.nodeIdx(meta.parent)
            if (state.selection[nodeIdx].length > 1) {
                commit ('removeSelected', {offer, item, meta, nodeIdx})
            }

            if (getters.nodeIdx (item) === -1) {
                dispatch('cart/remove', {item}, {root: true})
            }
        },

        toggleItem ({commit, state, dispatch, getters}, {item, idx}) {
            commit('toggleItem', {item, idx})

            if (item.count === 0) {
                dispatch('cart/remove', {item, idx}, {root: true})
            }
        },
    },
    getters: {
        visibleOffers: (state, getters, rootState) => item => {
            let offers = [item]
            let nodeIdx = state.nodesOpened.findIndex (openedItem => {
                return (openedItem.offerModel.offer.id
                        === item.offerModel.offer.id)
            })
            let offersWithCart = []

            if (nodeIdx !== -1 && state.selection[nodeIdx]) {
                offersWithCart = state.selection[nodeIdx].reduce (
                    (result, item) => {
                        let inCartIdx = rootState.cart.items.findIndex(
                            cartItem => {
                                return (item.offerModel.offer.id
                                        === cartItem.offerModel.offer.id)
                            }
                        )

                        if (inCartIdx !== -1) {
                            result.push (rootState.cart.items[inCartIdx])
                        } else {
                            result.push (item)
                        }

                        return result
                }, [])
            }

            return _.concat(offers, offersWithCart)
        },

        offerMenuItems: (state, getters, rootState) => (model) => {
            let groupActiveOffers = rootState.cart.items.reduce (
                (result, cartItem) => {
                    if (cartItem.offerModel.offer.parent_id
                            === model.offerModel.offer.parent_id) {
                        result.push(cartItem.offerModel)
                    }
                    return result
                }, [])

            let ids = _.difference(
                model.parentModel.formats.map((item)=>{return item.offer.id}),
                [...groupActiveOffers, model.offerModel].map(
                    (item)=>{return item.offer.id})
            )

            return ids.length ? model.parentModel.formats.filter((item)=>{
                return ids.indexOf(item.offer.id) !== -1
            }) : []
        },

        nodeIdx: (state) => (item) => {
            return state.nodesOpened.findIndex (openedItem => {
                return openedItem.offerModel.offer.id === item.offerModel.offer.id
            })
        },
    }
}
