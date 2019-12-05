<template>
	<v-container>
		<v-layout>
			<v-flex text-xs-center class="title">
				<router-link to="/admin/products">Products</router-link>
			</v-flex>
			<v-flex text-xs-center class="title">
				<router-link to="/admin/offers">Offers</router-link>
			</v-flex>
			<v-flex text-xs-center class="title">
				<router-link to="/admin/sales">Sales</router-link>
			</v-flex>
		</v-layout>
	</v-container>
</template>
<script>
export default {
    name: 'admin',
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
</style>
