#!/usr/bin/env python3
"""
PDF Organizer - Backend Server
Automatic PDF Classification and Organization
"""

from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import pdfplumber
import io
import os
import zipfile
import tempfile
import shutil
from pathlib import Path
import re
import json
from difflib import SequenceMatcher

app = Flask(__name__)
CORS(app)

# Store uploaded files in memory
uploaded_files = {}
checklists = {}

def extract_text_from_pdf(pdf_bytes):
    """Extract text from PDF using pdfplumber"""
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            text = ""
            # Extract text from first 3 pages (usually enough for identification)
            for page in pdf.pages[:3]:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text.lower()
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""

def normalize_text(text):
    """Normalize text for better matching"""
    # Remove special characters and extra spaces
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip().lower()

def calculate_similarity(text1, text2):
    """Calculate similarity between two texts"""
    return SequenceMatcher(None, text1, text2).ratio()

def classify_document(pdf_text, checklist_items):
    """
    Automatically classify document based on content
    Returns: (index, confidence_score, matched_keywords)
    """
    if not pdf_text or not checklist_items:
        return None, 0, []
    
    pdf_text_normalized = normalize_text(pdf_text)
    
    # Keywords for common document types
    document_patterns = {
        'rg': ['identidade', 'rg', 'registro geral', 'secretaria de segurança', 'doc identidade'],
        'cpf': ['cpf', 'cadastro de pessoas físicas', 'receita federal', 'ministério da fazenda'],
        'cnh': ['cnh', 'carteira nacional de habilitação', 'habilitação', 'detran', 'motorista'],
        'contrato': ['contrato', 'partes contratantes', 'cláusula', 'assinatura', 'testemunhas'],
        'comprovante': ['comprovante', 'endereço', 'residência', 'residente', 'domicílio'],
        'certidão': ['certidão', 'registro civil', 'cartório', 'nascimento', 'casamento', 'óbito'],
        'declaração': ['declaração', 'declaro', 'declaramos', 'firma'],
        'procuração': ['procuração', 'procurador', 'outorgante', 'poderes'],
        'título': ['título', 'eleitor', 'eleitoral', 'tribunal regional eleitoral', 'tre'],
        'diploma': ['diploma', 'certificado', 'conclusão', 'curso', 'graduação'],
        'ctps': ['carteira de trabalho', 'ctps', 'trabalho e previdência', 'emprego'],
        'conta': ['conta de luz', 'conta de água', 'energia elétrica', 'saneamento', 'fatura'],
        'iptu': ['iptu', 'imposto predial', 'territorial urbano', 'prefeitura'],
        'alvará': ['alvará', 'licença', 'funcionamento', 'prefeitura municipal'],
        'social': ['contrato social', 'estatuto social', 'sócios', 'capital social', 'sede'],
        'inscrição': ['inscrição municipal', 'inscrição estadual', 'cnpj', 'contribuinte'],
        'balanço': ['balanço', 'demonstração', 'financeiro', 'contábil', 'ativo', 'passivo'],
        'ata': ['ata', 'assembleia', 'reunião', 'deliberação'],
        'procuração empresarial': ['procuração empresarial', 'cnpj', 'empresa', 'representante legal']
    }
    
    best_match = None
    best_score = 0
    matched_keywords = []
    
    for idx, item_name in enumerate(checklist_items):
        item_normalized = normalize_text(item_name)
        score = 0
        item_keywords = []
        
        # Direct name similarity
        name_similarity = calculate_similarity(item_normalized, pdf_text_normalized)
        score += name_similarity * 2
        
        # Check if item name appears in document
        if item_normalized in pdf_text_normalized:
            score += 3
            item_keywords.append(item_name)
        
        # Check keyword patterns
        for doc_type, keywords in document_patterns.items():
            if any(keyword in item_normalized for keyword in [doc_type]):
                for keyword in keywords:
                    if keyword in pdf_text_normalized:
                        score += 1.5
                        item_keywords.append(keyword)
        
        # Word-by-word matching
        item_words = item_normalized.split()
        for word in item_words:
            if len(word) > 3 and word in pdf_text_normalized:
                score += 0.5
                if word not in item_keywords:
                    item_keywords.append(word)
        
        if score > best_score:
            best_score = score
            best_match = idx
            matched_keywords = item_keywords
    
    # Confidence threshold
    confidence = min(best_score * 10, 100)  # Convert to percentage
    
    return best_match, confidence, matched_keywords

@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_from_directory('.', 'pdf-organizer-auto.html')

@app.route('/api/upload', methods=['POST'])
def upload_files():
    """Handle PDF upload and automatic classification"""
    try:
        files = request.files.getlist('files')
        checklist_name = request.form.get('checklist_name')
        checklist_items_json = request.form.get('checklist_items')
        
        if not checklist_name or not checklist_items_json:
            return jsonify({'error': 'Checklist não fornecida'}), 400
        
        checklist_items = json.loads(checklist_items_json)
        
        results = []
        
        for file in files:
            if file.filename.endswith('.pdf'):
                # Read file
                pdf_bytes = file.read()
                file_id = f"{len(uploaded_files)}_{file.filename}"
                
                # Store file
                uploaded_files[file_id] = {
                    'bytes': pdf_bytes,
                    'filename': file.filename
                }
                
                # Extract text
                pdf_text = extract_text_from_pdf(pdf_bytes)
                
                # Classify document
                doc_index, confidence, keywords = classify_document(pdf_text, checklist_items)
                
                results.append({
                    'file_id': file_id,
                    'filename': file.filename,
                    'doc_index': doc_index,
                    'confidence': round(confidence, 1),
                    'matched_keywords': keywords[:5],  # Top 5 keywords
                    'text_preview': pdf_text[:200] if pdf_text else 'Não foi possível extrair texto'
                })
        
        return jsonify({
            'success': True,
            'results': results
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate', methods=['POST'])
def generate_organized_files():
    """Generate organized ZIP file"""
    try:
        data = request.json
        checklist_name = data.get('checklist_name')
        checklist_items = data.get('checklist_items')
        assignments = data.get('assignments')
        
        if not all([checklist_name, checklist_items, assignments]):
            return jsonify({'error': 'Dados incompletos'}), 400
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Create organized files
            for file_id, doc_index in assignments.items():
                if file_id in uploaded_files:
                    file_data = uploaded_files[file_id]
                    doc_name = checklist_items[int(doc_index)]
                    
                    # Generate new filename
                    number = str(int(doc_index) + 1).zfill(3)
                    safe_doc_name = sanitize_filename(doc_name)
                    new_filename = f"{number}_{safe_doc_name}.pdf"
                    
                    # Save file
                    file_path = os.path.join(temp_dir, new_filename)
                    with open(file_path, 'wb') as f:
                        f.write(file_data['bytes'])
            
            # Create ZIP
            zip_path = os.path.join(temp_dir, f"{sanitize_filename(checklist_name)}_Organizado.zip")
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith('.pdf'):
                            file_path = os.path.join(root, file)
                            zipf.write(file_path, file)
            
            # Send ZIP file
            return send_file(
                zip_path,
                mimetype='application/zip',
                as_attachment=True,
                download_name=f"{sanitize_filename(checklist_name)}_Organizado.zip"
            )
        
        finally:
            # Cleanup is handled by Flask after sending
            pass
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clear', methods=['POST'])
def clear_files():
    """Clear all uploaded files"""
    global uploaded_files
    uploaded_files = {}
    return jsonify({'success': True})

def sanitize_filename(name):
    """Sanitize filename for safe file system usage"""
    # Remove invalid characters
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    # Replace spaces with underscores
    name = name.replace(' ', '_')
    # Limit length
    return name[:100]

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 PDF Organizer Server - INICIADO!")
    print("=" * 60)
    print("📂 Classificação Automática de Documentos ATIVADA")
    print("🌐 Acesse: http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
