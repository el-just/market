module.exports = {
    outputDir: 'dist/',
    devServer: {
        proxy: 'http://backend:6543',
        port: 5000,
    }
}
