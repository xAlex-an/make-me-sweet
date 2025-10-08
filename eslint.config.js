// ESLint flat config format
export default [
  {
    files: ["**/*.js"],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "script",
      globals: {
        console: "readonly",
        document: "readonly",
        window: "readonly",
        setTimeout: "readonly",
        module: "readonly",
        MutationObserver: "readonly",
        bootstrap: "readonly"
      }
    },
    rules: {
      // Basic error prevention
      "no-unused-vars": "error",
      "no-undef": "error",
      "no-console": "off", // Allow console.log for debugging
      
      // Best practices
      "eqeqeq": "error",
      "curly": "error",
      "no-eval": "error",
      "no-implied-eval": "error",
      
      // Style rules
      "indent": ["error", 2],
      "quotes": ["error", "single"],
      "semi": ["error", "always"],
      "comma-dangle": ["error", "never"],
      
      // ES6+ rules
      "prefer-const": "error",
      "no-var": "error",
      "arrow-spacing": "error"
    }
  }
];