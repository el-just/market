<template>
    <v-container class="info-container">
        <v-layout>
            <v-flex>
                <slot></slot>
            </v-flex>
        </v-layout>
    </v-container>
</template>
<script>
export default {
    name: 'CarouselInfo',
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
    },

    computed: {
    },
    watch: {
    },
}
</script>
<style scoped lang="styl">
.info-container
    background-color: rgba(255,253,188,0.75);
    margin: 0

</style>
