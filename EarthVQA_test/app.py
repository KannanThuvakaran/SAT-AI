from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os
import subprocess
import h5py
import numpy as np
from PIL import Image
from collections import OrderedDict

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'dataset/Test/my_test_png/'
app.config['OUTPUT_FOLDER'] = 'log/sfpnr50/my_test_features/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def convert_feature_map_to_mask(feature_map_array, output_path):
    COLOR_MAP = OrderedDict([
        ('Background', (255, 255, 255)),
        ('Building', (255, 0, 0)),
        ('Road', (255, 255, 0)),
        ('Water', (0, 0, 255)),
        ('Barren', (159, 129, 183)),
        ('Forest', (0, 255, 0)),
        ('Agricultural', (255, 195, 128)),
        ('Playground', (165, 0, 165)),
        ('Pond', (0, 185, 246))
    ])
    
    if feature_map_array.ndim == 3:
        feature_map_array = np.argmax(feature_map_array, axis=0)
    
    height, width = feature_map_array.shape
    rgb_array = np.zeros((height, width, 3), dtype=np.uint8)
    
    for class_index, color in enumerate(COLOR_MAP.values()):
        mask = feature_map_array == class_index
        rgb_array[mask] = color

    target_size = (4096, 4096)
    image = Image.fromarray(rgb_array)
    if image.size != target_size:
        image = image.resize(target_size, Image.LANCZOS)
    
    image.save(output_path)

def perform_semantic_segmentation(input_path, output_path):
    filename_no_ext = os.path.splitext(os.path.basename(input_path))[0]
    hdf5_file = f'./log/sfpnr50/my_test_features/{filename_no_ext}.hdf5'
    
    cmd = [
        'python', './predict_seg.py',
        f'--config_path=sfpnr50',
        f'--ckpt_path=./log/sfpnr50.pth',
        f'--save_dir=./log/sfpnr50/my_test_features'
    ]
    subprocess.run(cmd, check=True)

    with h5py.File(hdf5_file, 'r') as f:
        dataset_name = 'pred_mask'
        dataset = f[dataset_name]
        segmented_array = np.array(dataset)
        
        print(f"Dataset name: {dataset_name}")
        print(f"Shape: {segmented_array.shape}, Dtype: {segmented_array.dtype}")
        
        convert_feature_map_to_mask(segmented_array, output_path)

@app.route('/')
def index():
    original_image = request.args.get('original')
    segmented_image = request.args.get('segmented')
    return render_template('index.html', original_image=original_image, segmented_image=segmented_image)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return redirect(request.url)
    
    file = request.files['image']
    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = file.filename
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)

        segmented_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        perform_semantic_segmentation(upload_path, segmented_path)

        return redirect(url_for('index', original=filename, segmented=filename))
    
    return redirect(request.url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/outputs/<filename>')
def output_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    app.run(debug=True)

