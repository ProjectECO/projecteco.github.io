from flask import Flask, request

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    six_plt = data.get('sixPlt')
    nine_plt = data.get('ninePlt')
    ten_plt = data.get('10plt')
    ten_plt_comp = data.get('10pltcomp')

    # Perform your Python code with the received values
    # Example: Calculate the total count
    total_count = int(six_plt) + int(nine_plt) + int(ten_plt) + int(ten_plt_comp)

    # Prepare the response message
    response = f"Total count: {total_count}"

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)