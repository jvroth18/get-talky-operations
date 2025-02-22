from flask import Flask, render_template, request, redirect, url_for, flash
import sys
import os
from datetime import datetime

# Add the pyACH directory to the Python path
sys.path.append(os.path.abspath("pyACH"))
from pyach.ACHRecordTypes import ACHFile
import pyach.ACHRecordTypes as ach_types

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Create output directory if it doesn't exist
OUTPUT_DIR = 'ach_files'
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_file', methods=['GET', 'POST'])
def create_file():
    if request.method == 'POST':
        try:
            # Create new ACH file
            payment_file = ACHFile()
            
            # Set file header information
            payment_file.destination_routing_number = request.form['destination_routing_number']
            payment_file.origin_id = request.form['origin_id']
            payment_file.destination_name = request.form['destination_name']
            payment_file.origin_name = request.form['origin_name']
            payment_file.reference_code = request.form.get('reference_code', '')
            
            # Create header
            payment_file.create_header()
            
            # Process each batch
            batches = parse_batch_data(request.form)
            for batch_data in batches:
                # Set batch information
                payment_file.batch_name = batch_data['batch_name']
                payment_file.entry_description = batch_data['entry_description']
                payment_file.company_identification_number = batch_data['company_identification_number']
                payment_file.entry_class_code = batch_data['entry_class_code']
                payment_file.service_class_code = ach_types.MIXED
                
                # Create new batch
                payment_file.new_batch(batch_data['dfi_number'], batch_data['batch_name'])
                
                # Add entries for this batch
                for entry in batch_data['entries']:
                    payment_file.batch_records[-1].add_entry(
                        int(entry['transaction_code']),
                        entry['payor_routing_number'],
                        entry['payor_account_number'],
                        float(entry['amount']),
                        entry['payor_id'],
                        entry['payor_name'],
                        discretionary_data=ach_types.SINGLE_ENTRY
                    )
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'ach_file_{timestamp}.txt'
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            # Save the file
            payment_file.save(filepath)
            
            flash(f'ACH file created successfully: {filename}', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            flash(f'Error creating ACH file: {str(e)}', 'error')
            return redirect(url_for('create_file'))
            
    return render_template('create_file.html')

def parse_batch_data(form_data):
    """Parse the form data to extract batch information."""
    batches = []
    batch_indices = set()
    
    # Find all batch indices from form data
    for key in form_data:
        if key.startswith('batches['):
            batch_idx = int(key.split('[')[1].split(']')[0])
            batch_indices.add(batch_idx)
    
    # Process each batch
    for idx in sorted(batch_indices):
        batch = {
            'batch_name': form_data.get(f'batches[{idx}][batch_name]'),
            'entry_description': form_data.get(f'batches[{idx}][entry_description]'),
            'company_identification_number': form_data.get(f'batches[{idx}][company_identification_number]'),
            'entry_class_code': form_data.get(f'batches[{idx}][entry_class_code]'),
            'dfi_number': form_data.get(f'batches[{idx}][dfi_number]'),
            'entries': []
        }
        
        # Find all entry indices for this batch
        entry_indices = set()
        for key in form_data:
            if key.startswith(f'batches[{idx}][entries]'):
                try:
                    entry_idx = int(key.split('[entries][')[1].split(']')[0])
                    entry_indices.add(entry_idx)
                except (IndexError, ValueError):
                    continue
        
        # Process each entry in this batch
        for entry_idx in sorted(entry_indices):
            entry = {
                'transaction_code': form_data.get(f'batches[{idx}][entries][{entry_idx}][transaction_code]', ''),
                'amount': form_data.get(f'batches[{idx}][entries][{entry_idx}][amount]', '0'),
                'payor_routing_number': form_data.get(f'batches[{idx}][entries][{entry_idx}][payor_routing_number]', ''),
                'payor_account_number': form_data.get(f'batches[{idx}][entries][{entry_idx}][payor_account_number]', ''),
                'payor_id': form_data.get(f'batches[{idx}][entries][{entry_idx}][payor_id]', ''),
                'payor_name': form_data.get(f'batches[{idx}][entries][{entry_idx}][payor_name]', '')
            }
            # Only add entry if it has a transaction code
            if entry['transaction_code']:
                batch['entries'].append(entry)
        
        batches.append(batch)
    
    return batches

if __name__ == '__main__':
    app.run(debug=True) 