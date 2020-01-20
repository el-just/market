<template>
<v-card
        class="contuct-us-dialog">
    <v-container>
        <v-layout row wrap>
            <v-flex xs12 sm12 md12 lg12 xl12
                     class="headline">
                 Рассказываем о новинках
            </v-flex>
            <v-flex xs12 sm6 md6 lg6 xl6 pa-3
                    class="subheading telegram-button"
                    @click="openInstagram"
                    >
                <v-layout>
                    <icon-instagram 
                            width="36"
                            height="36"
                            ></icon-instagram>
                    <v-flex align-self-center pl-2>
                        @veggies.market
                    </v-flex>
                </v-layout>
            </v-flex>
            <v-flex xs12 sm6 md6 lg6 xl6 pa-3
                    class="subheading"
                    >
                <v-layout>
                    <icon-telegram 
                            width="36"
                            height="36"
                            ></icon-telegram>
                    <v-flex align-self-center pl-2>
                        @veggies_market
                    </v-flex>
                </v-layout>
            </v-flex>
        </v-layout>
        <v-layout row wrap my-4>
            <v-flex xs12 sm12 md12 lg12 xl12
                     class="headline">
                Помогаем с покупками
            </v-flex>
            <v-flex xs12 sm6 md6 lg6 xl6 pa-3
                    class="subheading"
                    >
                <v-layout>
                    <icon-telegram 
                            width="36"
                            height="36"
                            ></icon-telegram>
                    <v-flex align-self-center pl-2>
                        @help_veggies_market
                    </v-flex>
                </v-layout>
            </v-flex>
            <v-flex xs12 sm6 md6 lg6 xl6 pa-3
                    class="subheading"
                    >
                <v-layout>
                    <icon-mail
                            width="36"
                            height="36"
                            ></icon-mail>
                    <v-flex align-self-center pl-2>
                        support@veggies.market
                    </v-flex>
                </v-layout>
            </v-flex>
        </v-layout>
        <v-layout row wrap>
            <v-flex xs12 sm12 md12 lg12 xl12
                     class="headline">
                Принимаем предложения
            </v-flex>
            <v-flex xs12 sm12 md12 lg12 xl12 pa-3>
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
            <v-flex xs12 sm12 md12 lg12 xl12 text-xs-center>
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
import IconInstagram from './icons/icon_instagram.vue'
import IconTelegram from './icons/icon_telegram.vue'
import IconMail from './icons/icon_mail.vue'

export default {
    name: 'Contacts',
    components: {
        IconInstagram,
        IconTelegram,
        IconMail,
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

            this.messageValid = this.message ?
                                this.message.replace(/\s/g, '').length > 0 :
                                false


            if (this.messageValid) {
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
            //this.$refs.messageArea.focus()
        },

        openInstagram () {
            window.open('https://www.instagram.com/veggies.market/', '_blank');
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

    .telegram-button:hover
        cursor: pointer
        text-decoration: underline

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
