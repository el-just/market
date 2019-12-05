<template>
    <v-list expand>
        <template
                v-for="(filter, group) in structure"
                >
            <v-text-field
                    :placeholder="filter.title"
                    single-line
                    append-icon="search"
                    color="white"
                    hide-details
                    v-model="currentState[group].searchText"
                    />
            <v-list-tile v-if="filteredFilters(group).length > 0"
                    v-for="(item, key) in visibleFilters(group)"
                    :key="item.id"
                    @click="activateFilter(group, item)"
                    v-model="item.active"
                    >
                <v-list-tile-content>
                    <v-list-tile-title>
                        {{ item.title }}
                    </v-list-tile-title>
                </v-list-tile-content>
            </v-list-tile>
            <v-subheader v-if="filteredFilters(group).length === 0">
                No results
            </v-subheader>
            <v-btn  v-if="!currentState[group].hideFilters || filteredFilters(group).length - visibleFilters(group).length > 0"
                    @click="currentState[group].hideFilters = !currentState[group].hideFilters"
                    flat small color="primary"
                    >
                    {{currentState[group].hideFilters ? '+'+(filteredFilters(group).length - visibleFilters(group).length)  : 'Hide'}}
            </v-btn>
        </template>
    </v-list>
</template>
<script>
import Vue from 'vue';

export default {
    name: 'SideFilter',
    compontents: {
    },

    props: ['structure', 'value'],
    data () {
        return {
            currentState: this.generateState(this.structure)
        }
    },
    computed: {
    },

    created () {
    },

    methods: {
        generateState (structure) {
            let state = {}
            let value = {}
            Object.keys(structure).forEach((key)=>{
                state[key] = {
                    hideFilters: true,
                    searchText: null,
                    activeFilters: []
                }
                value[key] = []
            })
            this.$emit('input', value)
            return state
        },
        filteredFilters (group){
            let
                self = this,
                items = self.structure[group].items.slice(0);

            if (self.currentState[group].searchText) {
                items = items.filter(
                    function (item) {
                        return (item.title.indexOf(
                                    self.currentState[group].searchText) !== -1 
                                && item.title !== 'All')
                    })
            }

            return items
        },

        visibleFilters (group){
            let
                sliceRange = 4,
                items = this.filteredFilters(group);

            if (!this.currentState[group].hideFilters) {
                return items
            }

            sliceRange = this.currentState[group].activeFilters.length < 3
                    ? sliceRange
                    : this.currentState[group].activeFilters.length + 1;

            return items.slice(0, sliceRange)
        },

        activateFilter(group, item){
            let key = this.structure[group].items.indexOf(item)
            Vue.set(this.structure[group].items[key], 'active', 
                !this.structure[group].items[key].active)
            
            if (key === 0) {
                this.currentState[group].activeFilters = [];
                let newValue = Object.assign({}, this.value)
                newValue[group] = [];
                this.$emit('input', newValue, group, 'clear')
                for (let idx=1; idx<this.structure[group].items.length; idx++){
                    Vue.set(this.structure[group].items[idx], 'active', false);
                }
            } else {
                if (this.structure[group].items[key].active) {
                    this.currentState[group].activeFilters.push(item)

                    let newValue = Object.assign({}, this.value)
                    newValue[group].push(item.id);
                    this.$emit('input', newValue, group, 'add', item.id)
                }
                else {
                    let valueGroup = []

                    this.currentState[group].activeFilters = this.currentState[group].activeFilters.filter(
                        function(active){
                            if (active !== item) {
                                valueGroup.push(active.id)
                            }
                            return active !== item
                        }
                    )
                    
                    let newValue = Object.assign({}, this.value)
                    newValue[group] = valueGroup;
                    this.$emit('input', newValue, group, 'removes', item.id)
                }

                Vue.set(this.structure[group].items[0], 'active',
                    this.currentState[group].activeFilters.length ? false : true)
            }

            if (this.currentState[group].hideFilters && this.currentState[group].activeFilters.length) {
                this.sortFilters(group)
            }
        },

        sortFilters(group) {
            let items = this.structure[group].items.slice(0)
            let hidedFilters = this.currentState[group].activeFilters.filter(function(item){
                return items.indexOf(item) > 3
            })

            if (hidedFilters.length > 0) {
                items.sort(function (next, current) {
                    if (current.title === 'All') {
                        return 1
                    }

                    if (next.active > current.active) {
                        return -1
                    }

                    if (next.active < current.active) {
                        return 1
                    }

                    return 0
                })

                this.structure[group].items = items
            }
        }
    },
    watch: {
        structure(value){
            this.currentState = this.generateState(value)
        },
        currentState: {
            handler (newState, oldState){
                if (Object.keys(oldState).length > 0) {
                    Object.keys(newState).forEach((key)=>{
                        if (newState[key].hideFilters
                                && newState[key].activeFilters.length) {
                            this.sortFilters(key)
                        }
                    })
                }
            },
            deep: true
        },
    },
}
</script>
