module.exports = {
    // The Webpack config to use when compiling your react app for development or production.
    webpack: function (config, env) {
        return {
            ...config,
            module: {
                ...config.module,
                rules: [
                    // See https://github.com/acrazing/mobx-sync/issues/14#issuecomment-469519335 - if ever resolved get rid of react-app-rewired
                    { test: /\.mjs$/, type: 'javascript/auto' },
                    ...config.module.rules
                ]
            }
        };
    },
}