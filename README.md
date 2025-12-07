# 🤖 Organizador Automático de PDFs com IA

Sistema inteligente que **identifica automaticamente** o tipo de cada documento PDF usando análise de texto e inteligência artificial.

## ✨ Funcionalidades

### 🎯 Classificação Automática
- **IA Inteligente**: Lê o conteúdo de cada PDF e identifica o tipo automaticamente
- **Confiança Visual**: Mostra o nível de confiança de cada classificação (Alta, Média, Baixa)
- **Palavras-chave**: Exibe as palavras encontradas que ajudaram na identificação
- **Correção Manual**: Permite alterar manualmente qualquer classificação

### 📋 Gerenciamento de Checklists
- Crie quantas checklists quiser
- Edite checklists existentes
- 2 exemplos prontos incluídos

### 📂 Organização Profissional
- Renomeia automaticamente: `001_Contrato_Social.pdf`, `002_RG_Socio_1.pdf`
- Gera arquivo ZIP organizado
- Pronto para inserir em outros sistemas

## 🚀 Como Usar

### 1️⃣ Iniciar o Servidor

Abra o terminal e execute:

```bash
python3 server.py
```

Você verá:
```
🚀 PDF Organizer Server - INICIADO!
📂 Classificação Automática de Documentos ATIVADA
🌐 Acesse: http://localhost:5000
```

### 2️⃣ Abrir no Navegador

Acesse no seu navegador:
```
http://localhost:5000
```

### 3️⃣ Usar o Sistema

1. **Selecione ou Crie uma Checklist**
   - Use os exemplos prontos ou crie sua própria

2. **Faça Upload dos PDFs**
   - Arraste até 200 PDFs de uma vez
   - Ou clique para selecionar

3. **Classificação Automática**
   - O sistema analisa cada PDF automaticamente
   - Mostra a confiança da classificação
   - Exibe as palavras-chave encontradas

4. **Revisar e Ajustar (se necessário)**
   - Clique em "Alterar" para corrigir manualmente
   - Sistema marca classificações manuais em laranja

5. **Gerar Arquivos Organizados**
   - Clique no botão verde
   - Baixe o ZIP com tudo organizado!

## 🎨 Indicadores Visuais

- **Verde**: Documento classificado automaticamente com alta confiança
- **Laranja**: Classificação manual ou baixa confiança
- **Badge de Confiança**: 
  - 🟢 70%+ = Alta confiança
  - 🟡 40-69% = Média confiança
  - 🔴 <40% = Baixa confiança (revisar)

## 🔍 Como Funciona a IA

O sistema usa múltiplas técnicas:

1. **Extração de Texto**: Lê o conteúdo do PDF
2. **Análise de Palavras-chave**: Procura por termos específicos (ex: "CPF", "RG", "Contrato")
3. **Similaridade**: Compara o texto com os nomes da checklist
4. **Pontuação Inteligente**: Combina todos os fatores para dar uma nota de confiança

### Exemplos de Identificação

- **RG**: Procura por "identidade", "registro geral", "SSP"
- **CPF**: Procura por "cadastro de pessoas físicas", "receita federal"
- **Contrato**: Procura por "contrato", "cláusulas", "partes contratantes"
- **Comprovante**: Procura por "comprovante", "endereço", "residência"

## 📊 Estatísticas em Tempo Real

O painel lateral mostra:
- **Arquivos**: Total de PDFs carregados
- **Auto**: Quantos foram classificados automaticamente
- **Completo**: Percentual de conclusão

## 🛠️ Requisitos Técnicos

- Python 3.x
- Bibliotecas instaladas automaticamente:
  - Flask (servidor web)
  - pdfplumber (leitura de PDFs)
  - flask-cors (comunicação)

## ⚡ Dicas de Uso

1. **Para melhor precisão**: Use nomes descritivos na checklist (ex: "RG do Sócio 1" em vez de apenas "Documento")

2. **PDFs escaneados**: O sistema funciona melhor com PDFs de texto. Para PDFs escaneados (imagens), a precisão pode ser menor.

3. **Revisar sempre**: Mesmo com alta confiança, sempre revise as classificações importantes.

4. **Múltiplas checklists**: Crie checklists diferentes para processos diferentes (abertura de empresa, admissão, etc)

## 🎯 Casos de Uso

- ✅ Abertura de empresas (múltiplos documentos de sócios)
- ✅ Admissão de funcionários
- ✅ Processos jurídicos
- ✅ Documentação contábil
- ✅ Processos de licitação
- ✅ Qualquer fluxo com documentação padronizada

## 📝 Notas

- O servidor precisa estar rodando para usar o sistema
- Os arquivos são processados localmente (não são enviados para nenhum servidor externo)
- As checklists são salvas no navegador (localStorage)

## 🆘 Resolução de Problemas

**Erro de conexão?**
- Verifique se o servidor está rodando
- Acesse http://localhost:5000 (não http://localhost:5000/index.html)

**Classificação errada?**
- Use o botão "Alterar" para corrigir manualmente
- Quanto mais descritiva a checklist, melhor a precisão

**PDFs não identificados?**
- PDFs escaneados (imagens) podem não ter texto extraível
- Nesse caso, classifique manualmente

---

**Desenvolvido para facilitar sua organização documental! 🚀**
