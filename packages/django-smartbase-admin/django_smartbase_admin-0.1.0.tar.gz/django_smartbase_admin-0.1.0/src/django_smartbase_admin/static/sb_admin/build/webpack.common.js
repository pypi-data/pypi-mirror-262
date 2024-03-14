const path = require('path');
const webpack = require('webpack');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const BundleTracker = require('webpack-bundle-tracker');
const ESLintPlugin = require('eslint-webpack-plugin');

const entries = {
    main: './static/sb_admin/src/js/main.js',
    table: './static/sb_admin/src/js/table.js',
    chart: './static/sb_admin/src/js/chart.js',
    main_style: './static/sb_admin/src/css/style.css',
    translations: './static/sb_admin/src/js/translations.js',
};

const projectRoot = process.env.PWD || process.cwd();

module.exports = {
    resolve: {
        symlinks: false
    },
    entry: entries,
    output: {
        clean: {
            keep: /sprites/
        },
        filename: '[name].[contenthash].js',
        path: path.resolve(projectRoot, './static/sb_admin/dist')
    },
    module: {
        rules: [
            {
                test: /\.m?js$/,
                exclude: /(node_modules|bower_components)/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env'],
                        targets: "defaults",
                        plugins: ['@babel/plugin-proposal-optional-chaining']
                    }
                }
            },
            {
                test: /\.css$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    {
                        loader: 'css-loader',
                        options: {
                            sourceMap: true,
                        },
                    },
                    {
                        loader: "postcss-loader",
                        options: {
                            postcssOptions: {
                                config: path.resolve(projectRoot, './static/sb_admin/build/postcss.config.js'),
                            }
                        },
                    },
                ],
            },
        ]
    },
    plugins: [
        new ESLintPlugin({
            files: ['./static/sb_admin/src/**/*.js'],
        }),
        new MiniCssExtractPlugin({
            filename: '[name].[contenthash].css',
        }),
        new BundleTracker({
            filename: './static/sb_admin/webpack-stats.json'
        }),
        new webpack.DefinePlugin({
            'process.env.BUILD': JSON.stringify('web'),
        }),
    ]
};
