export default {
    emailRegexp: new RegExp(/^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/),

    detransliterate (text) {
        let ruText = text.toLowerCase()
        let letters = {
            'a' : [new RegExp('a', 'g'), 'а'],
            'b' : [new RegExp('b', 'g'), 'б'],
            'v' : [new RegExp('v', 'g'), 'в'],
            'g' : [new RegExp('g', 'g'), 'г'],
            'd' : [new RegExp('d', 'g'), 'д'],
            'e' : [new RegExp('e', 'g'), 'е'],
            'z' : [new RegExp('z', 'g'), 'з'],
            'i' : [new RegExp('i', 'g'), 'и'],
            'y' : [new RegExp('y', 'g'), 'й'],
            'j' : [new RegExp('j', 'g'), 'й'],
            'k' : [new RegExp('k', 'g'), 'к'],
            'l' : [new RegExp('l', 'g'), 'л'],
            'm' : [new RegExp('m', 'g'), 'м'],
            'n' : [new RegExp('n', 'g'), 'н'],
            'o' : [new RegExp('o', 'g'), 'о'],
            'p' : [new RegExp('p', 'g'), 'п'],
            'r' : [new RegExp('r', 'g'), 'р'],
            's' : [new RegExp('s', 'g'), 'с'],
            't' : [new RegExp('t', 'g'), 'т'],
            'u' : [new RegExp('u', 'g'), 'у'],
            'f' : [new RegExp('f', 'g'), 'ф'],
            'h' : [new RegExp('h', 'g'), 'х'],
            '\'' : [new RegExp('\'', 'g'), 'ь'],
            'e' : [new RegExp('e', 'g'), 'э'],}

        let multipleLetters = {
            'zh' : [new RegExp('zh', 'g'), 'ж'],
            'ts' : [new RegExp('ts', 'g'), 'ц'],
            'ch' : [new RegExp('ch', 'g'), 'ч'],
            'sh' : [new RegExp('sh', 'g'), 'ш'],
            'sch' : [new RegExp('sch', 'g'), 'щ'],
            'yu' : [new RegExp('yu', 'g'), 'ю'],
            'ya' : [new RegExp('ya', 'g'), 'я'],
            'ju' : [new RegExp('ju', 'g'), 'ю'],
            'ja' : [new RegExp('ja', 'g'), 'я'],}

        for (let letterTranslit of Object.keys(multipleLetters)) {
            let letter = multipleLetters[letterTranslit][1]
            ruText = ruText.replace(
                    multipleLetters[letterTranslit][0], letter)
        }

        for (let letterTranslit of Object.keys(letters)) {
            let letter = letters[letterTranslit][1]
            ruText = ruText.replace(letters[letterTranslit][0], letter)
        }

        return ruText
    },

    CountForms (declensions) {
        let self = this
        this.currentForm = declensions[0]
        this.setCount = function (count) {
            let stringCount = count+''

            if (['0', '5', '6', '7', '8', '9'].indexOf(
                    stringCount[stringCount.length - 1]) !== -1 ||
                        stringCount[stringCount.length - 2] == '1') {
                self.currentForm  = declensions[2]
            } else if (stringCount[stringCount.length - 1] == '1') {
                self.currentForm  = declensions[0] || declensions[0]
            } else if (['2', '3', '4'].indexOf(
                    stringCount[stringCount.length - 1]) !== -1) {
                self.currentForm  = declensions[1] || declensions[0]
            }

            return self.currentForm
        }
    },
}
