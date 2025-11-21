import unusedImports from 'eslint-plugin-unused-imports'
import { FlatCompat } from '@eslint/eslintrc'
import js from '@eslint/js'
import typescriptEslint from '@typescript-eslint/eslint-plugin'
import typescriptParser from '@typescript-eslint/parser'
import importPlugin from 'eslint-plugin-import'
import jsxA11y from 'eslint-plugin-jsx-a11y'
import n from 'eslint-plugin-n'
import noRelativeImportPaths from 'eslint-plugin-no-relative-import-paths'
import prettier from 'eslint-plugin-prettier'
// @ts-ignore - no types available
import promise from 'eslint-plugin-promise'
import react from 'eslint-plugin-react'
import reactHooks from 'eslint-plugin-react-hooks'

import simpleImportSort from 'eslint-plugin-simple-import-sort'
import { dirname } from 'path'

import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

const compat = new FlatCompat({
  baseDirectory: __dirname,
  recommendedConfig: js.configs.recommended,
  allConfig: js.configs.all,
})

// Shared rules that apply to all file types
const sharedRules = {
  // Semicolon rules (matching Biome "asNeeded")
  semi: ['error', 'never'],
  'no-extra-semi': 'off',

  // Basic rules
  'prefer-const': 'error',

  // React rules
  'react/jsx-fragments': ['warn', 'syntax'],
  'react/jsx-key': 'off',
  'react/jsx-uses-react': 'off',
  'react/react-in-jsx-scope': 'off',
  'react/jsx-boolean-value': ['error', 'never'],
  'react/self-closing-comp': 'error',
  'react/no-danger': 'off',
  'react/jsx-no-target-blank': 'off',
  'react-hooks/rules-of-hooks': 'error',
  'react-hooks/exhaustive-deps': 'off',

  // Accessibility rules
  'jsx-a11y/html-has-lang': 'warn',
  'jsx-a11y/scope': 'off',
  'jsx-a11y/aria-role': ['warn', { ignoreNonDOM: false, allowedInvalidRoles: ['none', 'text'] }],
  'jsx-a11y/no-autofocus': 'off',
  'jsx-a11y/no-static-element-interactions': 'warn',
  'jsx-a11y/form-control-has-label': 'off',
  'jsx-a11y/media-has-caption': 'off',
  'jsx-a11y/click-events-have-key-events': 'off',
  'jsx-a11y/no-noninteractive-element-interactions': 'off',

  // Complexity rules
  'prefer-template': 'error',
  'no-useless-concat': 'warn',
  'no-continue': 'off',

  // Style rules
  yoda: ['warn', 'never'],
  'no-unneeded-ternary': 'off',
  'no-else-return': 'off',
  curly: 'off',
  'one-var': ['error', 'never'],
  'no-param-reassign': 'error',
  'prefer-numeric-literals': 'error',

  // Suspicious rules
  'no-dupe-else-if': 'warn',
  'no-irregular-whitespace': 'warn',

  // Import rules
  'import/no-unused-modules': 'off',
  'import/first': 'error',
  'import/newline-after-import': 'error',
  'import/no-duplicates': 'error',
  'unused-imports/no-unused-imports': 'error',

  // Prettier integration - disabled since we extend prettier config
  'prettier/prettier': 'off',

  // Import sorting with strict grouping
  'simple-import-sort/imports': [
    'error',
    {
      groups: [
        // Built-in modules (like 'fs', 'path')
        ['^node:'],
        // External packages
        ['^[^@]\\w'],
        // Internal packages (@/...)
        ['^@/'],
        // Relative imports
        ['^\\.\\./', '^\\./'],
      ],
    },
  ],
  'simple-import-sort/exports': 'error',

  // Enforce absolute imports
  'no-relative-import-paths/no-relative-import-paths': ['error', { allowSameFolder: true, rootDir: '.', prefix: '@' }],
}

export default [
  {
    ignores: [
      '**/pnpm-lock.yaml',
      '**/lib/db/migrations/**',
      '**/lib/editor/react-renderer.tsx',
      '**/node_modules/**',
      '**/.next/**',
      '**/public/**',
      '**/.vercel/**',
      '**/.history/**',
      'eslint.config.ts',
      'fix-tailwind-vars.js',
      'components/ui/*.tsx',
      'e2e/**/*',
      '**/*.test.ts',
      '**/*.test.tsx',
      '__tests__/**/*',
    ],
  },
  ...compat.extends('next/core-web-vitals'),
  ...compat.extends('prettier'),
  js.configs.recommended,
  {
    files: ['**/*.{js,jsx,mjs}'],
    plugins: {
      react,
      'react-hooks': reactHooks,
      'jsx-a11y': jsxA11y,
      import: importPlugin,
      promise,
      n,
      prettier,
      'simple-import-sort': simpleImportSort,
      'no-relative-import-paths': noRelativeImportPaths,
      'unused-imports': unusedImports,
    },
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      parserOptions: {
        ecmaFeatures: {
          jsx: true,
        },
      },
    },
    settings: {
      react: {
        version: 'detect',
      },
    },
    rules: {
      ...sharedRules,
      // JS-specific unused vars rule
      'no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
    },
  },
  {
    files: ['**/*.{ts,tsx}'],
    plugins: {
      '@typescript-eslint': typescriptEslint,
      react,
      'react-hooks': reactHooks,
      'jsx-a11y': jsxA11y,
      import: importPlugin,
      promise,
      n,
      prettier,
      'simple-import-sort': simpleImportSort,
      'no-relative-import-paths': noRelativeImportPaths,
      'unused-imports': unusedImports,
    },
    languageOptions: {
      parser: typescriptParser,
      ecmaVersion: 'latest',
      sourceType: 'module',
      parserOptions: {
        ecmaFeatures: {
          jsx: true,
        },
        project: './tsconfig.json',
      },
    },
    settings: {
      react: {
        version: 'detect',
      },
    },
    rules: {
      ...sharedRules,
      // TypeScript-specific rules
      'no-unused-vars': 'off', // Use TypeScript version instead
      '@typescript-eslint/array-type': 'error',
      '@typescript-eslint/no-unused-vars': ['warn', { argsIgnorePattern: '^_', varsIgnorePattern: '^_' }],
      '@typescript-eslint/prefer-optional-chain': 'error',
      '@typescript-eslint/consistent-type-assertions': ['error', { assertionStyle: 'as' }],
      '@typescript-eslint/no-unnecessary-type-assertion': 'error',
      '@typescript-eslint/default-param-last': 'warn',
      '@typescript-eslint/no-inferrable-types': 'error',
      '@typescript-eslint/prefer-literal-enum-member': 'error',
      '@typescript-eslint/no-explicit-any': 'off',
      '@typescript-eslint/consistent-type-imports': [
        'error',
        {
          prefer: 'type-imports',
          fixStyle: 'inline-type-imports',
        },
      ],
      'no-restricted-syntax': [
        'error',
        {
          selector: 'TSBannedTypes',
          message: 'Use of banned types is not allowed',
        },
      ],
      '@next/next/no-head-import-in-document': 'warn',
      '@next/next/no-document-import-in-page': 'warn',
      'no-undef': 'off',
    },
  },
  {
    files: ['**/playwright/**/*.{js,jsx,ts,tsx}'],
    rules: {
      'no-empty-pattern': 'off',
    },
  },
]
