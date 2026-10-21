#!/usr/bin/env node

/**
 * uaippt CLI — Gerador de apresentações PowerPoint (.pptx) no padrão oficial SENAI / Fatesg
 * com Motion Design (Manim & Blender) e skill para AI Coding Agents.
 *
 * Repositório: https://github.com/Ujeverson/uaippt
 * npm: https://www.npmjs.com/package/uaippt
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');
const { spawn, execSync } = require('child_process');

const VERSION = '1.0.0';
const PACKAGE_ROOT = path.resolve(__dirname, '..');
const SKILL_SOURCE = path.join(PACKAGE_ROOT, '.agents', 'skills', 'uaippt');

function printBanner() {
  console.log('\n\x1b[34m=================================================================\x1b[0m');
  console.log('\x1b[1m\x1b[34m  uaippt\x1b[0m \x1b[33mv' + VERSION + '\x1b[0m — Gerador de Apresentações SENAI / Fatesg & Motion Design');
  console.log('\x1b[36m  GitHub: https://github.com/Ujeverson/uaippt\x1b[0m');
  console.log('\x1b[34m=================================================================\x1b[0m\n');
}

function printHelp() {
  printBanner();
  console.log('Uso:');
  console.log('  uaippt <comando> [opções]\n');
  console.log('Comandos:');
  console.log('  create [saida.pptx]          Cria uma nova apresentação interativamente.');
  console.log('  build <roteiro.json> [saida] Gera uma apresentação a partir de um arquivo JSON.');
  console.log('  init [destino]               Instala a skill uaippt na pasta de AI Agents.');
  console.log('  skill-path                   Exibe o caminho dos arquivos da skill instalada.');
  console.log('  --version, -v                Exibe a versão do uaippt.');
  console.log('  --help, -h                   Exibe este menu de ajuda.\n');
  console.log('Exemplos:');
  console.log('  npx uaippt create aula1.pptx');
  console.log('  npx uaippt build roteiro.json apresentacao.pptx');
  console.log('  npx uaippt init .agents/skills/uaippt\n');
}

function getPythonCmd() {
  const candidates = ['python', 'py', 'python3'];
  for (const cmd of candidates) {
    try {
      execSync(`${cmd} --version`, { stdio: 'ignore' });
      return cmd;
    } catch (e) {
      // continua tentando
    }
  }
  return null;
}

function askQuestion(rl, query) {
  return new Promise((resolve) => rl.question(query, resolve));
}

async function handleCreate(outputFile) {
  printBanner();
  const pythonCmd = getPythonCmd();
  if (!pythonCmd) {
    console.error('\x1b[31mErro: Python não encontrado no sistema. Por favor, instale o Python 3.10+.\x1b[0m');
    process.exit(1);
  }

  const outPptx = outputFile || 'apresentacao_uaippt.pptx';
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  console.log('Configuração da Apresentação (Padrão Oficial SENAI / Fatesg):\n');

  const title = (await askQuestion(rl, '\x1b[1m1. Título da Apresentação:\x1b[0m ')).trim() || 'Apresentação SENAI';
  const subtitle = (await askQuestion(rl, '\x1b[1m2. Subtítulo:\x1b[0m ')).trim() || 'Aula Expositiva';
  
  let professor = '';
  while (!professor) {
    professor = (await askQuestion(rl, '\x1b[1m\x1b[33m3. Nome do(a) Professor(a) [obrigatório na capa]:\x1b[0m ')).trim();
    if (!professor) {
      console.log('\x1b[31m   Atenção: O nome do(a) professor(a) é obrigatório para constar na capa.\x1b[0m');
    }
  }

  const course = (await askQuestion(rl, '\x1b[1m4. Unidade Curricular / Curso (padrão: Faculdade SENAI Fatesg):\x1b[0m ')).trim() || 'Faculdade SENAI Fatesg';
  rl.close();

  const deckScript = path.join(SKILL_SOURCE, 'scripts', 'uaippt_deck.py');
  const starterOutline = {
    title: title,
    course: course,
    professor: professor,
    output: outPptx,
    slides: [
      {
        type: 'cover',
        title: title,
        subtitle: subtitle,
        course: course,
        professor: professor,
        notes: 'Apresentação gerada com uaippt (padrão SENAI / Faculdade SENAI Fatesg).'
      },
      {
        type: 'bullets',
        title: 'Objetivos e Visão Geral',
        items: [
          'Introdução aos principais conceitos da aula',
          ['Detalhamento e contextualização técnica', 1],
          'Desenvolvimento de competências profissionais SENAI',
          'Atividades práticas e avaliação'
        ],
        notes: 'Explanar os objetivos de aprendizagem alinhados com o itinerário formativo.'
      },
      {
        type: 'highlight',
        title: 'Conceito Fundamental',
        statement: 'A prática integrada com a teoria é a base da metodologia de educação profissional do SENAI.',
        items: [
          'Foco no domínio técnico e aplicação direta',
          'Metodologias ativas e resolução de problemas reais'
        ],
        notes: 'Enfatizar a importância da aprendizagem significativa.'
      },
      {
        type: 'closing',
        title: 'Obrigado!',
        subtitle: `${course} • Bons estudos!`
      }
    ]
  };

  const tempJson = path.join(process.cwd(), `.tmp_uaippt_${Date.now()}.json`);
  fs.writeFileSync(tempJson, JSON.stringify(starterOutline, null, 2), 'utf-8');

  console.log(`\nGerando apresentação '${outPptx}' com Python...`);
  const proc = spawn(pythonCmd, [deckScript, tempJson, path.resolve(process.cwd(), outPptx)], { stdio: 'inherit' });

  proc.on('close', (code) => {
    try { fs.unlinkSync(tempJson); } catch (e) {}
    if (code === 0) {
      console.log(`\n\x1b[32m✔ Sucesso! Apresentação gerada em:\x1b[0m ${path.resolve(process.cwd(), outPptx)}\n`);
    } else {
      console.error(`\n\x1b[31mFalha ao gerar apresentação (código ${code}).\x1b[0m`);
    }
  });
}

function handleBuild(jsonFile, outputFile) {
  if (!jsonFile) {
    console.error('\x1b[31mErro: Informe o caminho do arquivo JSON do roteiro.\x1b[0m');
    console.log('Exemplo: uaippt build roteiro.json saida.pptx');
    process.exit(1);
  }

  const pythonCmd = getPythonCmd();
  if (!pythonCmd) {
    console.error('\x1b[31mErro: Python não encontrado no sistema.\x1b[0m');
    process.exit(1);
  }

  const resolvedJson = path.resolve(process.cwd(), jsonFile);
  if (!fs.existsSync(resolvedJson)) {
    console.error(`\x1b[31mErro: Arquivo não encontrado: ${resolvedJson}\x1b[0m`);
    process.exit(1);
  }

  const deckScript = path.join(SKILL_SOURCE, 'scripts', 'uaippt_deck.py');
  const args = [deckScript, resolvedJson];
  if (outputFile) {
    args.push(path.resolve(process.cwd(), outputFile));
  }

  const proc = spawn(pythonCmd, args, { stdio: 'inherit' });
  proc.on('close', (code) => {
    if (code === 0) {
      console.log('\n\x1b[32m✔ Apresentação gerada com sucesso!\x1b[0m');
    } else {
      console.error(`\n\x1b[31mFalha na geração (código ${code}).\x1b[0m`);
    }
  });
}

function copyRecursiveSync(src, dest) {
  const exists = fs.existsSync(src);
  const stats = exists && fs.statSync(src);
  const isDirectory = exists && stats.isDirectory();
  if (isDirectory) {
    if (!fs.existsSync(dest)) fs.mkdirSync(dest, { recursive: true });
    fs.readdirSync(src).forEach((childItemName) => {
      copyRecursiveSync(path.join(src, childItemName), path.join(dest, childItemName));
    });
  } else {
    fs.copyFileSync(src, dest);
  }
}

function handleInit(targetDir) {
  printBanner();
  const dest = targetDir ? path.resolve(process.cwd(), targetDir) : path.resolve(process.cwd(), '.agents', 'skills', 'uaippt');

  if (!fs.existsSync(SKILL_SOURCE)) {
    console.error(`\x1b[31mErro: Origem da skill não encontrada em: ${SKILL_SOURCE}\x1b[0m`);
    process.exit(1);
  }

  console.log(`Instalando skill uaippt em:\n  \x1b[36m${dest}\x1b[0m\n`);
  copyRecursiveSync(SKILL_SOURCE, dest);
  console.log('\x1b[32m✔ Skill uaippt instalada com sucesso!\x1b[0m');
  console.log('AI Coding Agents (Antigravity, Claude Code, Cursor) já podem utilizá-la automaticamente.\n');
}

// ---------------------------------------------------------------- Dispatcher CLI
const args = process.argv.slice(2);
const command = args[0] || '--help';

switch (command) {
  case '-v':
  case '--version':
  case 'version':
    console.log(`uaippt v${VERSION}`);
    break;

  case '-h':
  case '--help':
  case 'help':
    printHelp();
    break;

  case 'create':
    handleCreate(args[1]);
    break;

  case 'build':
    handleBuild(args[1], args[2]);
    break;

  case 'init':
    handleInit(args[1]);
    break;

  case 'skill-path':
    console.log(SKILL_SOURCE);
    break;

  default:
    console.error(`\x1b[31mComando desconhecido: ${command}\x1b[0m\n`);
    printHelp();
    process.exit(1);
}
