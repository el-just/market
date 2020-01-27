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
                 Veggies, это что?
            </v-flex>
            <v-flex xs12 sm12 md12 lg12 xl12 pa-3
                    class="subheading"
                    >
                Люди, бывавшие на рынках, обычно делятся на два типа. Одним, это
                безумно нравится, а другие, побывав там по наводке восхищенных
                друзей, больше никогда туда не возвращаются. И их можно понять.
                Рынок, это место где нужно всегда быть на чеку. Нужно общаться,
                проверять товар, протискиваться между тележками. Но знаете что?
                Уж если вы там "освоились", то вам открыта дорога к вкуснейшим
                сезонным фруктам, ягодам и овощам. Таким, которых вы не найдете
                в привычных супермаркетах.
                <br/><br/>
                Так что же такое Veggies? Veggies - это люди, которые
                знают, где на рынках лежит все самое свежее и вкусное. Они
                выберут для вас как для себя. Позвонят, если чего-то нет,
                или наоборот есть, что-то очень спелое сезонное. А после,
                бережно и ничего не помяв, доставят к вам домой.
            </v-flex>
        </v-layout>
        <v-layout row wrap my-4>
            <v-flex xs12 sm12 md12 lg12 xl12
                     class="headline">
                Цены такие-же как на рынке?
            </v-flex>
            <v-flex xs12 sm12 md12 lg12 xl12 pa-3
                    class="subheading"
                    >
                Мы стараемся держать цены на уровне рынка. Но на некоторые
                позиции, мы можем незначительно поднимать цены, чтобы иметь
                пространство для торга. Иногда можно, купить чуть-чуть дороже,
                но получить гарантированно хороший товар. Мы этим, непременно,
                пользуемся.
            </v-flex>
        </v-layout>
        <v-layout row wrap my-4>
            <v-flex xs12 sm12 md12 lg12 xl12
                     class="headline">
                Что еще нужно знать?
            </v-flex>
            <v-flex xs12 sm12 md12 lg12 xl12 pa-3
                    class="subheading"
                    >
                Мы берем плату за выбор товара и его доставку. Поэтому, совсем
                мальнькие заказы будут невыгодны. Заказ в 700-1000₽ + наши
                услуги, по цене выйдут как товары из супермаркета, только с
                доставкой на дом. А суммы больше, уже будут заметно выгодней
                магазинных.
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
