const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: './src/index.js', // Entry point of the application
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js',
    clean: true, // Cleans the output directory before building
  },
  mode: 'development', // Change to 'production' for production builds
  devServer: {
    static: path.join(__dirname, 'dist'),
    port: 3001,
    open: true, // Automatically open the browser
    hot: true, // Enable hot module replacement
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/, // For JavaScript and JSX files
        exclude: /node_modules/,
        use: 'babel-loader',
      },
      {
        test: /\.css$/, // For CSS files
        use: ['style-loader', 'css-loader'],
      },
      {
        test: /\.(png|jpg|jpeg|gif|svg)$/i, // For image files
        type: 'asset/resource',
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'], // Resolve these extensions
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './public/index.html', // Use your HTML file as a template
    }),
  ],
};
