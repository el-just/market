<template>
    <v-container fluid
            class="products-container"
            >
        <v-layout wrap justify-space-around
                class="categories-container"
                >
            <v-btn flat
                    v-for="tabId in categories.length"
                    :key="tabId"
                    :outline="activeTab === tabId-1"
                    @click="setActiveTab(tabId-1)"
                    :color="tabId === categories.length
                            ? 'rgb(251, 114, 0)' : ''"
                    >
                {{ categories[tabId-1] }}
            </v-btn>
        </v-layout>
        <v-layout>
            <v-flex xs-and-up12>
                <v-data-iterator
                        row
                        wrap
                        hide-actions
                        :items="items"
                        :rows-per-page-items="rowsPerPageItems"
                        content-tag="v-layout"
                        :total-items="total"
                        no-data-text=""
                        >
                    <template v-slot:item="{ item }">
                        <v-flex
                                xs12 sm6 md4 lg4 xl3 px-3 py-4>
                            <offer-card
                                    :model="item"></offer-card>
                        </v-flex>
                    </template>
                </v-data-iterator>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
import _ from 'lodash'

import OfferCard from '../components/offer_card.vue'
import { mapState, mapGetters, mapMutations, mapActions } from 'vuex'


export default {
    name: 'Market',
    components: {
        OfferCard,
    },

    props: [],
    data () {
        return {
        }
    },

    created () {
        let params = window.location.search.substring(1).split('&').reduce(
            (result, item) => {
                result[item.split('=')[0]] = item.split('=')[1] || null
                return result
        }, {})

        if (params['category']) {
            this.setActiveTab(parseInt(params['category'], 10))
        } else {
            this.load ()
        }
    },
    destroyed () {
    },

    methods: {
        ...mapActions('market', [
            'setActiveTab',
            'load',
        ]),

        ...mapMutations('market', [
            'nextItems',
        ]),

        ...mapMutations([
            'setShowMore',
        ]),
    },

    computed: {
        ...mapState('market', [
            'activeTab',
            'categories',
            'items',
            'rowsPerPageItems',
            'pagination',
        ]),

        ...mapState([
            'searchText',
            'scroll',
        ]),

        ...mapGetters('market', [
            'total',
            'hasMore',
        ])
    },
    watch: {
        searchText (searchText){
            this.load ()
        },

        hasMore () {
            this.setShowMore(this.hasMore)
        }
    }
}
</script>
<style scoped lang="styl">
primary_green_color = #e2ffbc
green_text_color = #151911

.products-container
    padding-left: 0
    padding-right: 0
    padding-top: 0

    .categories-container
        background-color: primary_green_color
</style>
