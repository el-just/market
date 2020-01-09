<template>
    <v-layout :class="[
            small !== undefined ? 'offer-selector--small' : '',
            offerMenuItems.length && !hideDropdown ? ''
                : 'offer-selector--no-dropdown']">
        <v-flex xs4 sm4 md4 lg4 xl4>
            <v-menu bottom offset-y
                    :attach="`.selector-button__${$_uid}`"

                    v-model="menuOpened"
                    >
                <template v-slot:activator="{}">
                    <div
                            @click="menuOpened = 
                                offerMenuItems.length && !hideDropdown ?
                                !menuOpened : menuOpened"
                            :class="['selector-button',
                                `selector-button__${$_uid}`,
                                ...[
                                    menuOpened ? 'selector-button--is-focused'
                                    : ''
                                ]]">
                        <div class="selector-button__offer-container">
                            <button
                                    class="body-2 font-weight-regular
                                        selector-button__offer-format"
                                    :title="item.offerModel.offer.name"
                                    >
                                {{ item.offerModel.offer.name }}
                            </button>
                            <v-icon
                                    v-if="offerMenuItems.length && !hideDropdown"
                                    class="selector-button__dropdown-icon"
                                    color="grey lighten-1"
                                    >
                                arrow_drop_down
                            </v-icon>
                        </div>
                        <div v-if="item.offerModel.offer.weight"
                                class="selector-button__weight">
                            &#8776{{ item.offerModel.offer.weight }} кг
                        </div>
                    </div>
                </template>
                <v-list
                        class="selector-menu__container">
                    <v-list-tile
                            v-for="menuItem in offerMenuItems"
                            :key="menuItem.offer.name"
                            @click="selectOffer({
                                        changedOffer: item.offerModel,
                                        newOffer: menuItem,
                                        item,
                                        meta,})"
                            >
                        <v-list-tile-title>
                            <v-layout>
                                <v-flex
                                        xs9 sm9 md9 lg9 xl9
                                        class="selector-menu__format-container"
                                        >
                                    <span
                                            class="selector-menu__format"
                                            >
                                        {{ menuItem.offer.name }}
                                    </span>
                                    <span v-if="menuItem.offer.weight"
                                            class="caption
                                            selector-menu__weight"
                                            >
                                        &#8776{{ menuItem.offer.weight }} кг
                                    </span>
                                </v-flex>
                                <v-flex
                                        xs3 sm3 md3 lg3 xl3
                                        class="selector-menu__amount"
                                        text-xs-right
                                        >
                                    {{ menuItem.offer.price }}₽
                                </v-flex>
                            </v-layout>
                        </v-list-tile-title>
                    </v-list-tile>
                </v-list>
            </v-menu>
        </v-flex>
        <v-flex xs8 sm8 md8 lg8 xl8
                align-self-center 
                justify-end
                :class="[
                    'count-editor', ...[
                        countEditorFocused ? 'count-editor--is-focused' : '',
                        Number(item.count) ? 'count-editor--positive-count' : '', 
                    ]]"
                >
            <v-btn outline
                    class="count-editor__add-action"
                    @click="processAction('add')"
                    >
                <v-icon>add</v-icon>
            </v-btn>
            <input
                    class="subheading body-2 font-weight-regular
                        count-editor__input"
                    v-show="Number(item.count) || countEditorFocused"

                    v-model="count"
                    @focus="countEditorFocused = true"
                    @blur="countEditorFocused = false"
                    >
            </input>
            <v-btn outline
                    class="count-editor__remove-action"
                    v-if="Number(item.count) || countEditorFocused"

                    @click="processAction('remove')"
                    >
                <v-icon>remove</v-icon>
            </v-btn>
            <div 
                    class="count-editor__amount font-weight-regular">
                {{ item.offerModel.offer.price }}₽
            </div>
        </v-flex>
    </v-layout>
</template>
<script>
import { mapGetters, mapState, mapMutations, mapActions } from 'vuex'

export default {
    name: 'OfferSelector',
    components: {
    },

    props: [
        'small',
        'item',
        'offerMenuItems',
        'hideDropdown',
        'meta',
    ],
    data () {
        return {
            menuOpened: false,
            countEditorFocused: false,
            count: null,
            action: null,
        }
    },

    created () {
        this.count = this.item.count
    },
    destroyed () {
    },

    methods: {
        ...mapActions ('cart', [
            'updateCount',
        ]),

        selectOffer (eventData) {
            this.$emit ('offerSelected', eventData)
        },

        processAction (actionName) {
            if (actionName === 'add') {
                this.count = Number(this.count) + 1
            } else if (actionName === 'remove') {
                this.count = Number(this.count) - 1 > 0 ?
                        Number(this.count) - 1 : 0
            }

            this.action = actionName
        }
    },

    computed: {
    },
    watch: {
        count (newValue, oldValue) {
            if ((Number(newValue) === Number(oldValue) && 
                    Number(newValue) !== 0) || oldValue === null) {
                return
            }

            let value = (this.count+'').replace(/\s/g, '')

            if (value !== '' && (Number(value) !== 0
                    || !this.countEditorFocused)) {
                let pattern = this.item.offerModel.offer.count_type === 0 ?
                        new RegExp(/\d+/g) : new RegExp(/\d+[,.]?\d{0,3}/g)
                let badPart = value.replace(pattern, '')

                if(badPart){
                    value = value.split(badPart)[0]
                } else if (value.match(pattern).length > 1) {
                    value = value.match(pattern)[0]
                }

                value = Number(value) < 0 ? 0 : value

                this.updateCount ({
                    offerModel: this.item.offerModel,
                    parentModel: this.item.parentModel,
                    count: Number(value),
                })

                if (this.action) {
                    this.$emit ('actionProceed', {
                        actionName: this.action,
                        count: Number(this.count),
                        item: this.item,
                        meta: this.meta,
                    })
                }
            }

            if (Number(this.count) !== Number(value)) {
                this.count = Number(value)
            }
        },

        countEditorFocused () {
            this.action = null
            if (!this.countEditorFocused && (
                    this.count === '' || Number(this.count) === 0)) {
                this.action = 'remove'
                this.count = 0
            }
        },

        item: {
            handler: function (item) {
                if (item.count !== this.count) {
                    this.count = item.count
                }
            },
            deep: true,
        }
    },
}
</script>
<style scoped lang="styl">
primary_green_color = #e2ffbc
primary_yellow_color = #fffdbc

green_border_color = #cee8ac
green_text_color = #151911

/* selector-button sizes */
.offer-selector--small
    .selector-button
        &:hover i
        &.selector-button--is-focused i
            color: #eae300 !important

        .selector-button__dropdown-icon
            font-size: 15px

        .selector-button__weight
            font-size: 10px !important

        .selector-button__offer-format
            font-size: 14px !important
            line-height: 16px

            max-width: 63px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: normal;
            text-align: left

        .selector-menu__container
            .selector-menu__format-container
                .selector-menu__format
                    font-size: 16px
                .selector-menu__weight
                    line-height: 33px
                    font-size: 10px !important
            .selector-menu__amount
                font-size: 16px

    .count-editor
        div
        input
        button
            height: 21px
            width: 27px

        .count-editor__add-action
        .count-editor__remove-action
            i
                font-size: 16px

        .count-editor__amount
            font-size: 16px


        .count-editor__add-action
            border: 1px solid #eae300
            background-color: primary_yellow_color !important

            i
                color: #424003 !important

        .count-editor__input
            font-size: 12px !important
            border-top: 1px solid #f2f0b3
            border-bottom: 1px solid #f2f0b3

        .count-editor__remove-action
            border: 1px solid #f2f0b3

            i
                color: #eae300

.selector-button
    div
        max-width: 100%

    &:hover i
    &.selector-button--is-focused i
        color: green_border_color !important

    .selector-button__dropdown-icon
        font-size: 18px

    .selector-button__weight
        font-size: 12px !important

    .selector-button__offer-format
        font-size: 16px !important
        line-height: 18px

        max-width: 72px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: normal;
        text-align: left

    .selector-menu__container
        .selector-menu__format-container
            .selector-menu__format
                font-size: 18px
            .selector-menu__weight
                line-height: 32px
        .selector-menu__amount
            font-size: 18px

.count-editor
    div
    input
    button
        height: 28px
        width: 36px

    .count-editor__add-action
    .count-editor__remove-action
        i
            font-size: 20px

    .count-editor__amount
        font-size: 20px

    .count-editor__add-action
        border: 1px solid green_border_color
        background-color: primary_green_color !important

        i
            color: green_text_color !important

    .count-editor__input
        font-size: 16px !important
        border-top: 1px solid primary_green_color
        border-bottom: 1px solid primary_green_color

    .count-editor__remove-action
        border: 1px solid primary_green_color

        i
            color: green_border_color

/* end of sizes */

.selector-button
    float: left
    cursor: pointer
    user-select: none

    transition: 0.3s cubic-bezier(0.25, 0.8, 0.5, 1)

    & button:focus
        outline: none

    &.selector-button--is-focused i
        transform: rotate(180deg)

    .offer-selector--no-dropdown &
    .offer-selector--no-dropdown & button
        cursor: default

    .selector-button__weight
        text-align: right
        margin-top: -4px
        color: #9e9e9e

    .selector-menu__container
        background-color: white !important
        min-width: 250px

        .selector-menu__format-container
            .selector-menu__format
                vertical-align: top
            .selector-menu__weight
                color: #9E9E9E

.count-editor
    div
    input
    button
        float: right
        min-width: 0
        padding: 0
        margin: 0

    input:focus
        outline: none

    &.count-editor--is-focused
    &.count-editor--positive-count
        .count-editor__add-action
            border-top-left-radius: 0
            border-bottom-left-radius: 0
    .count-editor__add-action
        border-radius: 2px

    .count-editor__input
        text-align: center

    .count-editor__remove-action
        border-top-right-radius: 0
        border-bottom-right-radius: 0

    .count-editor__amount
        width: auto !important
        margin-top: -1px !important
        margin-right: 6px !important
</style>
