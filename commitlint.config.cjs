// Conventional Commits + gitmoji shortcodes
// :emoji: type(scope): subject — max 72 chars, English subject

module.exports = {
  extends: ['@commitlint/config-conventional'],
  parserPreset: {
    parserOpts: {
      headerPattern:
        /^(:[a-z0-9_+\-]+:)\s+(feat|fix|security|config|docs|style|refactor|perf|test|build|ci|chore|revert|hotfix|raw|cleanup|remove)(?:\(([^)]+)\))?:\s(.+)$/,
      headerCorrespondence: ['emoji', 'type', 'scope', 'subject'],
    },
  },
  rules: {
    'header-max-length': [2, 'always', 72],
    'type-empty': [2, 'never'],
    'type-enum': [
      2,
      'always',
      [
        'feat',
        'fix',
        'security',
        'config',
        'docs',
        'style',
        'refactor',
        'perf',
        'test',
        'build',
        'ci',
        'chore',
        'revert',
        'hotfix',
        'raw',
        'cleanup',
        'remove',
      ],
    ],
    'subject-empty': [2, 'never'],
    'subject-case': [0],
  },
  ignores: [
    (commit) => {
      const header = commit.split('\n', 1)[0];
      return (
        /^(Merge |Revert |fixup!|squash!)/.test(header) ||
        /^(Bump |:arrow_up:)/.test(header) ||
        /\(deps[\w-]*\):/.test(header)
      );
    },
  ],
};
