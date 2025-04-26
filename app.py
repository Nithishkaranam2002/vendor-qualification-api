from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)


df = None

# Loading  the dataset
def load_data():
    global df
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, 'cleaned_vendor_data.csv')
    print(f"Loading dataset from: {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"Dataset loaded successfully with {len(df)} records")
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]

# Loading the  data at startup
load_data()

def filter_and_rank_vendors(software_category, capabilities):
    if software_category:
        filtered_df = df[df['main_category'].str.contains(software_category, case=False, na=False)]
    else:
        filtered_df = df.copy()
    
    if capabilities:
        for capability in capabilities:
            filtered_df = filtered_df[filtered_df['parsed_features'].str.contains(capability, case=False, na=False)]
    
    filtered_df = filtered_df.sort_values(by='rating', ascending=False)
    top_vendors = filtered_df.head(10)[['product_name', 'main_category', 'parsed_features', 'rating']].to_dict('records')
    
    return top_vendors

@app.route('/vendor_qualification', methods=['POST'])
def vendor_qualification():
    try:
        data = request.get_json()
        software_category = data.get('software_category', '')
        capabilities = data.get('capabilities', [])
        
        top_vendors = filter_and_rank_vendors(software_category, capabilities)
        
        return jsonify({
            'status': 'success',
            'data': {
                'top_vendors': top_vendors,
                'count': len(top_vendors)
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'The Vendor Qualification API is running'
    })



if __name__ == '__main__':
    print("Starting Flask application on http://0.0.0.0:8000")
    app.run(debug=True, host='0.0.0.0', port=8000)