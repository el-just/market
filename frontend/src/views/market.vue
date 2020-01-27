<template>
    <v-container fluid
            class="products-container"
            >
        <v-layout class="market-carousel-container">
            <v-carousel light :height="carouselHeight"
                    hide-delimiters
                    :cycle="false"
                    >
                <v-carousel-item
                        reverse-transition="fade"
                        transition="fade"
                        key="0"
                        :src="carousel[0]"
                        >
                    <v-layout justify-start>
                            <carousel-info
                                    :class="infoClasses"
                                    >
                                <v-layout justify-start>
                                    <span>
                                        Отбираем лучшее
                                    </span>
                                </v-layout>
                                <v-layout justify-end>
                                    <span>
                                        на рынках города
                                    </span>
                                </v-layout>
                                <v-layout justify-end>
                                    <v-btn flat
                                            color="rgb(251, 114, 0)"
                                            @click="aboutDialogShowed = true"
                                            >
                                        <icon-question
                                                :width="
                                                    $vuetify.breakpoint
                                                        .width < 350
                                                    ? 18 : 23"
                                                :height="
                                                    $vuetify.breakpoint
                                                        .width < 350
                                                    ? 18 : 23"
                                                style="margin-right: 4px"
                                                fill="rgb(251, 114, 0)"
                                                >
                                        </icon-question>
                                        <span>подробнее</span>
                                    </v-btn>
                                </v-layout>
                            </carousel-info>
                    </v-layout>
                </v-carousel-item>
                <v-carousel-item
                        reverse-transition="fade"
                        transition="fade"
                        key="1"
                        :src="carousel[1]"
                        >
                    <carousel-info
                            :class="infoClasses"
                            >
                        <v-layout justify-center>
                            <v-flex>
                                Не пропусти сезон!
                            </v-flex>
                        </v-layout>
                        <v-layout justify-start
                                class="carousel-info_second-line"
                                >
                            <span>Манго:&nbsp;</span>
                            <span style="color: rgb(251, 114, 0);">
                                50 - 120₽&nbsp;</span>
                            <span> за шт</span>
                        </v-layout>
                    </carousel-info>
                </v-carousel-item>
                <v-carousel-item
                        reverse-transition="fade"
                        transition="fade"
                        key="2"
                        :src="carousel[2]"
                        >
                    <carousel-info
                            :class="infoClasses"
                            >
                        <v-layout justify-center>
                            <v-flex>
                                Не пропусти сезон!
                            </v-flex>
                        </v-layout>
                        <v-layout justify-start
                                class="carousel-info_second-line"
                                >
                            <span>Хурма:&nbsp;</span>
                            <span style="color: rgb(251, 114, 0);">
                                35₽&nbsp;
                            </span>
                            <span> за шт</span>
                        </v-layout>
                    </carousel-info>
                </v-carousel-item>
            </v-carousel>
        </v-layout>
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
        <v-dialog
                content-class="offer-dialog"
                v-model="offerDialogShowed"
                >
        </v-dialog>
        <v-dialog
                v-model="aboutDialogShowed"
                min-width="62%"
                :transition="$vuetify.breakpoint.width < 500
                    ? 'dialog-bottom-transition'
                    : null"
                :fullscreen="$vuetify.breakpoint.width < 500"
                >
            <about
                    @dialogClosed="aboutDialogShowed = false"
                    >
            </about>
        </v-dialog>
    </v-container>
</template>

<script>
import _ from 'lodash'

import OfferCard from '../components/offer_card.vue'
import About from '../components/about.vue'
import CarouselInfo from '../components/carousel_info.vue'
import IconQuestion from '../components/icons/icon_question.vue'
import { mapState, mapGetters, mapMutations, mapActions } from 'vuex'


export default {
    name: 'Market',
    components: {
        OfferCard,
        IconQuestion,
        About,
        CarouselInfo,
    },

    props: [],
    data () {
        return {
            aboutDialogShowed: false,
        }
    },

    created () {
        let params = window.location.search.substring(1).split('&').reduce(
            (result, item) => {
                result[item.split('=')[0]] = item.split('=')[1] || null
                return result
        }, {})

        if (params['offer']) {
            this.setActiveOffer(parseInt(params['offer']))
        }

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
            'setActiveOffer',
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
            'offerDialogShowed',
            'offerModel',
            'carousel',
        ]),

        ...mapState([
            'searchText',
            'scroll',
        ]),

        ...mapGetters('market', [
            'total',
            'hasMore',
        ]),

        offerDialogShowed: {
            get () {
                return this.$store.state.market.offerDialogShowed
            },
            set (value) {
                this.$store.commit('setOfferDialogShowed', value)
            },
        },

        carouselHeight () {
            if (this.$vuetify.breakpoint.width < 350) {
                return 250
            } else if (this.$vuetify.breakpoint.width < 500) {
                return 300
            }

            return 400
        },

        infoClasses () {
            if (this.$vuetify.breakpoint.width < 350) {
                return ['carousel-info-tiny', 'carousel-info-container']
            } else if (this.$vuetify.breakpoint.width < 500) {
                return ['headline', 'carousel-info-medium', 'carousel-info-container']
            }
            return ['display-1', 'carousel-info-container']
        },
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
primary_yellow_color = #fffdbc
green_text_color = #151911

.market-carousel-container
    & >>> .v-carousel__controls
        background: primary_green_color
        opacity: 0.6

    .market-carousel-text-container
        background: primary_yellow_color
        width: 400px
        height: 141px;
        opacity: 0.75
        padding: 24px

    .carousel-info-container
        max-width: 400px;
        margin: 16px 16px 0 16px

        button
            margin: 0px
            padding: 0 8px

        .carousel-info_second-line
            font-size: 26px
            padding-left: 24px

        &.carousel-info-tiny
            max-width: 200px;
            font-size: 18px
            padding: 8px
            margin: 8px 8px 0 8px

            button
                font-size: 12px
                height: 26px
                padding: 0 4px

            .carousel-info_second-line
                font-size: 16px !important
                padding-left: 14px

        &.carousel-info-medium
            max-width: 300px;
            padding: 10px

            margin: 10px 10px 0 10px

            button
                padding: 0 8px

            .carousel-info_second-line
                font-size: 20px !important
                padding-left: 18px

.offer-dialog
    max-width: 400px

.products-container
    padding-left: 0
    padding-right: 0
    padding-top: 0

    .categories-container
        background-color: primary_green_color
</style>
