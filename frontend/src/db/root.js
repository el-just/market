export default {
    entities () {
        return {
            id: undefined,
            name: undefined,
            object: undefined,
            data_created: undefined,
            paused: undefined,
            declensions: [],
        }
    },

    products () {
        return {
            id: undefined,
            entity_id: undefined,
            parent_id: undefined,
            is_node: undefined,

            manufacturer_id: undefined,

            name: undefined,
            descriptions: undefined,
            img: undefined,
        }
    },

    offers () {
        return {
            id: undefined,
            entity_id: undefined,
            parent_id: undefined,
            is_node: undefined,
            
            name: undefined,
            weight: undefined,
            price: undefined,
            count_type: 0,
        }
    },

    manufacturers () {
        return {
            id: undefined,
            entity_id: undefined,
            name: undefined,
            country_id: undefined,
        }
    }
}
