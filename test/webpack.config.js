const path = require('path');

module.exports = {
  entry: './content.js', // Entry point of your content script
  output: {
    path: path.resolve(__dirname, 'dist'), // Output directory for bundled files
    filename: 'bundle.js', // Name of the bundled file
  },
};
