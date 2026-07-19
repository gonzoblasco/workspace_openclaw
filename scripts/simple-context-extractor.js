#!/usr/bin/env node
/**
 * Simple Kanam context extractor - reads workspace docs and summarizes state
 */

const fs = require('fs');
const path = require('path');

const ROOT_DIR = '/Users/gonzoblasco/.openclaw/workspace';

console.log('🔍 Extracting Kanam context...\n');

// Workspace fundamental docs
const workspaceDocs = [
  { file: 'AGENTS.md', role: 'agent-workspace' },
  { file: 'SOUL.md', role: 'persona/tone' },
  { file: 'USER.md', role: 'about-your-human' },
  { file: 'TOOLS.md', role: 'local-notes' },
  { file: 'MEMORY.md', role: 'long-term-memory' }
];

console.log('📄 Workspace Configuration:');
for (const doc of workspaceDocs) {
  const fullFile = `${ROOT_DIR}/${doc.file}`;
  if (fs.existsSync(fullFile)) {
    let summary = '';
    try {
      const content = fs.readFileSync(fullFile, 'utf8');
      // Extract title or first paragraph
      if (content.match(/^#\s+(.+)$/)) {
        summary = content.split('\n').filter(l => l.startsWith('#')).pop() || 'Content loaded';
      } else {
        summary = 'Document present and loaded';
      }
    } catch (e) {
      summary = `Cannot read: ${e.message}`;
    }
    console.log(`  ✅ ${doc.file}: ${summary}`);
  } else {
    console.log(`  ⚠️ ${doc.file}: NOT FOUND`);
  }
}

// Check project structure
console.log('\n📁 Project Structure:');
const projDirs = fs.readdirSync(ROOT_DIR).filter(d => d.startsWith('projects/') || d.startsWith('products/'));
for (const dir of projDirs) {
  const fullDir = `${ROOT_DIR}/${dir}`;
  if (fs.existsSync(fullDir)) {
    const contents = fs.readdirSync(fullDir);
    console.log(`  - ${dir}/ (${contents.length} items)`);
  } else {
    console.log(`  ⚠️ ${dir}/: directory missing`);
  }
}

// Summary
console.log('\n📊 Status Summary:');
const workspaceDocs = [
  { file: 'AGENTS.md', role: 'agent-workspace' },
  { file: 'SOUL.md', role: 'persona/tone' },
  { file: 'USER.md', role: 'about-your-human' },
  { file: 'TOOLS.md', role: 'local-notes' },
  { file: 'MEMORY.md', role: 'long-term-memory' }
];

let found = 0;
for (const doc of workspaceDocs) {
  const fullFile = `${ROOT_DIR}/${doc.file}`;
  if (fs.existsSync(fullFile)) {
    try {
      const content = fs.readFileSync(fullFile, 'utf8');
      if (!content.includes('Con') && !content.includes('Gonzo') && !content.includes('Kanam')) {
        console.log(`  ⚠️ ${doc.file}: Missing key context (not Gonzo/Kanam focused)`);
      } else {
        console.log(`  ✅ ${doc.file}: Context found`);
        found++;
      }
    } catch (e) {
      console.log(`  ⚠️ ${doc.file}: Cannot read (not Gonzo/Kanam focused)`);
    }
  } else {
    console.log(`  ⚠️ ${doc.file}: NOT FOUND`);
  }
}

console.log(`\n✅ Found ${found}/${workspaceDocs.length} workspace docs with key context`);
console.log('📄 Next step: Read full files for detailed spec generation');
