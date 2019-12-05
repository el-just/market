<template>
<v-card
        class="contuct-us-dialog">
    <v-container fill-height>
        <v-layout column justify-space-between>
            <v-flex xs1 sm1 lg1 xl1>
                <v-layout row>
                    <v-flex xs12 sm8 lg4 xl4>
                        <v-text-field solo flat hide-details
                                v-model="email"
                                :class="['input-field', 'email',
                                         ... [emailValid ? ''
                                              : 'validation-error']]"
                                browser-autocomplete="email"
                                placeholder="Ваш e-mail"
                                >
                        </v-text-field>
                    </v-flex>
                </v-layout>
            </v-flex>
            <v-flex xs10 sm10 lg10 xl10>
                <v-textarea solo flat hide-details
                    v-model="message"
                    :class="['input-field', 'message-area',
                             ... [messageValid ? ''
                                  : 'validation-error']]"
                    ref="messageArea"
                    no-resize
                    >
                </v-textarea>
            </v-flex>

            <v-flex  xs1 sm1 lg1 xl1 text-xs-center>
                <v-btn flat
                        :disabled="sent === false"
                        class="send-button"
                        color="rgb(71, 188, 234)"

                        @click="sendMessage"
                        >
                    {{sendButtonText}}
                </v-btn>
            </v-flex>
        </v-layout>
    </v-container>
</v-card>
</template>
<script>
import utils from '../utils.js'

export default {
    name: 'Contacts',
    components: {
    },

    props: [],
    data () {
        return {
            email: null,
            sendButtonText: 'Отправить',
            sent: undefined,
            message: null,
            emailValid: true,
            messageValid: true,
        }
    },

    created () {
    },
    destroyed () {
    },

    methods: {
        sendMessage () {
            let timeout = false
            let request = false

            this.emailValid = utils.emailRegexp.test(this.email)
            this.messageValid = this.message ?
                                this.message.replace(/\s/g, '').length > 0 :
                                false


            if (this.emailValid && this.messageValid) {
                this.sent = false
                this.sendButtonText = 'Отправляем ...'

                setTimeout (() => {
					timeout = true

                    if (request) {
                        this.sent = true
                        this.message = null
                        this.sendButtonText = 'Отправить еще'
                    }
                }, 700)

				fetch(`/api/message/create`, {
					method: 'POST',
					body: JSON.stringify({
                        "email":this.email,
                        "message":this.message,
                    }),
				})
				.then(response => {
					return response.json()
				})
				.then(result => {
					request = true
					if (timeout) {
                        this.sent = true
                        this.message = null
                        this.sendButtonText = 'Отправить еще'
					}
				})
                .catch(exp => {
                    });
            }
        },

        focusMessage () {
            this.$refs.messageArea.focus()
        },
    },

    computed: {
    },
    watch: {
        email () {
            if (!this.emailValid) {
                this.emailValid = utils.emailRegexp.test(this.email)
            }
        },
        message () {
            if (!this.messageValid) {
                this.messageValid = this.message ?
                                    this.message.replace(/\s/g, '').length > 0 :
                                    false
            }
        },
    },
}
</script>
<style scoped lang="styl">
color_error = #ffc28f
color_error_focused = #ffa559

.contuct-us-dialog
    background-color: #ffffff
    height: 100%

    .input-field
        border: 1px solid #d3f0fb
        border-radius: 2px

        &.validation-error
            border-color: color_error

            &:hover
            &.v-input--is-focused
                border-color: color_error_focused

        &:hover
        &.v-input--is-focused
            border-color: #a0ddf5

    .headline
        color: rgba(0, 0, 0, 0.72)

    .email
        & >>> .v-input__control
            min-height: 40px
        margin-bottom: 12px
    .message-area
        height: 100%
        margin-bottom: 4px

        & >>> textarea
            resize: none
            height: 100% !important

        & >>> div
            height: 100%

    .send-button
        margin-right: 0
</style>
