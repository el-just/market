<template>
<v-card
        class="about-dialog">
    <v-btn flat icon
            color="rgba(0,0,0,0.72)"
            style="position: absolute; top: 8px; right: 8px"
            @click="closeWindow"
            >
        <v-icon large>close</v-icon>
    </v-btn>
    <v-container>
        <v-layout row wrap>
            <v-flex xs12 sm12 md12 lg12 xl12
                     class="headline">
                 Veggies
            </v-flex>
            <v-flex xs12 sm12 md12 lg12 xl12 pa-3
                    class="subheading"
                    >
                Мы убеждены, что самое свежее, вкусное и дешевое можно найти
                только на фруктово-овощных базах, локальных рынках или у каких-то
                узкоспециализированных поставщиков/фермеров.
                <br/><br/>
                Мы постоянно актуализируем базу товаров, следим за качеством
                и ценами. В сезон, предлагаем сезонные фрукты и овощи.
                Упаковываем так, чтобы ничего не помялось, и доставляем вам
                домой.
            </v-flex>
        </v-layout>
    </v-container>
</v-card>
</template>
<script>
export default {
    name: 'About',
    components: {
    },

    props: [],
    data () {
        return {
        }
    },

    created () {
    },
    destroyed () {
    },

    methods: {
        closeWindow () {
            this.$emit ('dialogClosed')
        },
    },

    computed: {
    },
    watch: {
    },
}
</script>
<style scoped lang="styl">
.about-dialog
    background-color: #ffffff
</style>
