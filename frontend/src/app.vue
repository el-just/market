<template>
<v-app
        v-scroll="onScroll"
        v-show="serviceEnabled"
        >
    <v-toolbar app flat fixed clipped-right
            :dense="true"
            :class="[
                'toolbar-container',
                showNavigation && !isMobile ? 'navigation-showed': '',
                marketInfoWidth === this.toolbarConfig.marketInfoShortWidth ?
                    'short-market-info' : '',
                searchHidden ?
                    'search-hidden' : '',
                forceSearch ?
                    'force-search' : '',
               ]"
            >
        <v-layout fill-height>
            <v-flex xs3 sm3 lg3 xl3
                    class="market-info font-weight-medium"
                    align-self-center
                    v-if="marketInfoWidth !== 0"
                    >
                    <div style="float:left">
                        <router-link to="/"
                                style="text-decoration: none; color: black;
                                       margin-left: 8px;
                                       font-size: 24px;"
                                >VEGGIES</router-link>
                        <div v-if="marketInfoWidth ===
                                       this.toolbarConfig.marketInfoShortWidth"
                                style="margin: -8px 3px 4px">
                            Санкт-Петербург
                        </div>
                    </div>
                    <div v-if="marketInfoWidth !==
                                   this.toolbarConfig.marketInfoShortWidth"
                            style="font-size: 14px; white-space: normal;
                                width: 228px; color: #9e9e9e;
                                padding-left: 12px; padding-right: 23px;
                                line-height: 20px;
                                margin-left: 110px">
                        Доставка овощей и фруктов в Санкт-Петербурге
                    </div>
            </v-flex>
            <v-flex
                    :class="[
                        marketInfoWidth === 0 ? 'xs12 sm12 lg12 xl12'
                            : 'xs9 sm9 lg9 xl9']">
                <v-badge right overlap color="black"
                        style="float: right"
                        :class="[
                            'cart-button-container',
                            count > 0 ? 'items-in-cart' : '']"
                        v-show="!showNavigation"
                        >
                    <template v-slot:badge v-if="count > 0">
                        <span class="caption">{{ count }}</span>
                    </template>
                    <v-btn flat
                            class="cart-button"
                            @click="showNavigation = !showNavigation"
                            >
                        <icon-cart 
                                width="26"
                                height="26"
                                ></icon-cart>
                    </v-btn>
                </v-badge>
                <div style="float: right; text-align: center; width: 72px;
                            position: relative; height: 100%">
                    <login-button
                        ></login-button>
                </div>
                <v-text-field
                        class="search-field"
                        flat
                        solo
                        v-model="searchTextLink"
                        color="rgba(0,0,0,0.54)"
                        ref="searchField"
                        >
                    <template v-slot:append>
                        <icon-search
                                style="fill: rgba(0,0,0,0.8)"
                                :width="16"
                                :height="16"
                                @click="toggleSearch"
                                ></icon-search>
                    </template>
                </v-text-field>
            </v-flex>
        </v-layout> 
    </v-toolbar>
    <v-content
            style="background-color: white">
        <router-view
                ref="routerComponent"
                ></router-view>
    </v-content>
    <v-footer
            height="auto"
            :class="[showNavigation && !isMobile ? 'navigation-showed': '']"
            >
        <v-container class="footer-container">
            <v-layout row
                    class="footer-button">
                <v-flex xs3 sm3 md3 lg3 xl3>
                </v-flex>
                <v-flex xs6 sm6 md6 lg6 xl6 text-xs-center>
                    <v-btn outline style="margin: 0;"
                            v-show="showMore"
                            @click="nextItems"
                            >
                        Показать ещё
                    </v-btn>
                </v-flex>
                <v-flex xs3 sm3 md3 lg3 xl3 text-xs-right
                        style="min-width: 128px"
                        >
                    <v-btn flat style="margin: 0;"
                            v-show="showUp"
                            @click="$vuetify.goTo(0, {
                                duration: 600, easing:'easeInOutCubic'})"
                            >
                        Наверх
                        <v-icon style="transform: rotate(-90deg)">
                            last_page
                        </v-icon>
                    </v-btn>
                </v-flex>
            </v-layout>
            <v-layout row wrap
                    class="footer-content">
                    <a
                            @click="openRoute('/confidentialPolicies.html')"
                            >
                        Соглашение о конфиденциальности
                    </a>
                    <a
                            @click="openRoute('/deliveryPolicies.html')"
                            >
                        Соглашение об условиях доставки
                    </a>
                    <a
                            @click.stop="openContacts">
                        Написать
                    </a>
                    <v-dialog
                            v-model="contactDialogShowed"
                            max-width="62%"
                            :content-class="[fullScreenMenus
                                ? '' : 'contact-dialog']"
                            :transition="fullScreenMenus
                                ? 'dialog-bottom-transition'
                                : null"
                            :fullscreen="fullScreenMenus"
                            >
                        <contacts ref="contacts"
                                v-touch="{
                                    left: ()=>contactDialogShowed=false,
                                    right: ()=>contactDialogShowed=false,
                                    up: ()=>contactDialogShowed=false,
                                    down: ()=>contactDialogShowed=false,
                                    }"
                                ></contacts>
                    </v-dialog>
                    <v-spacer></v-spacer>
                    <span>© Veggies</span>
            </v-layout>
        </v-container>
    </v-footer>
    <v-navigation-drawer app right floating
            width="350"
            class="cart-container"
            v-model="showNavigation"
            >
        <cart></cart>
    </v-navigation-drawer>
</v-app>
</template>

<script>
import Vue from 'vue'

import Cart from './components/cart.vue'
import IconCart from './components/icons/icon_cart.vue'
import IconSearch from './components/icons/icon_search.vue'
import LoginButton from './components/login_button.vue'
import Contacts from './components/contacts.vue'

import { mapState, mapGetters, mapMutations, mapActions } from 'vuex'


export default {
    name: 'App',
    components: {
        Cart,
        IconCart,
        IconSearch,
        LoginButton,
        Contacts,
    },


    props: [],
    data () {
        return {
            searchTextLink: null,

            showUp: false,
            contactDialogShowed: false,

            forceSearch: false,
            toolbarConfig: {
                marketInfoShortWidth: 138,
                marketInfoFullWidth: 333,
                searchMinWidth: 135,
            }
        }
    },

    created () {
        // this.$options.sockets.onmessage = (data) => console.log(data)

        this.searchTextLink = this.searchText
        fetch(`/api/user/info`, {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                return response.json()
            })
            .then(result => {
                this.setAll(result.data)
                if (result.data.cart) {
                    this.replace(result.data.cart.items.reduce((result, item)=>{
                        if (item.count > 0) {
                            result.push(item)
                        }

                        return result
                    }, []))
                }
            })
            .catch(exp => {
                console.error(exp)});
        fetch('/api/market/get_stage', {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                return response.json()
            })
            .then(result => {
                this.stage = result.stage
            })
    },
    destroyed () {
        // delete this.$options.sockets.onmessage
    },

    methods: {
        onScroll (e) {
            let offset = window.pageYOffset
                         || document.documentElement.scrollTop
            let clientHeight = document.documentElement.clientHeight
            let fullHeight = document.body.clientHeight

            this.showUp = offset / clientHeight > 0.2


            //this.updateScroll ({ offset, clientHeight, fullHeight }, this)
        },

        updateScroll: _.debounce ((scroll, self) => {
            //self.setScroll (scroll)
        }, 50),

        scrollUp() {
            window.scrollTo({
                top: 0,
                left: 0,
                behavior: 'smooth'
            })
        },

        openRoute (route) {
            window.open(route, '_blank');
        },

        nextItems () {
            if (this.$refs.routerComponent.nextItems) {
                let hasMore = this.$refs.routerComponent.nextItems()
            }
        },

        openContacts () {
            this.contactDialogShowed = true
            this.sendButtonText = 'Send'
            setTimeout(()=>{
                this.$refs.contacts.focusMessage()
            }, 0)
        },

        toggleSearch (target) {
            if ((this.forceSearch && !this.searchText)
                    || this.searchHidden) {
                this.forceSearch = !this.forceSearch
                if (!this.forceSearch) {
                    this.$refs.searchField.blur()
                }
            }
        },

        ...mapActions([
            'setSearchText'
        ]),

        ...mapMutations([
            'setScroll'
        ]),
        ...mapMutations('cart', [
            'replace'
        ]),

        ...mapMutations('user', [
            'setAll',
        ]),
    },

    computed: {
        ...mapState([
            'searchText',
            'showMore',
        ]),

        ...mapGetters('cart', [
            'count',
        ]),

        showNavigation: {
            get () {
                return this.$store.state.showNavigation
            },
            set (value) {
                this.$store.commit('setShowNavigation', value)
            },
        },

        isMobile () {
            return this.$vuetify.breakpoint.width <= 1264
        },

        searchHidden () {
            if (this.forceSearch) {
                return false
            }

            return this.$vuetify.breakpoint.width < (72*2
                                            + this.toolbarConfig.searchMinWidth
                                            + this.marketInfoWidth)
        },

        marketInfoWidth () {
            let shortMarketInfo = this.$vuetify.breakpoint.width < (72*3 +
                                        this.toolbarConfig.marketInfoFullWidth)

            if (this.forceSearch) {
                return !shortMarketInfo ?
                       this.toolbarConfig.marketInfoShortWidth
                       : 0
            }

            return shortMarketInfo
                   ? this.toolbarConfig.marketInfoShortWidth
                   : this.toolbarConfig.marketInfoFullWidth
        },

        fullScreenMenus () {
            return (
                this.marketInfoWidth === 0 || ( this.marketInfoWidth ===
                    this.toolbarConfig.marketInfoShortWidth &&
                        !this.forceSearch )
            )
        },

        serviceEnabled () {
            return ( window.location.search === '?test'
                    || this.stage === 'production' )
        },

        stage: {
            get () {
                return this.$store.state.stage
            },
            set (value) {
                this.$store.commit('setStage', value)
            },
        },
    },
    watch: {
        searchTextLink () {
            this.setSearchText (this.searchTextLink)
        }
    }
}
</script>
<style lang="styl">
secondary_background_color = #fffff5
primary_green_color = #e2ffbc
primary_yellow_color = #fffdbc

.buttons-container
    min-width: 136px
    line-height: 100%

.cart-container
    background-color: secondary_background_color !important

.toolbar-container
    background-color: white !important
    border-bottom: 1px solid primary_green_color

    .v-toolbar__content
        padding-right: 0 !important
        padding-left: 6px !important

    .user-button
        position:absolute
        top:50%
        margin: 0
        transform: translate(-50%, -50%)

    &.navigation-showed
        .search-field
            width: calc(100% - 72px);

    &.force-search
        .search-field
            .v-input__append-inner
                cursor: pointer

    .search-field
        width: calc(100% - 144px);

        float: right;
        margin: 5px 0

        .v-text-field__details
            display: none

        .v-input__control
            .v-input__slot
                margin-bottom: 0
            min-height: 36px !important
        &:hover
        &.v-input--is-focused
            border: 1px solid #a0ddf5

        border: 1px solid #d3f0fb
        border-radius: 2px

    &.short-market-info
        .market-info
            min-width: 138px

    .market-info
        min-width: 333px

    &.search-hidden
        .search-field
            border: 0
            .v-input__slot
                padding: 0
                cursor: pointer
            input
                display: none

.navigation-showed
    width: calc(100% - 350px)

.cart-button-container
    text-align: center
    height:100%
    background-color: primary_yellow_color

    width: 72px

    margin: 0
    padding: 0

    .cart-button
        height: 100%
        margin: 0
        padding: 0

        width: 100%
        border-radius: 0



    .cart-button
        margin-right: 0
        margin-left: 0
        min-width: 0

    &.items-in-cart
        .v-btn__content    
            margin-right: 12px

    .v-badge__badge
        top: 3px
        right: 7px

    .caption
        line-height: 12px

.scroll-button-container
    z-index: 100
    width: 100%
    position: fixed
    bottom: 0
    text-align: center

    &.navigation-showed
        .scroll-button
            margin-right: 350px

.footer-container
    width: 100%
    max-width: 100%
    padding: 0
    .footer-button
        background-color: secondary_background_color
        padding: 12px
    .footer-content
        background-color: white;

        padding: 12px 0

        a
            color: #9E9E9E
            margin: 0 12px
            &:hover
                text-decoration: underline

        span
            color: #9E9E9E
            margin-right: 12px
            cursor: default

.contact-dialog
    height: 62%
</style>
<style lang="styl">
aside::-webkit-scrollbar
    display: none
</style>
