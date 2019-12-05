<template>
    <div :class="containerClass">
        <div class="top" ref="top"
                @mouseenter="topHovered(true)"
                @mouseleave="topHovered(false)"
                :style="{
                    'border-top-color': borders.topTop,
                    'border-right-color': borders.topRight,
                    'border-bottom-color': borders.topBottom,
                    'border-left-color': borders.topLeft,
                }"
                >
            <slot name="top-field"
                    :focusTop="focusTop"
                    :blurTop="blurTop"
                    :inputTop="inputTop"
                    ></slot>
        </div>
        <div class="bottom" ref="bottom"
                v-if="bottomVisible === false ? false : true"
                @mouseenter="bottomHovered(true)"
                @mouseleave="bottomHovered(false)"
                :style="{
                    'border-top-color': borders.bottomTop,
                    'border-right-color': borders.bottomRight,
                    'border-bottom-color': borders.bottomBottom,
                    'border-left-color': borders.bottomLeft,
                }"
                >
            <slot name="bottom-field"
                    :focusBottom="focusBottom"
                    :blurBottom="blurBottom"
                    :inputBottom="inputBottom"
                    ></slot>
        </div>
    </div>
</template>
<script>
import Vue from 'vue'

export default {
    name: 'DualField',
    components: {
    },

    props: ['bottomVisible', 'borderColor', 'borderColorFocused'],
    data () {
        return {
            containerClass: ['field-group', 'no-focus'],

            borders: {
                topTop: '#f2f0b3',
                topRight: '#f2f0b3',
                topBottom: '#f2f0b3',
                topLeft: '#f2f0b3',

                bottomTop: '#f2f0b3',
                bottomRight: '#f2f0b3',
                bottomBottom: '#f2f0b3',
                bottomLeft: '#f2f0b3',
            },

            color: '#f2f0b3',
            colorFocused: '#eae300',
            colorError: '#ffc28f',
            colorErrorFocused: '#ffa559',
        }
    },

    created () {
        this.color = this.borderColor ? this.borderColor : this.color
        this.colorFocused = this.borderColorFocused ? this.borderColorFocused
                             : this.colorFocused

        this.borders = this.getDefaultColors()
    },
    destroyed () {
    },

    methods: {
        getDefaultColors () {
            let colors = {}

            colors.topTop = this.color
            colors.topRight = this.color
            colors.topBottom = this.color
            colors.topLeft = this.color

            colors.bottomTop = this.color
            colors.bottomRight = this.color
            colors.bottomBottom = this.color
            colors.bottomLeft = this.color

            return colors
        },

        validate (field, control) {
            let newClasses = this.containerClass.slice()
            let errorClass = `${field}-validation-error`
            let controlContainer = this.$refs[field]
            let validate = ( control ? control.validate : undefined )
                            ||
                           ( control && control.target ? control.target.validate
                               : undefined )
            let isValid = validate ? validate() : (
                                controlContainer.querySelectorAll(
                                    '.error--text').length === 0)

            if (isValid) {
                newClasses = newClasses.filter((item)=>{
                    return item !== errorClass
                })
            } else if (newClasses.indexOf(errorClass) === -1) {
                newClasses.push(errorClass)
            }

            this.containerClass = newClasses
        },

        focus (field) {
            let newClasses = this.containerClass.filter((item)=>{
                return item !== 'no-focus'
            })

            newClasses.push(
                    field === 'top' ? 'top-focused' : 'bottom-focused')

            this.containerClass = newClasses
        },

        blur (field, control) {
            let newClasses = this.containerClass.filter((item)=>{
                return item !== (field === 'top' ? 'top-focused'
                        : 'bottom-focused')
            })

            if (newClasses.indexOf('no-focus') === -1 &&
                    newClasses.indexOf('top-focused') === -1 &&
                    newClasses.indexOf('bottom-focused') === -1 ) {
                newClasses.push('no-focus')
            }

            this.containerClass = newClasses
            this.validate(field, control)
        },


        inputTop() {
            let isValid = this.containerClass.indexOf(
                          'top-validation-error') === -1

            if (!isValid) {
                this.validate('top')
            }
        },
        inputBottom() {
            let isValid = this.containerClass.indexOf(
                          'bottom-validation-error') === -1
            if (!isValid) {
                this.validate('bottom')
            }
        },


        focusTop () {
            this.focus ('top')
        },
        blurTop (control) {
            this.blur ('top', control)
        },

        focusBottom () {
            this.focus ('bottom')
        },
        blurBottom (control) {
            this.blur ('bottom', control)
        },

        topHovered (hovered) {
            let newClasses = this.containerClass.filter((item)=>{
                return item !== 'top-hovered'
            })

            if (hovered) {
                newClasses.push('top-hovered')
            }

            this.containerClass = newClasses
        },
        bottomHovered (hovered) {
            let newClasses = this.containerClass.filter((item)=>{
                return item !== 'bottom-hovered'
            })

            if (hovered) {
                newClasses.push('bottom-hovered')
            }

            this.containerClass = newClasses
        },

        testState () {
            let state = {
                topHovered: false,
                bottomHovered: false,
                topFocused: false,
                bottomFocused: false,
                topError: false,
                bottomError: false,
            }

            this.containerClass.forEach((item) => {
                switch (item) {
                    case 'top-hovered':
                        state.topHovered = true
                        break
                    case 'bottom-hovered':
                        state.bottomHovered = true
                        break
                    case 'top-focused':
                        state.topFocused = true
                        break
                    case 'bottom-focused':
                        state.bottomFocused = true
                        break
                    case 'top-validation-error':
                        state.topError = true
                        break
                    case 'bottom-validation-error':
                        state.bottomError = true
                        break
                } 
            })

            return state
        },
    },

    computed: {
    },
    watch: {
        containerClass () {
            let state = this.testState()
            let colors = this.getDefaultColors()

            if (state.topError) {
                colors.topTop = this.colorError
                colors.topRight = this.colorError
                colors.topBottom = this.colorError
                colors.topLeft = this.colorError

                colors.bottomTop = this.colorError
            }
            if (state.bottomError) {
                colors.bottomTop = this.colorError
                colors.bottomRight = this.colorError
                colors.bottomBottom = this.colorError
                colors.bottomLeft = this.colorError

                colors.topBottom = this.colorError
            }

            if (state.topHovered || state.topFocused) {
                colors.topTop = state.topError ? this.colorErrorFocused
                                : this.colorFocused
                colors.topRight = state.topError ? this.colorErrorFocused
                                : this.colorFocused
                colors.topBottom = state.topError ? this.colorErrorFocused
                                : this.colorFocused
                colors.topLeft = state.topError ? this.colorErrorFocused
                                : this.colorFocused
            }

            if (state.bottomHovered || state.bottomFocused) {
                colors.bottomTop = state.bottomError ? this.colorErrorFocused
                                : this.colorFocused
                colors.bottomRight = state.bottomError ? this.colorErrorFocused
                                : this.colorFocused
                colors.bottomBottom = state.bottomError ? this.colorErrorFocused
                                : this.colorFocused
                colors.bottomLeft = state.bottomError ? this.colorErrorFocused
                                : this.colorFocused
            }

            this.borders = colors
        },
    },
}
</script>
<style scoped lang="styl">
border_color = #f2f0b3
border_color_focused = #eae300
error_color = #ffc28f
error_color_focused = #ffa559

.top
    border-top: 1px solid
    border-left: 1px solid
    border-right: 1px solid

    border-top-left-radius: 2px
    border-top-right-radius: 2px


.bottom
    border-bottom: 1px solid
    border-left: 1px solid
    border-right: 1px solid

    border-bottom-left-radius: 2px
    border-bottom-right-radius: 2px

.field-group
    & >>> .error--text
        color: inherit !important;
        caret-color: inherit !important;

    &.top-focused
        .top
            border: 1px solid

    &.bottom-focused
        .bottom
            border: 1px solid

    &.no-focus
        .top
            border-bottom: 1px solid

    &.no-focus:hover > .top
        border-bottom: 0

    &.no-focus
        .top:hover
            border-bottom: 1px solid
            border: 1px solid

    &.no-focus
        .bottom:hover
            border: 1px solid
</style>
